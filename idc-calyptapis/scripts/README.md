# IDC Calyptapis Font Scripts

Tools for reviewing and rebuilding font glyphs.

## Glyph Review Tool

A web-based interface for visually reviewing font glyphs and recording design consistency assessments.

### Usage

```bash
cd scripts/
python3 review_server.py
```

Then open http://localhost:5000 in your browser.

### Features

- Displays all 47 glyphs across 6 weights (UltraLight, Light, Normal, SemiBold, Bold, Black)
- Click any glyph to open the review modal
- Thumbs up/down for design consistency assessment
- Optional comment field for notes
- Autosaves on sentiment selection and comment blur
- Visual indicators: green border for approved, red for issues
- Progress bar tracking overall review completion
- Keyboard shortcuts:
  - `1` or `↑` = thumbs up
  - `2` or `↓` = thumbs down
  - `←`/`→` = navigate glyphs
  - `Esc` = close modal

### Output

Reviews are saved to `glyph_reviews.json` with the structure:

```json
{
  "reviews": {
    "Weight/calyptapis-NNN.svg": {
      "weight": "Weight",
      "glyph": "calyptapis-NNN.svg",
      "sentiment": "up|down",
      "comment": "optional notes"
    }
  },
  "metadata": {
    "total_glyphs": 282,
    "reviewed_count": 282
  }
}
```

### Requirements

- Python 3.8+
- Flask (`pip install flask`)

---

## Glyph Rebuild Tool

Rebuilds specific glyphs across all weights without regenerating the entire font.

### Usage

```bash
cd scripts/

# Rebuild default glyphs (414 and 4008)
python3 rebuild_glyphs.py

# Rebuild specific glyphs
python3 rebuild_glyphs.py --glyphs 414 412

# Rebuild for specific weights only
python3 rebuild_glyphs.py --weights Normal Bold
```

### Weight Configuration

| Weight     | pen_height multiplier |
|------------|----------------------|
| UltraLight | 0.06                 |
| Light      | 0.09                 |
| Normal     | 0.12                 |
| SemiBold   | 0.15                 |
| Bold       | 0.18                 |
| Black      | 0.21                 |

### Adding New Glyphs

Edit `GLYPH_SOURCES` in `rebuild_glyphs.py` to map figure numbers to source files:

```python
GLYPH_SOURCES = {
    414: SRC_DIR / "letters" / "U10414.mp",
    4008: SRC_DIR / "letters" / "U1041c.mp",
    # Add more as needed
}
```

### Requirements

- Python 3.8+
- MetaPost (`mpost` command available in PATH)

---

## Files

- `review_server.py` - Flask server for glyph review interface
- `review_app.html` - Web interface for the review tool
- `rebuild_glyphs.py` - Script to rebuild specific glyphs across weights
- `glyph_reviews.json` - Saved review data from sentiment analysis
