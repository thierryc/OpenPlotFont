# OpenPlotFont 0.4.0

Draft format 0.4 adds optional per-stroke flexible-pen profiles while retaining
editable centerlines and optional compiled OpenType layout. Python tooling is
0.4.0; the Glyphs 4 exporter is 0.2.0. No package-registry publication is required.

- Preserve authored dimensions, angle, placement, progression, defaults and
  segment-local locations, including explicitly inherited native channels.
- Retain exact bound native appearance alongside Glyphs profiles. Native
  progression is not silently approximated as linear easing. A separate portable
  linear-ellipse model has explicitly defined interpolation.
- Export 0.4 preservation or an explicit 0.3 centerline projection. Existing
  0.2/0.3 fonts keep their meanings; older readers reject 0.4.
- Render profile-aware SVG and ordered per-stroke writing masks. Preview timing
  is a declared constant-speed demonstration, not recovered handwriting.
- Keep optional OpenType layout and glyph-ID bindings when attaching compiled
  layout or producing a centerline projection.

The original public demo qualifies native Save/reopen, precise nodes, nullable
channels, native-expanded reference geometry and both plugin export actions in
Glyphs 4.2 build 4202. Portable conformance tests verify those independently.

Read [the profile contract](PEN_POINTS.md) before implementing a consumer.
Native-profile editing requires regenerating its bound appearance. Generic
Glyphs-progression evaluation, quadratic/implied-point profile remapping,
profile-bearing component transforms, filled-region profiles, joined-profile
transitions, and physical pressure/depth mappings are not implemented.
Unsupported native mappings fail rather than discard values. Plugin installation
and cold-start/menu loading remain separately unqualified.

Release assets contain generic tooling, specification and original fixtures.
No private font sources, drawings, research records or customer packages belong
to this release. The existing public font catalog is unchanged.

## Validation

The full Python suite passes 119 tests. All public schemas/examples, documentation
links, the 87-entry website catalog and exporter payload checks pass. Native
Save/reopen and actual class/action checks ran in Glyphs 4.2 build 4202. Exact
raw native geometry and Pen-point records are retained as original public test
fixtures. Package and published-download integrity are verified separately.
