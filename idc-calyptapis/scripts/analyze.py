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
