#!/usr/bin/env python3
# build_otf.py

import fontforge
import os
from pathlib import Path
from unicode_mapping import fig_to_unicode, unicode_to_glyph_name
import psMat
import re
from pathlib import Path

class FontBuilder:
    """Build OTF fonts from SVG glyphs"""
    
    def __init__(self, font_name: str, weight: str):
        self.font_name = font_name
        self.weight = weight
        self.font = fontforge.font()
        
        # Set font metadata
        self.font.familyname = font_name
        self.font.fontname = f"{font_name}-{weight}"
        self.font.fullname = f"{font_name} {weight}"
        self.font.weight = weight
        
        # Set design metrics
        self.font.em = 1000  # Standard em-square size
        self.font.ascent = 800
        self.font.descent = 200
        
        # Encoding
        self.font.encoding = 'UnicodeFull'
        
    def get_target_height(self, codepoint: int) -> float:
        """Determine appropriate height target based on glyph type"""
        
        # Deseret capitals (U+10400-U+10427)
        if 0x10400 <= codepoint <= 0x10427:
            return 1000  # Full height
        
        # Latin capitals (A-Z)
        if 0x0041 <= codepoint <= 0x005A:
            return 1000  # Full height
        
        # Punctuation marks
        if codepoint in [0x002E, 0x002C, 0x003A, 0x003B]:  # . , : ;
            return 200  # Small
        
        if codepoint in [0x0021, 0x003F]:  # ! ?
            return 800  # Tall but not full
        
        if codepoint in [0x0027, 0x0022]:  # ' "
            return 400  # Mid-height
        
        # Brackets, parentheses
        if codepoint in [0x0028, 0x0029, 0x005B, 0x005D, 0x007B, 0x007D]:
            return 1000  # Full height
        
        # Default: scale to fill but with sanity checks
        return 1000

    def should_scale_glyph(self, original_height: float, target_height: float) -> bool:
        """Decide if this glyph needs scaling"""
        
        # If glyph is already close to target, don't scale
        ratio = original_height / target_height
        if 0.8 <= ratio <= 1.2:
            return False
        
        # If glyph is way too small (< 50% of target), definitely scale
        if ratio < 0.5:
            return True
        
        # If glyph is way too big (> 150% of target), scale down
        if ratio > 1.5:
            return True
        
        return False

    def import_svg_glyph(self, svg_path: Path, fig_number: int):
        """Import with em-square normalization"""
        try:
            codepoint = fig_to_unicode(fig_number)
            glyph_name = unicode_to_glyph_name(codepoint)
            glyph = self.font.createChar(codepoint, glyph_name)
            
            # Import
            glyph.importOutlines(str(svg_path))
            
            # Get bounding box
            bbox = glyph.boundingBox()
            if bbox[2] == bbox[0] or bbox[3] == bbox[1]:
                # Empty glyph
                print(f"  WARNING: {glyph_name} is empty!")
                return
            
            original_width = bbox[2] - bbox[0]
            original_height = bbox[3] - bbox[1]
            
            # TARGET: Normalize to use full em-square height
            # Most glyphs should span from -200 (descent) to 800 (ascent) = 1000 units
            target_height = self.font.em  # 1000
            
            # Decide if we need to scale
            if self.should_scale_glyph(original_height, target_height):
                scale_factor = target_height / original_height
                
                import psMat
                transform = psMat.scale(scale_factor)
                glyph.transform(transform)
                
                scaled_bbox = glyph.boundingBox()
                
                # Vertical alignment based on glyph type
                if codepoint in [0x002E, 0x002C]:  # Period, comma - sit on baseline
                    target_bottom = -50
                elif codepoint in [0x0027, 0x0022]:  # Quotes - float high
                    target_bottom = 400
                else:  # Default - centered in ascent
                    target_bottom = -200
                
                current_bottom = scaled_bbox[1]
                if abs(current_bottom - target_bottom) > 10:
                    vertical_shift = target_bottom - current_bottom
                    shift_transform = psMat.translate(0, vertical_shift)
                    glyph.transform(shift_transform)
                
                print(f"  {glyph_name}: {original_width:.0f}x{original_height:.0f} "
                    f"→ target={target_height:.0f} scale={scale_factor:.3f}")
            else:
                print(f"  {glyph_name}: {original_width:.0f}x{original_height:.0f} "
                    f"→ no scaling needed")

            # Process paths
            glyph.removeOverlap()
            glyph.simplify()
            glyph.round()
            
            # Set advance width
            final_bbox = glyph.boundingBox()
            glyph_width = final_bbox[2] - final_bbox[0]
            
            # Sidebearings - smaller for punctuation
            if codepoint in [0x002E, 0x002C, 0x003A, 0x003B]:
                sidebearing = 100  # More space around punctuation
            else:
                sidebearing = 50
            
            glyph.left_side_bearing = sidebearing
            glyph.right_side_bearing = sidebearing
            glyph.width = int(glyph_width + 2 * sidebearing)

        except Exception as e:
            print(f"  ERROR importing {svg_path.name}: {e}")
            import traceback
            traceback.print_exc()

    def clean_svg_colors(self, svg_path: Path):
        """Fix RGB color format in-place"""
        content = svg_path.read_text()
        
        # Replace percentage RGB with integer RGB (all black = 0,0,0)
        fixed = re.sub(
            r'rgb\([\d.]+%\s*,\s*[\d.]+%\s*,\s*[\d.]+%\)',
            'rgb(0,0,0)',
            content
        )

        if fixed != content:
            svg_path.write_text(fixed)

    def import_directory(self, svg_dir: Path):
        """Import all SVG files from a directory"""
        print(f"\nImporting glyphs from {svg_dir}")
        
        # Find all SVG files
        svg_files = sorted(svg_dir.glob('calyptapis-*.svg'))

        # Clean them ONCE before importing
        print(f"Cleaning {len(svg_files)} SVG files...")
        for svg_file in svg_files:
            self.clean_svg_colors(svg_file)        

        for svg_file in svg_files:
            # Extract figure number from filename
            # calyptapis-4000.svg → 4000
            stem = svg_file.stem  # "calyptapis-4000"
            fig_str = stem.split('-')[1]  # "4000"
            fig_number = int(fig_str)
            
            self.import_svg_glyph(svg_file, fig_number)
        
        print(f"Imported {len(svg_files)} glyphs")
    
    def set_metadata(self, version: str = "1.0", copyright_text: str = ""):
        """Set additional font metadata"""
        self.font.version = version
        self.font.copyright = copyright_text
        
        # OS/2 table settings
        self.font.os2_vendor = "ILDC"  # Your vendor ID
        
        # Weight class mapping
        weight_classes = {
            'UltraLight': 100,
            'Light': 300,
            'Normal': 400,
            'SemiBold': 600,
            'Bold': 700,
            'Black': 900
        }
        self.font.os2_weight = weight_classes.get(self.weight, 400)
    
    def auto_hint(self):
        """Apply automatic hinting"""
        print("\nAuto-hinting...")
        self.font.selection.all()
        self.font.autoHint()
    
    def generate_otf(self, output_path: Path):
        """Generate OpenType font file"""
        print(f"\nGenerating {output_path}")
        
        # Generate with options
        self.font.generate(
            str(output_path),
            flags=(
                'opentype',  # Generate OpenType
                'round',     # Round coordinates to integers
            )
        )
        
        print(f"✓ Generated {output_path}")
    
    def close(self):
        """Clean up"""
        self.font.close()

