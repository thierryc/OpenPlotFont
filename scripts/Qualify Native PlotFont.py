# MenuTitle: Qualify Native PlotFont
# encoding: utf-8
__doc__ = 'Verify the saved Hershey project source and export, using disposable native fixtures'
import sys
from pathlib import Path
from GlyphsApp import Glyphs
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from plotfont.native_qualification import qualify_native

if __name__ == '__main__':
    print(qualify_native(Glyphs.font, ROOT))
