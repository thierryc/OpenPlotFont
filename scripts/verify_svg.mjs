// Independent SVG interchange check: Node standard library; no PlotFont package.
import {readFileSync} from 'node:fs';

const [fontPath, svgPath, text, height = '12'] = process.argv.slice(2);
function demand(condition, message) { if (!condition) throw new Error(message); }
try {
  demand(fontPath && svgPath && text !== undefined, 'Usage: node verify_svg.mjs FONT SVG TEXT [CAP_HEIGHT_MM]');
  const font = JSON.parse(readFileSync(fontPath, 'utf8'));
  const svg = readFileSync(svgPath, 'utf8');
  demand(font.format === 'PlotFont' && font.version === '0.2', 'Unsupported font format/version');
  const scale = Number(height) / font.metrics.capHeight;
  demand(Number.isFinite(scale) && scale > 0, 'Invalid physical scale');
  const glyphs = new Map(font.glyphs.map(g => [g.name, g]));
  const mapping = new Map(font.glyphs.flatMap(g => g.unicodes.map(u => [parseInt(u, 16), g])));
  const expected = [];
  const lines = text.replace(/\r\n?/g, '\n').split('\n');
  for (let row = 0; row < lines.length; row++) {
    let x = 0, previous;
    for (const scalar of lines[row]) {
      demand(scalar !== '\t', 'Tabs require layout policy');
      const g = mapping.get(scalar.codePointAt(0)) ?? glyphs.get(font.missingGlyph);
      demand(g, 'Missing fallback');
      if (previous) x += (font.kerning ?? []).find(p => p.left === previous && p.right === g.name)?.value ?? 0;
      const baseline = row * (font.metrics.ascender - font.metrics.descender + font.metrics.lineGap);
      for (const op of g.strokes) {
        const kind = op.kind ?? 'stroke';
        demand(kind === 'stroke' || kind === 'fill', 'Unsupported operation');
        const tokens = [];
        for (const path of kind === 'stroke' ? [op] : op.contours) {
          for (const command of path.commands) {
            tokens.push(command[0]);
            for (let i = 1; i < command.length; i += 2) tokens.push((x + command[i]) * scale, (baseline - command[i + 1]) * scale);
          }
          if (path.closed) tokens.push('Z');
        }
        expected.push({tokens, kind, fillRule: op.fillRule});
      }
      x += g.advanceWidth;
      previous = g.name;
    }
  }
  demand(/width="[^" ]+mm"/.test(svg) && /height="[^" ]+mm"/.test(svg), 'SVG dimensions must declare millimetres');
  const paths = [...svg.matchAll(/<path\b([^>]*)\/>/g)].map(m => {
    const attrs = Object.fromEntries([...m[1].matchAll(/([\w-]+)="([^"]*)"/g)].map(a => [a[1], a[2]]));
    const tokens = (attrs.d ?? '').match(/[MLQCZ]|[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:e[-+]?\d+)?/gi) ?? [];
    return {attrs, tokens: tokens.map(t => /^[MLQCZ]$/.test(t) ? t : Number(t))};
  });
  demand(paths.length === expected.length, `Independent path count mismatch: ${paths.length} != ${expected.length}`);
  for (let i = 0; i < paths.length; i++) {
    const {tokens, attrs} = paths[i], e = expected[i];
    demand(tokens.length === e.tokens.length, `Path ${i}: command/coordinate count mismatch`);
    for (let j = 0; j < tokens.length; j++) {
      demand(typeof e.tokens[j] === 'number' ? typeof tokens[j] === 'number' && Math.abs(tokens[j] - e.tokens[j]) <= 1e-8 : tokens[j] === e.tokens[j],
             `Path ${i}, token ${j}: order, geometry or axis mismatch`);
    }
    demand(e.kind === 'stroke' ? attrs.fill === 'none' : attrs.stroke === 'none' && attrs['fill-rule'] === e.fillRule,
           `Path ${i}: stroke/fill intent mismatch`);
  }
  console.log(`Verified ${paths.length} independent SVG paths, physical scale, curves, closure and fill rules.`);
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}
