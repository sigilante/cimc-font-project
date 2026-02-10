# metapost_parser.py

import re
import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any
from collections import defaultdict

@dataclass
class GlobalParameters:
    """Font-wide parameters from main .mp file"""
    # Geometric dimensions
    x_radius: Optional[float] = None
    y_radius: Optional[float] = None
    cap_height: Optional[float] = None
    x_height: Optional[float] = None
    em_width: Optional[float] = None
    
    # Pen definitions (store as strings, parse separately if needed)
    pens: Dict[str, str] = field(default_factory=dict)
    
    # Any other global variables
    variables: Dict[str, str] = field(default_factory=dict)
    
    # Raw content
    raw_header: str = ""
    
    def to_dict(self):
        return asdict(self)

def parse_global_parameters(main_file: Path) -> GlobalParameters:
    """Extract global parameters from main calyptapis.mp"""
    content = main_file.read_text()
    params = GlobalParameters(raw_header=content)
    
    # Find pen definitions: thin_pen = pencircle scaled X rotated Y;
    pen_pattern = r'(\w+_pen)\s*:?=\s*([^;]+);'
    for pen_name, definition in re.findall(pen_pattern, content):
        params.pens[pen_name] = definition.strip()
    
    # Find numeric variable assignments
    var_pattern = r'(\w+)\s*:=\s*([^;]+);'
    for var_name, value in re.findall(var_pattern, content):
        if var_name not in params.pens:  # Don't duplicate pens
            # Try to detect if it's a dimensional variable
            if any(dim in var_name for dim in ['radius', 'height', 'width', 'em']):
                try:
                    params.variables[var_name] = value.strip()
                    # Also set as attribute if it exists
                    if hasattr(params, var_name):
                        setattr(params, var_name, value.strip())
                except:
                    pass
    
    return params


@dataclass
class PathElement:
    """A named path or drawing element"""
    name: str
    path_type: str  # 'loop', 'serif', 'stem', etc.
    base_definition: str
    transformations: List[Dict[str, str]] = field(default_factory=list)
    pen_used: Optional[str] = None

    def to_dict(self):
        return asdict(self)

@dataclass
class GlyphStructure:
    """Complete structure of one glyph"""
    unicode_codepoint: str  # "U+1041A"
    unicode_name: str  # "DESERET CAPITAL LETTER JEE"
    fig_number: int
    filename: str  # Source file

    # Local variables defined in this glyph
    local_variables: Dict[str, str] = field(default_factory=dict)

    # Drawing elements
    paths: List[PathElement] = field(default_factory=list)
    draw_operations: List[str] = field(default_factory=list)
    pen_changes: List[Dict[str, Any]] = field(default_factory=list)

    # Structural properties
    uses_reflection: bool = False
    reflection_axis: Optional[str] = None
    complexity: int = 0  # Number of path elements

    # Raw code
    raw_code: str = ""

    def to_dict(self):
        result = asdict(self)
        result['paths'] = [p.to_dict() for p in self.paths]
        return result

def parse_glyph_file(filepath: Path) -> Optional[GlyphStructure]:
    """Parse a single letter file (e.g., U1041a.mp)"""
    if not filepath.exists():
        return None

    content = filepath.read_text()

    # Extract Unicode info from filename
    filename = filepath.stem  # "U1041a"
    unicode_codepoint = filename.upper()  # Normalize to uppercase

    # Find the beginfig block
    fig_match = re.search(
        r'beginfig\((\d+)\)\s*;(.*?)endfig;',
        content,
        re.DOTALL
    )

    if not fig_match:
        print(f"Warning: No beginfig found in {filepath}")
        return None

    fig_number = int(fig_match.group(1))
    block = fig_match.group(2)

    # Extract Unicode name from comment
    name_match = re.search(r'%\s*U\+\w+\s+(.+?)\s*\(', content)
    unicode_name = name_match.group(1) if name_match else "UNKNOWN"

    glyph = GlyphStructure(
        unicode_codepoint=unicode_codepoint,
        unicode_name=unicode_name,
        fig_number=fig_number,
        filename=str(filepath),
        raw_code=block
    )

    # Parse local variables
    for var_list in re.findall(r'^\s*numeric\s+([^;]+);', block, re.MULTILINE):
        # Handle "numeric x_diam, y_diam;"
        for var in var_list.split(','):
            glyph.local_variables[var.strip()] = "declared"

    for var_name, value in re.findall(r'^\s*(\w+)\s*:=\s*([^;]+);', block, re.MULTILINE):
        glyph.local_variables[var_name] = value.strip()

    # Parse path declarations
    path_names = re.findall(r'path\s+(\w+);', block)

    for path_name in path_names:
        # Find the definition
        path_def_pattern = rf'{path_name}\s*:=\s*(.+?);'
        path_matches = list(re.finditer(path_def_pattern, block, re.DOTALL))

        if not path_matches:
            continue

        # First definition
        base_definition = path_matches[0].group(1).strip()

        # Look for transformations (subsequent assignments)
        transformations = []
        for match in path_matches[1:]:
            transform_str = match.group(1)
            if path_name in transform_str:  # path := path scaled ...
                # Extract transformations
                for transform in parse_transformations(transform_str):
                    transformations.append(transform)

        # Classify path type
        path_type = classify_path_type(path_name, base_definition)

        glyph.paths.append(PathElement(
            name=path_name,
            path_type=path_type,
            base_definition=base_definition,
            transformations=transformations
        ))

    # Find pen changes
    for match in re.finditer(r'pickup\s+(\w+(?:_pen)?)', block):
        glyph.pen_changes.append({
            'pen': match.group(1)
        })

    # Find draw operations
    glyph.draw_operations = re.findall(r'draw\s+([^;]+);', block)

    # Check for reflection
    if 'reflectedabout' in block:
        glyph.uses_reflection = True
        reflection_match = re.search(
            r'reflectedabout\(\(([^)]+)\),\s*\(([^)]+)\)\)',
            block
        )
        if reflection_match:
            p1, p2 = reflection_match.groups()
            glyph.reflection_axis = classify_reflection_axis(p1, p2)

    glyph.complexity = len(glyph.paths)

    return glyph

