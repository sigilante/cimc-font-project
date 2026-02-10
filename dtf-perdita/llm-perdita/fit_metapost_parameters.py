#!/usr/bin/env python3
# fit_metapost_parameters.py

import cv2
import numpy as np
from pathlib import Path
import subprocess
import tempfile
import shutil
from scipy.optimize import minimize, differential_evolution
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Dict, Tuple, Optional

@dataclass
class ParameterBounds:
    """Bounds for a single parameter."""
    name: str
    min_val: float
    max_val: float
    initial: float

class MetapostOptimizer:
    """Optimize METAPOST parameters to match specimen image."""
    
    def __init__(self, 
                 template_path: Path,
                 base_path: Path,
                 specimen_path: Path,
                 output_dir: Path):
        self.template_path = template_path
        self.base_path = base_path
        self.specimen_path = specimen_path
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True, parents=True)
        
        # Load and process specimen
        print(f"Loading specimen: {specimen_path}")
        self.target_image = self.load_specimen(specimen_path)
        self.target_features = self.extract_features(self.target_image)
        
        print(f"Target features:")
        for key, val in self.target_features.items():
            print(f"  {key}: {val:.2f}")
    
    def load_specimen(self, image_path: Path) -> np.ndarray:
        """Load and preprocess specimen image."""
        img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
        
        # Invert if needed
        if np.mean(img) < 127:
            img = 255 - img
        
        # Threshold to binary
        _, binary = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)
        
        return binary
    
    def extract_features(self, binary_image: np.ndarray) -> Dict[str, float]:
        """
        Extract geometric features from binary image.
        These will be used for comparison.
        """
        # Find all foreground pixels
        points = np.argwhere(binary_image > 0)
        
        if len(points) == 0:
            return {}
        
        y_coords = points[:, 0]
        x_coords = points[:, 1]
        
        # Basic bounding box
        x_min, x_max = x_coords.min(), x_coords.max()
        y_min, y_max = y_coords.min(), y_coords.max()
        
        width = x_max - x_min
        height = y_max - y_min
        
        # Moments for centroid and shape
        moments = cv2.moments(binary_image)
        
        if moments['m00'] == 0:
            cx, cy = width / 2, height / 2
        else:
            cx = moments['m10'] / moments['m00']
            cy = moments['m01'] / moments['m00']
        
        # Find contours for more detailed analysis
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Largest contour (main stroke)
        if contours:
            main_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(main_contour)
            perimeter = cv2.arcLength(main_contour, True)
            
            # Circularity (4π*area/perimeter²)
            if perimeter > 0:
                circularity = 4 * np.pi * area / (perimeter ** 2)
            else:
                circularity = 0
        else:
            area = 0
            perimeter = 0
            circularity = 0
        
        return {
            'width': float(width),
            'height': float(height),
            'aspect_ratio': float(height / width if width > 0 else 1),
            'center_x': float(cx),
            'center_y': float(cy),
            'area': float(area),
            'perimeter': float(perimeter),
            'circularity': float(circularity),
            'x_min': float(x_min),
            'y_min': float(y_min),
            'x_max': float(x_max),
            'y_max': float(y_max),
        }
    
    def render_metapost(self, parameters: Dict[str, float]) -> Optional[np.ndarray]:
        """Render METAPOST with given parameters to binary image."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            
            # Read template
            template_content = self.template_path.read_text()
            
            # Substitute parameters
            mp_code = self.substitute_parameters(template_content, parameters)
            
            # Write complete METAPOST file
            mp_file = tmpdir / "test.mp"
            
            # Copy base file to temp directory (easier than absolute paths)
            base_copy = tmpdir / "perdita_base.mp"
            shutil.copy(self.base_path, base_copy)
            
            # Include base file with simple relative path
            full_code = 'input perdita_base.mp;\n\n' + mp_code
            mp_file.write_text(full_code)
            
            # DEBUG: Print generated code
            print("\n" + "=" * 60)
            print("GENERATED METAPOST CODE:")
            print("=" * 60)
            print(full_code)
            print("=" * 60)
            
            # Run mpost with shorter timeout to fail fast
            try:
                result = subprocess.run(
                    ['mpost', str(mp_file)],
                    cwd=tmpdir,
                    capture_output=True,
                    timeout=5  # Reduced from 10
                )
                
                # DEBUG: Show output
                if result.stdout:
                    print("MPOST stdout:", result.stdout.decode())
                if result.stderr:
                    print("MPOST stderr:", result.stderr.decode())
                
                if result.returncode != 0:
                    print(f"METAPOST error (return code {result.returncode})")
                    # Save failed code for inspection
                    failed_file = self.output_dir / "failed_code.mp"
                    failed_file.write_text(full_code)
                    print(f"Saved failed code to: {failed_file}")
                    return None
                
                # Find generated SVG
                svg_files = list(tmpdir.glob('*.svg'))
                if not svg_files:
                    print("No SVG generated")
                    # List all files that were created
                    all_files = list(tmpdir.glob('*'))
                    print(f"Files in tmpdir: {[f.name for f in all_files]}")
                    return None
                
                svg_file = svg_files[0]
                
                # Rasterize SVG to image
                binary = self.rasterize_svg(svg_file)
                
                return binary
                
            except subprocess.TimeoutExpired:
                print("METAPOST timeout - code has infinite loop or error")
                # Save the code that timed out
                timeout_file = self.output_dir / "timeout_code.mp"
                timeout_file.write_text(full_code)
                print(f"Saved timeout code to: {timeout_file}")
                return None
            except Exception as e:
                print(f"Rendering error: {e}")
                import traceback
                traceback.print_exc()
                return None
    
    def substitute_parameters(self, template: str, parameters: Dict[str, float]) -> str:
        """
        Substitute parameter values into template.
        Handles both = and := assignments.
        """
        import re
        
        result = template
        
        for param_name, value in parameters.items():
            # Pattern 1: Simple assignment with = (like x_scale = 36;)
            pattern1 = rf'(\s*{param_name}\s*=\s*)[\d.]+(\s*;)'
            replacement1 = rf'\g<1>{value:.6f}\g<2>'
            result = re.sub(pattern1, replacement1, result, flags=re.MULTILINE)
            
            # Pattern 2: METAPOST assignment with := (like pen_start := 12;)
            pattern2 = rf'(\s*{param_name}\s*:=\s*)[\d.]+(\s*;)'
            replacement2 = rf'\g<1>{value:.6f}\g<2>'
            result = re.sub(pattern2, replacement2, result, flags=re.MULTILINE)
        
        return result
    
    def rasterize_svg(self, svg_path: Path, size=500) -> np.ndarray:
        """
        Convert SVG to binary raster image.
        """
        # Use ImageMagick or cairosvg for rasterization
        # For now, simple approach with subprocess
        
        png_path = svg_path.with_suffix('.png')
        
        try:
            # Try ImageMagick convert
            subprocess.run([
                'convert',
                '-density', '300',
                '-background', 'white',
                '-flatten',
                str(svg_path),
                str(png_path)
            ], check=True, capture_output=True)
            
            # Load PNG
            img = cv2.imread(str(png_path), cv2.IMREAD_GRAYSCALE)
            
            # Resize to consistent size
            img = cv2.resize(img, (size, size))
            
            # Threshold
            _, binary = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)
            
            return binary
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Fallback: try inkscape
            try:
                subprocess.run([
                    'inkscape',
                    str(svg_path),
                    '--export-type=png',
                    f'--export-filename={png_path}',
                    '--export-width=500',
                    '--export-height=500'
                ], check=True, capture_output=True)
                
                img = cv2.imread(str(png_path), cv2.IMREAD_GRAYSCALE)
                _, binary = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)
                return binary
                
            except:
                print("Could not rasterize SVG (need ImageMagick or Inkscape)")
                return None
    
    def compare_images(self, rendered: np.ndarray, target: np.ndarray) -> float:
        """
        Compute similarity score between rendered and target.
        Lower is better (minimization).
        """
        # Resize to same dimensions
        if rendered.shape != target.shape:
            rendered = cv2.resize(rendered, (target.shape[1], target.shape[0]))
        
        # Simple pixel overlap metric
        intersection = np.sum((rendered > 0) & (target > 0))
        union = np.sum((rendered > 0) | (target > 0))
        
        if union == 0:
            return 1.0
        
        # IoU-based distance
        iou = intersection / union
        distance = 1.0 - iou
        
        # Also compare features
        rendered_features = self.extract_features(rendered)
        feature_distance = self.compare_features(rendered_features, self.target_features)
        
        # Weighted combination
        total_distance = 0.5 * distance + 0.5 * feature_distance
        
        return total_distance
    
    def compare_features(self, features1: Dict, features2: Dict) -> float:
        """Compare extracted features."""
        if not features1 or not features2:
            return 1.0
        
        # Normalize and compare key features
        distance = 0.0
        weights = {
            'aspect_ratio': 0.3,
            'circularity': 0.2,
            'width': 0.15,
            'height': 0.15,
            'area': 0.2,
        }
        
        for key, weight in weights.items():
            if key in features1 and key in features2:
                v1 = features1[key]
                v2 = features2[key]
                
                # Normalize by target value
                if v2 > 0:
                    diff = abs(v1 - v2) / v2
                else:
                    diff = 0 if v1 == 0 else 1
                
                distance += weight * min(diff, 1.0)  # Cap at 1.0
        
        return distance
    
    def objective_function(self, param_values: np.ndarray, param_bounds: list) -> float:
        """
        Objective function for optimization.
        Takes parameter values array, returns error (to minimize).
        """
        # Convert array to parameter dict
        parameters = {}
        for i, bound in enumerate(param_bounds):
            parameters[bound.name] = param_values[i]
        
        # Render with these parameters
        rendered = self.render_metapost(parameters)
        
        if rendered is None:
            return 10.0  # Large penalty for rendering failure
        
        # Compare to target
        error = self.compare_images(rendered, self.target_image)
        
        print(f"  Params: {param_values} → Error: {error:.4f}")
        
        return error
    
    def optimize(self, param_bounds: list, method='differential_evolution') -> Dict[str, float]:
        """
        Run optimization to find best parameters.
        
        Args:
            param_bounds: List of ParameterBounds objects
            method: 'differential_evolution' or 'nelder-mead'
        """
        print(f"\nOptimizing {len(param_bounds)} parameters...")
        print("=" * 60)
        
        if method == 'differential_evolution':
            # Global optimization - good for finding rough optimum
            bounds = [(b.min_val, b.max_val) for b in param_bounds]
            
            result = differential_evolution(
                lambda x: self.objective_function(x, param_bounds),
                bounds,
                maxiter=20,  # Increase for better results
                popsize=5,
                workers=1,  # Parallel if your system supports
                disp=True
            )
            
            best_params = result.x
            
        else:  # nelder-mead
            # Local optimization - fast but needs good initial guess
            x0 = np.array([b.initial for b in param_bounds])
            
            result = minimize(
                lambda x: self.objective_function(x, param_bounds),
                x0,
                method='Nelder-Mead',
                options={'maxiter': 50, 'disp': True}
            )
            
            best_params = result.x
        
        # Convert to dict
        optimized = {}
        for i, bound in enumerate(param_bounds):
            optimized[bound.name] = best_params[i]
        
        print("\n" + "=" * 60)
        print("OPTIMIZATION COMPLETE")
        print("=" * 60)
        print(f"Final error: {result.fun:.4f}")
        print("\nOptimized parameters:")
        for name, value in optimized.items():
            print(f"  {name}: {value:.4f}")
        
        return optimized
    
    def generate_final_metapost(self, optimized_params: Dict[str, float]) -> str:
        """Generate final METAPOST file with optimized parameters."""
        template = self.template_path.read_text()
        return self.substitute_parameters(template, optimized_params)
    
    def save_comparison(self, optimized_params: Dict[str, float], output_path: Path):
        """
        Render optimized version and save side-by-side comparison.
        """
        rendered = self.render_metapost(optimized_params)
        
        if rendered is None:
            print("Could not render final comparison")
            return
        
        # Resize to match
        if rendered.shape != self.target_image.shape:
            rendered = cv2.resize(rendered, (self.target_image.shape[1], self.target_image.shape[0]))
        
        # Create side-by-side comparison
        comparison = np.hstack([self.target_image, rendered])
        
        # Add labels
        import matplotlib.pyplot as plt
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        
        ax1.imshow(self.target_image, cmap='gray')
        ax1.set_title('Target Specimen')
        ax1.axis('off')
        
        ax2.imshow(rendered, cmap='gray')
        ax2.set_title('Optimized METAPOST')
        ax2.axis('off')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"Saved comparison: {output_path}")


import re

# Updated parameter bounds
def main():
    """Main optimization workflow."""
    
    # Paths
    base_dir = Path('.')
    specimen_path = base_dir / 'design' / 'U10400.png'
    template_path = base_dir / 'perdita_templates' / 'U10400.mp'
    base_path = base_dir / 'perdita_templates' / 'perdita_base.mp'
    output_dir = base_dir / 'optimized_output'
    
    # Check files exist
    for p in [specimen_path, template_path, base_path]:
        if not p.exists():
            print(f"ERROR: File not found: {p}")
            return
    
    # Initialize optimizer
    optimizer = MetapostOptimizer(
        template_path=template_path,
        base_path=base_path,
        specimen_path=specimen_path,
        output_dir=output_dir
    )
    
    # Define parameters to optimize
    param_bounds = [
        # Overall scale
        ParameterBounds('x_scale', 25, 50, 36),
        ParameterBounds('y_scale', 60, 90, 72),
        
        # Left y position coefficient
        ParameterBounds('left_y_coeff', 0.3, 0.7, 0.5),
        
        # Pen sizes
        ParameterBounds('pen_start', 8, 18, 12),
        ParameterBounds('pen_loop', 6, 14, 10),
        ParameterBounds('pen_right', 10, 20, 14),
        ParameterBounds('pen_bottom', 10, 20, 14),
        ParameterBounds('pen_left', 10, 20, 14),
        
        # Tensions
        ParameterBounds('t1', 0.8, 1.5, 1.1),
        ParameterBounds('t2', 0.8, 1.5, 1.2),
        ParameterBounds('t3', 0.8, 1.5, 1.1),
        ParameterBounds('t4', 0.8, 1.5, 1.0),
        ParameterBounds('t5', 0.8, 1.5, 1.1),
    ]
    
    print(f"\nOptimizing {len(param_bounds)} parameters:")
    for bound in param_bounds:
        print(f"  {bound.name}: [{bound.min_val}, {bound.max_val}] (initial: {bound.initial})")
    
    # Run optimization
    optimized_params = optimizer.optimize(param_bounds, method='differential_evolution')
    
    # Generate final METAPOST
    final_mp = optimizer.generate_final_metapost(optimized_params)
    
    # Save outputs
    output_mp_file = output_dir / 'U10400_optimized.mp'
    output_mp_file.write_text(final_mp)
    print(f"\nSaved optimized METAPOST: {output_mp_file}")
    
    # Save comparison visualization
    comparison_path = output_dir / 'U10400_comparison.png'
    optimizer.save_comparison(optimized_params, comparison_path)
    
    print("\n" + "=" * 60)
    print("COMPLETE")
    print(f"Check {output_dir}/ for results")

if __name__ == '__main__':
    main()