def build_weight(
    weight_name: str,
    svg_dir: Path,
    output_dir: Path,
    font_name: str = "Calyptapis"
):
    """Build one weight of the font"""
    print("=" * 60)
    print(f"Building {font_name} {weight_name}")
    print("=" * 60)
    
    builder = FontBuilder(font_name, weight_name)
    
    # Import all SVG glyphs
    builder.import_directory(svg_dir)
    
    # Set metadata
    builder.set_metadata(
        version="1.0",
        copyright_text="ⓒ 2024–2026 N. E. Davis for Illinois Deseret Consortium.  Made available under the SIL Open Font License 1.1.  “IDC Calyptapis” is a reserved font name under this license, but “Calyptapis” is not reserved."
    )
    
    # Auto-hint
    builder.auto_hint()
    
    # Generate OTF
    output_path = output_dir / f"{font_name}-{weight_name}.otf"
    builder.generate_otf(output_path)
    
    builder.close()
    
    return output_path

def fix_svg_colors(svg_dir: Path):
    """Fix all SVG color specs in directory"""
    for svg_file in svg_dir.rglob("*.svg"):
        content = svg_file.read_text()
        
        # Replace percentage RGB with integer RGB
        fixed = re.sub(
            r'rgb\((\d+\.\d+)%,\s*(\d+\.\d+)%,\s*(\d+\.\d+)%\)',
            'rgb(0,0,0)',  # Since they're all black anyway
            content
        )
        
        if fixed != content:
            svg_file.write_text(fixed)
            print(f"Fixed {svg_file}")

def main():
    """Build all weights"""
    project_root = Path('calyptapis')
    maj_dir = project_root / 'maj'
    output_dir = project_root / 'fonts'
    output_dir.mkdir(exist_ok=True)
    
    weights = ['UltraLight', 'Light', 'Normal', 'SemiBold', 'Bold', 'Black']
    
    generated_fonts = []
    
    for weight in weights:
        svg_dir = maj_dir / weight
        if svg_dir.exists():
            try:
                output_path = build_weight(weight, svg_dir, output_dir)
                generated_fonts.append(output_path)
            except Exception as e:
                print(f"\n✗ FAILED to build {weight}: {e}")
                import traceback
                traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("BUILD COMPLETE")
    print("=" * 60)
    print(f"Generated {len(generated_fonts)} font files:")
    for font_path in generated_fonts:
        print(f"  {font_path}")
    fix_svg_colors(Path('calyptapis/maj'))

if __name__ == '__main__':
    main()