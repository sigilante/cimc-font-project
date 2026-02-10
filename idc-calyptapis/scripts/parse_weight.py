@dataclass
class FontDataset:
    """Complete font data across all glyphs"""
    global_params: GlobalParameters
    glyphs: Dict[str, GlyphStructure] = field(default_factory=dict)
    
    def to_dict(self):
        return {
            'global_params': self.global_params.to_dict(),
            'glyphs': {
                codepoint: glyph.to_dict() 
                for codepoint, glyph in self.glyphs.items()
            }
        }
    
    def save_json(self, output_path: Path):
        """Export complete dataset to JSON"""
        with output_path.open('w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load_json(cls, input_path: Path) -> 'FontDataset':
        """Load dataset from JSON"""
        with input_path.open('r') as f:
            data = json.load(f)
        
        # Reconstruct (simplified - you'd want proper deserialization)
        dataset = cls(global_params=GlobalParameters())
        # ... reconstruction logic
        return dataset

def parse_font_directory(
    main_file: Path,
    letters_dir: Path
) -> FontDataset:
    """Parse complete font from directory structure"""
    
    print(f"Parsing global parameters from {main_file}")
    global_params = parse_global_parameters(main_file)
    
    dataset = FontDataset(global_params=global_params)
    
    print(f"Parsing glyph files from {letters_dir}")
    glyph_files = sorted(letters_dir.glob('U*.mp'))
    
    for glyph_file in glyph_files:
        print(f"  Parsing {glyph_file.name}...")
        glyph = parse_glyph_file(glyph_file)
        if glyph:
            dataset.glyphs[glyph.unicode_codepoint] = glyph
    
    print(f"\nParsed {len(dataset.glyphs)} glyphs")
    print(f"Found {len(global_params.pens)} pen definitions")
    
    return dataset
