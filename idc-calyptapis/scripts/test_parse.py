from header import *
import level1
from level2 import parse_glyph
import level3
import level4

# test_parse.py
header_params = parse_header(Path('./calyptapis/src/calyptapis.mp'))
jee_glyph_code = Path('./calyptapis/src/letters/U1041a.mp').read_text()
glyph = parse_glyph(jee_glyph_code, 4006)

print(f"Glyph: {glyph.name}")
print(f"Local vars: {glyph.local_variables}")
print(f"Paths: {[p.name for p in glyph.paths]}")
print(f"Symmetry: {glyph.symmetry_axis}")
print(f"Complexity: {glyph.complexity}")
