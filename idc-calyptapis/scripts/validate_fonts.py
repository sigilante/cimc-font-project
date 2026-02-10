#!/usr/bin/env python3
# validate_fonts.py

import fontforge
from pathlib import Path

def validate_font(font_path: Path):
    """Check for common issues"""
    print(f"\nValidating {font_path.name}")
    
    font = fontforge.open(str(font_path))
    
    issues = []
    
    # Check glyph count
    glyph_count = sum(1 for g in font.glyphs() if g.unicode != -1)
    print(f"  Glyphs: {glyph_count}")
    
    # Check for empty glyphs
    empty = [g.glyphname for g in font.glyphs() 
             if g.unicode != -1 and not g.layers[1]]
    if empty:
        issues.append(f"Empty glyphs: {len(empty)}")
    
    # Check for self-intersecting paths
    intersecting = []
    for glyph in font.glyphs():
        if glyph.unicode != -1:
            result = glyph.validate()
            if result:
                intersecting.append(glyph.glyphname)
    
    if intersecting:
        issues.append(f"Self-intersecting: {len(intersecting)}")
    
    # Check metrics
    print(f"  Em: {font.em}")
    print(f"  Ascent: {font.ascent}")
    print(f"  Descent: {font.descent}")
    
    if issues:
        print(f"  ⚠ Issues found:")
        for issue in issues:
            print(f"    - {issue}")
    else:
        print(f"  ✓ No issues found")
    
    font.close()

def main():
    fonts_dir = Path('calyptapis/fonts')
    for font_file in sorted(fonts_dir.glob('*.otf')):
        validate_font(font_file)

if __name__ == '__main__':
    main()