#!/usr/bin/env python3
# extract_parameters.py

from pathlib import Path
from metapost_parser import (
    parse_font_directory,
    FontAnalyzer
)

def main():
    # Paths for your structure
    project_root = Path('calyptapis')
    main_file = project_root / 'src' / 'calyptapis.mp'
    letters_dir = project_root / 'src' / 'letters'
    output_dir = project_root / 'analysis'
    output_dir.mkdir(exist_ok=True)
    
    # Parse the font
    print("=" * 60)
    print("METAPOST Font Parameter Extraction")
    print("=" * 60)
    
    dataset = parse_font_directory(main_file, letters_dir)
    
    # Save complete dataset as JSON
    dataset_path = output_dir / 'calyptapis_dataset.json'
    print(f"\nSaving dataset to {dataset_path}")
    dataset.save_json(dataset_path)
    
    # Run analysis
    print("\nAnalyzing construction patterns...")
    analyzer = FontAnalyzer(dataset)
    
    analysis_path = output_dir / 'construction_patterns.json'
    print(f"Saving analysis to {analysis_path}")
    analyzer.export_summary(analysis_path)
    
    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Glyphs parsed: {len(dataset.glyphs)}")
    print(f"Pens defined: {len(dataset.global_params.pens)}")
    print(f"Global variables: {len(dataset.global_params.variables)}")
    
    patterns = analyzer.analyze_construction_patterns()
    print(f"\nPath types used:")
    for path_type, count in sorted(patterns['path_types'].items(), 
                                   key=lambda x: x[1], 
                                   reverse=True):
        print(f"  {path_type}: {count}")
    
    print(f"\nSymmetry usage:")
    for axis, count in patterns['symmetry_usage'].items():
        print(f"  {axis}: {count}")
    
    print(f"\nComplexity range: {min(patterns['complexity_distribution'])} - {max(patterns['complexity_distribution'])}")
    print(f"Average complexity: {sum(patterns['complexity_distribution']) / len(patterns['complexity_distribution']):.1f}")

if __name__ == '__main__':
    main()
