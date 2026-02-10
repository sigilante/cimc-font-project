# unicode_mapping.py
#
# MetaPost figure numbers are derived from Unicode codepoints via:
#
#     fig_number = codepoint % 32768
#
# This keeps all figure numbers under MetaPost's 32767 limit.
# The reverse mapping uses known ranges to recover the full codepoint.

# (fig_low, fig_high, unicode_offset)
# where codepoint = fig_number + unicode_offset
_RANGES = [
    (33, 124, 0),          # ASCII punctuation/numerals: U+0021–U+007C
    (1024, 1063, 0x10000), # Deseret capitals: U+10400–U+10427
    (24576, 24588, 0x8000),# PUA variants: U+E000–U+E00C
]

def unicode_to_fig(codepoint: int) -> int:
    """Map a Unicode codepoint to a MetaPost figure number."""
    return codepoint % 32768

def fig_to_unicode(fig_number: int) -> int:
    """Map a MetaPost figure number back to its Unicode codepoint."""
    for low, high, offset in _RANGES:
        if low <= fig_number <= high:
            return fig_number + offset
    raise ValueError(f"Unknown figure number: {fig_number}")

def unicode_to_glyph_name(codepoint: int) -> str:
    """Generate proper glyph name from Unicode"""
    if codepoint < 0x10000:
        return f"uni{codepoint:04X}"
    else:
        return f"u{codepoint:05X}"