def parse_transformations(transform_str: str) -> List[Dict[str, str]]:
    """Extract transformation operations from METAPOST code"""
    transforms = []

    # scaled (2/3) or scaled 0.5
    for scale in re.findall(r'scaled\s+\(([^)]+)\)', transform_str):
        transforms.append({'type': 'scaled', 'value': scale.strip()})
    for scale in re.findall(r'scaled\s+([^\s]+)', transform_str):
        if '(' not in scale:  # Avoid duplicating parenthesized version
            transforms.append({'type': 'scaled', 'value': scale.strip()})

    # shifted (x, y)
    for shift in re.findall(r'shifted\s+\(([^)]+)\)', transform_str):
        transforms.append({'type': 'shifted', 'value': shift.strip()})

    # rotated angle
    for angle in re.findall(r'rotated\s+([^\s;]+)', transform_str):
        transforms.append({'type': 'rotated', 'value': angle.strip()})

    return transforms

def classify_path_type(name: str, definition: str) -> str:
    """Infer semantic type from name and structure"""
    name_lower = name.lower()

    # Name-based classification
    type_keywords = {
        'loop': 'loop',
        'bowl': 'bowl',
        'serif': 'serif',
        'stem': 'stem',
        'stroke': 'stroke',
        'tail': 'tail',
        'arm': 'arm',
        'leg': 'leg',
        'bar': 'crossbar',
    }

    for keyword, path_type in type_keywords.items():
        if keyword in name_lower:
            return path_type

    # Structure-based classification
    if 'cycle' in definition:
        return 'closed_path'
    elif '..' in definition and not '--' in definition:
        return 'curved_path'
    elif '--' in definition:
        return 'straight_segment'

    return 'unknown'

def classify_reflection_axis(p1: str, p2: str) -> str:
    """Determine reflection axis from two points"""
    p1 = p1.strip()
    p2 = p2.strip()

    if p1 == '0,0' and p2 == '0,1':
        return 'vertical'
    elif p1 == '0,0' and p2 == '1,0':
        return 'horizontal'
    else:
        return f'custom({p1} to {p2})'


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


class FontAnalyzer:
    """Analyze patterns across the font"""

    def __init__(self, dataset: FontDataset):
        self.dataset = dataset

    def analyze_construction_patterns(self) -> Dict[str, Any]:
        """Find common construction strategies"""
        patterns = {
            'path_types': defaultdict(int),
            'transformation_usage': defaultdict(int),
            'pen_usage': defaultdict(int),
            'symmetry_usage': defaultdict(int),
            'complexity_distribution': [],
        }

        for glyph in self.dataset.glyphs.values():
            # Path types
            for path in glyph.paths:
                patterns['path_types'][path.path_type] += 1

                # Transformations
                for transform in path.transformations:
                    patterns['transformation_usage'][transform['type']] += 1

            # Pen usage
            for pen_change in glyph.pen_changes:
                patterns['pen_usage'][pen_change['pen']] += 1

            # Symmetry
            if glyph.uses_reflection:
                patterns['symmetry_usage'][glyph.reflection_axis] += 1

            # Complexity
            patterns['complexity_distribution'].append(glyph.complexity)

        return dict(patterns)

    def find_common_transformations(self) -> Dict[str, List[str]]:
        """Which transformation values appear most often?"""
        transform_values = defaultdict(list)

        for glyph in self.dataset.glyphs.values():
            for path in glyph.paths:
                for transform in path.transformations:
                    key = transform['type']
                    value = transform['value']
                    transform_values[key].append(value)

        # Find most common values for each transform type
        common = {}
        for transform_type, values in transform_values.items():
            from collections import Counter
            common[transform_type] = Counter(values).most_common(10)

        return common

    def export_summary(self, output_path: Path):
        """Export analysis summary"""
        analysis = {
            'total_glyphs': len(self.dataset.glyphs),
            'construction_patterns': self.analyze_construction_patterns(),
            'common_transformations': self.find_common_transformations(),
        }

        with output_path.open('w') as f:
            json.dump(analysis, f, indent=2)
