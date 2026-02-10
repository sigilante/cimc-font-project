#!/usr/bin/env python3
# optimize_metapost.py

import cv2
import numpy as np
from pathlib import Path
import subprocess
import tempfile
import json
import re
from scipy.optimize import minimize, differential_evolution
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class Parameter:
    """A single optimizable parameter."""
    name: str           # e.g., "x_a_2"
    value: float        # Current value
    min_val: float      # Search bounds
    max_val: float
    optimizable: bool   # Can this be changed?

class MetapostOptimizer:
    """
    Optimize parameterized METAPOST to match specimen.
    
    Uses human-provided structure but refines free parameters.
    """
    
    def __init__(self, 
                 metapost_template: Path,
                 metadata_file: Path,
                 specimen_path: Path,
                 output_dir: Path):
        self.template_path = metapost_template
        self.metadata_path = metadata_file
        self.specimen_path = specimen_path
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True, parents=True)
        
        # Load template
        self.template = metapost_template.read_text()
        
        # Load metadata
        with open(metadata_file) as f:
            self.metadata = json.load(f)
        
        # Load specimen
        self.target_image = self.load_specimen(specimen_path)
        
        # Extract parameters from metadata
        self.parameters = self.extract_parameters()
        
        print(f"Loaded {len(self.parameters)} parameters")
        free_params = [p for p in self.parameters if p.optimizable]
        print(f"  {len(free_params)} are free to optimize")
        print(f"  {len(self.parameters) - len(free_params)} are fixed")
    
    def load_specimen(self, image_path: Path) -> np.ndarray:
        """Load and preprocess specimen."""
        img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
        
        if np.mean(img) < 127:
            img = 255 - img
        
        _, binary = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)
        
        return binary
    
    def extract_parameters(self) -> List[Parameter]:
        """Extract hierarchical parameters from metadata."""
        parameters = []
        
        # Global parameters
        for param in self.metadata['hierarchy']['global']:
            parameters.append(Parameter(
                name=param['name'],
                value=param['value'],
                min_val=param['min'],
                max_val=param['max'],
                optimizable=True
            ))
        
        # Point base coordinates
        for point_data in self.metadata['hierarchy']['points']:
            # X base coordinate
            x_info = point_data['x_base']
            x_name = x_info['name']
            x_value = self.get_current_value(x_name)
            range_frac = x_info.get('range_fraction', 0.15)
            
            parameters.append(Parameter(
                name=x_name,
                value=x_value,
                min_val=x_value * (1 - range_frac),
                max_val=x_value * (1 + range_frac),
                optimizable=x_info['optimizable']
            ))
            
            # Y base coordinate  
            y_info = point_data['y_base']
            y_name = y_info['name']
            y_value = self.get_current_value(y_name)
            
            parameters.append(Parameter(
                name=y_name,
                value=y_value,
                min_val=y_value * (1 - range_frac),
                max_val=y_value * (1 + range_frac),
                optimizable=y_info['optimizable']
            ))
        
        return parameters
    
    def get_current_value(self, param_name: str) -> float:
        """Extract current value from template."""
        pattern = rf'{param_name}\s*:=\s*([\d.-]+)\s*;'
        match = re.search(pattern, self.template)
        if match:
            return float(match.group(1))
        return 0.0
    
    def substitute_parameters(self, param_values: Dict[str, float]) -> str:
        """Substitute parameter values into template."""
        result = self.template
        
        for name, value in param_values.items():
            pattern = rf'({name}\s*:=\s*)[\d.-]+(\s*;)'
            replacement = rf'\g<1>{value:.6f}\g<2>'
            result = re.sub(pattern, replacement, result)
        
        return result
    
    def render_metapost(self, param_values: Dict[str, float]) -> np.ndarray:
        """Render METAPOST with given parameters."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            # Generate code with substituted values
            mp_code = self.substitute_parameters(param_values)
            
            # Write to file
            mp_file = tmpdir / "temp.mp"
            mp_file.write_text(mp_code)
            
            # DEBUG: Save failing code
            debug_file = self.output_dir / "debug_last_attempt.mp"
            debug_file.write_text(mp_code)
            
            # Run mpost
            try:
                result = subprocess.run(
                    ['mpost', str(mp_file)],
                    cwd=tmpdir,
                    capture_output=True,
                    timeout=10
                )
                
                if result.returncode != 0:
                    # Save failed code
                    fail_file = self.output_dir / "debug_failed.mp"
                    fail_file.write_text(mp_code)
                    print(f"  METAPOST failed. Saved to: {fail_file}")
                    print(f"  stderr: {result.stderr.decode()[:200]}")
                    return None
                
                # Find SVG
                svg_files = list(tmpdir.glob('*.svg'))
                if not svg_files:
                    print("  No SVG generated")
                    return None
                
                # Rasterize
                binary = self.rasterize_svg(svg_files[0])
                return binary
                
            except subprocess.TimeoutExpired:
                # Save timeout code
                timeout_file = self.output_dir / "debug_timeout.mp"
                timeout_file.write_text(mp_code)
                print(f"  METAPOST timeout. Saved to: {timeout_file}")
                return None
            except Exception as e:
                print(f"  Render error: {e}")
                return None
    
    def validate_template(self):
        """Test that the initial template renders correctly."""
        print("\nValidating template...")
        
        # Use initial parameter values
        param_dict = {p.name: p.value for p in self.parameters}
        
        rendered = self.render_metapost(param_dict)
        
        if rendered is None:
            print("ERROR: Initial template does not render!")
            print("Check generated_path_parameterized.mp manually")
            return False
        
        print("✓ Template validates successfully")
        
        # Show initial error
        error = self.compare_images(rendered, self.target_image)
        print(f"Initial error: {error:.4f}")
        
        # Save initial render
        cv2.imwrite(str(self.output_dir / "initial_render.png"), rendered)
        print(f"Saved initial render to: {self.output_dir / 'initial_render.png'}")
        
        return True

    def rasterize_svg(self, svg_path: Path, size: int = 500) -> np.ndarray:
        """Convert SVG to binary image."""
        png_path = svg_path.with_suffix('.png')
        
        try:
            # Try ImageMagick
            subprocess.run([
                'convert',
                '-density', '300',
                '-background', 'white',
                '-flatten',
                str(svg_path),
                str(png_path)
            ], check=True, capture_output=True, timeout=5)
            
        except:
            # Try Inkscape
            try:
                subprocess.run([
                    'inkscape',
                    str(svg_path),
                    '--export-type=png',
                    f'--export-filename={png_path}',
                    '--export-width=500',
                    '--export-height=500'
                ], check=True, capture_output=True, timeout=5)
            except:
                return None
        
        # Load and process
        img = cv2.imread(str(png_path), cv2.IMREAD_GRAYSCALE)
        if img is None:
            return None
        
        img = cv2.resize(img, (size, size))
        _, binary = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)
        
        return binary
    
    def compare_images(self, rendered: np.ndarray, target: np.ndarray) -> float:
        """Compare rendered to target. Lower is better."""
        if rendered is None:
            return 10.0
        
        # Resize to match
        if rendered.shape != target.shape:
            rendered = cv2.resize(rendered, (target.shape[1], target.shape[0]))
        
        # Pixel overlap
        intersection = np.sum((rendered > 0) & (target > 0))
        union = np.sum((rendered > 0) | (target > 0))
        
        if union == 0:
            return 1.0
        
        iou = intersection / union
        return 1.0 - iou
    
    def objective_function(self, param_array: np.ndarray) -> float:
        """Objective function for optimization."""
        # Map array to parameter dict
        param_dict = {}
        free_params = [p for p in self.parameters if p.optimizable]
        
        for i, param in enumerate(free_params):
            param_dict[param.name] = param_array[i]
        
        # Also include fixed parameters
        for param in self.parameters:
            if not param.optimizable:
                param_dict[param.name] = param.value
        
        # Render
        rendered = self.render_metapost(param_dict)
        
        # Compare
        error = self.compare_images(rendered, self.target_image)
        
        print(f"  Error: {error:.4f}")
        
        return error
    
    def optimize(self, method='nelder-mead', max_iter=50):
        """Run optimization."""
        free_params = [p for p in self.parameters if p.optimizable]
        
        print(f"\nOptimizing {len(free_params)} free parameters...")
        print("=" * 60)
        
        # Initial values
        x0 = np.array([p.value for p in free_params])
        
        # Bounds
        bounds = [(p.min_val, p.max_val) for p in free_params]
        
        if method == 'nelder-mead':
            # Local optimization
            result = minimize(
                self.objective_function,
                x0,
                method='Nelder-Mead',
                options={'maxiter': max_iter, 'disp': True}
            )
            best_params = result.x
            
        elif method == 'differential_evolution':
            # Global optimization
            result = differential_evolution(
                self.objective_function,
                bounds,
                maxiter=20,
                popsize=5,
                workers=1,
                disp=True
            )
            best_params = result.x
        
        # Map back to dict
        optimized = {}
        for i, param in enumerate(free_params):
            optimized[param.name] = best_params[i]
        
        # Include fixed params
        for param in self.parameters:
            if not param.optimizable:
                optimized[param.name] = param.value
        
        print("\n" + "=" * 60)
        print("OPTIMIZATION COMPLETE")
        print(f"Final error: {result.fun:.4f}")
        print("=" * 60)
        
        return optimized
    
    def save_optimized(self, optimized_params: Dict[str, float]):
        """Save optimized METAPOST."""
        optimized_code = self.substitute_parameters(optimized_params)
        
        output_file = self.output_dir / "optimized.mp"
        output_file.write_text(optimized_code)
        
        print(f"\nSaved optimized METAPOST: {output_file}")
        
        # Render comparison
        rendered = self.render_metapost(optimized_params)
        if rendered is not None:
            self.save_comparison(rendered)
    
    def save_comparison(self, rendered: np.ndarray):
        """Save side-by-side comparison."""
        import matplotlib.pyplot as plt
        
        if rendered.shape != self.target_image.shape:
            rendered = cv2.resize(rendered, (self.target_image.shape[1], self.target_image.shape[0]))
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        
        ax1.imshow(self.target_image, cmap='gray')
        ax1.set_title('Target Specimen')
        ax1.axis('off')
        
        ax2.imshow(rendered, cmap='gray')
        ax2.set_title('Optimized Result')
        ax2.axis('off')
        
        plt.tight_layout()
        
        output_path = self.output_dir / "comparison.png"
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        
        print(f"Saved comparison: {output_path}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Optimize parameterized METAPOST')
    parser.add_argument('specimen', type=Path, help='Target specimen image')
    parser.add_argument('--template', type=Path, default=Path('generated_path_parameterized.mp'),
                       help='Parameterized METAPOST template')
    parser.add_argument('--metadata', type=Path, default=Path('optimizer_metadata.json'),
                       help='Parameter metadata JSON')
    parser.add_argument('--output', type=Path, default=Path('optimized_output'),
                       help='Output directory')
    parser.add_argument('--method', choices=['nelder-mead', 'differential_evolution'],
                       default='nelder-mead', help='Optimization method')
    parser.add_argument('--max-iter', type=int, default=50, help='Maximum iterations')
    
    args = parser.parse_args()
    
    optimizer = MetapostOptimizer(
        metapost_template=args.template,
        metadata_file=args.metadata,
        specimen_path=args.specimen,
        output_dir=args.output
    )

    if not optimizer.validate_template():
        print("\nFix the template before optimizing!")
        return
    
    optimized = optimizer.optimize(method=args.method, max_iter=args.max_iter)
    optimizer.save_optimized(optimized)

if __name__ == '__main__':
    main()
