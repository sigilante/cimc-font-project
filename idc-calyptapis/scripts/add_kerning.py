#!/usr/bin/env python3
# add_kerning.py

import fontforge

def add_basic_kerning(font_path, output_path):
    """Add automatic kerning pairs"""
    font = fontforge.open(str(font_path))
    
    # Auto-kern based on glyph shapes
    # This is FontForge's built-in auto-kerning
    font.addLookup(
        "kern",
        "gpos_pair",
        (),
        (("kern", (("latn", ("dflt")),)),)
    )
    font.addLookupSubtable("kern", "kern-1")
    
    # Auto-kern with reasonable defaults
    font.autoKern("kern-1", 100, onlySelected=False)
    
    # Generate with kerning
    font.generate(str(output_path))
    font.close()
    
    print(f"Added kerning to {output_path}")