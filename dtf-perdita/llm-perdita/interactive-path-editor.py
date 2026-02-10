#!/usr/bin/env python3
# interactive_path_editor.py

import cv2
import numpy as np
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional, Tuple
import matplotlib.pyplot as plt

@dataclass
class PathPoint:
    """A control point on the path."""
    x: float
    y: float
    direction: Optional[str] = None  # 'up', 'down', 'left', 'right', or None
    fixed: bool = False
    tension: float = 1.0

@dataclass
class PathSegment:
    """A continuous stroke (may have multiple points)."""
    points: List[PathPoint]
    pen_start: float = 12.0  # Pen size at segment start
    pen_end: float = 12.0    # Pen size at segment end
    pen_shape: str = 'circle'  # 'circle', 'square', 'diamond'

class InteractivePathEditor:
    """
    Interactive tool to trace centerline over specimen.
    
    Controls:
    - Left click: Add point to current segment
    - Right click on point: Cycle direction (up/down/left/right/none)
    - Shift+click on point: Toggle fixed/free
    - Ctrl+click: Start new segment (disconnected stroke)
    - Mouse wheel: Adjust pen size for current segment
    - 1/2/3: Set pen shape (circle/square/diamond)
    - +/-: Increase/decrease pen size at segment end
    - [/]: Increase/decrease pen size at segment start
    - 'd': Delete last point
    - 'c': Clear all segments
    - 's': Save segments to file
    - 'l': Load segments from file
    - 'g': Generate METAPOST code
    - 'o': Optimize free parameters
    - 'q': Quit
    """
    
    def __init__(self, specimen_path: Path):
        self.specimen = cv2.imread(str(specimen_path))
        if self.specimen is None:
            raise ValueError(f"Could not load {specimen_path}")
        
        self.specimen_rgb = cv2.cvtColor(self.specimen, cv2.COLOR_BGR2RGB)
        self.display = self.specimen_rgb.copy()
        
        self.segments: List[PathSegment] = [PathSegment(points=[])]
        self.current_segment_idx = 0
        
        self.height, self.width = self.specimen.shape[:2]
        
        self.print_help()
    
    def print_help(self):
        print("Interactive Path Editor")
        print("=" * 60)
        print("MOUSE CONTROLS:")
        print("  Left click: Add control point")
        print("  Right click on point: Cycle direction constraint")
        print("  Shift+click on point: Toggle fixed/free")
        print()
        print("SEGMENT CONTROLS:")
        print("  n: Start new disconnected segment (next click is first point)")
        print()
        print("PEN SIZE CONTROLS:")
        print("  +/-: Adjust pen size at segment END")
        print("  [/]: Adjust pen size at segment START")
        print("  1/2/3: Set pen shape (circle/square/diamond)")
        print()
        print("COMMANDS:")
        print("  d: Delete last point")
        print("  c: Clear all segments")
        print("  s: Save segments to JSON")
        print("  l: Load segments from JSON")
        print("  g: Generate METAPOST code")
        print("  o: Optimize free parameters")
        print("  q: Quit")
        print("=" * 60)
    
    def current_segment(self) -> PathSegment:
        """Get current segment."""
        return self.segments[self.current_segment_idx]
    
    def run(self):
        """Main interaction loop."""
        cv2.namedWindow('Path Editor')
        cv2.setMouseCallback('Path Editor', self.mouse_callback)
        
        self.new_segment_mode = False  # Flag for starting new segment
        
        while True:
            self.render()
            cv2.imshow('Path Editor', cv2.cvtColor(self.display, cv2.COLOR_RGB2BGR))
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                break
            elif key == ord('d'):
                self.delete_last_point()
            elif key == ord('c'):
                self.clear_all()
            elif key == ord('n'):
                # Toggle new segment mode
                self.new_segment_mode = True
                print("NEW SEGMENT MODE: Next click will start a new segment")
            elif key == ord('g'):
                self.generate_metapost()
                self.generate_metapost_parameterized()
            elif key == ord('o'):
                self.optimize_path()
            elif key == ord('s'):
                self.save_segments()
            elif key == ord('l'):
                self.load_segments()
            elif key == ord('+') or key == ord('='):
                self.adjust_pen_end(+2)
            elif key == ord('-') or key == ord('_'):
                self.adjust_pen_end(-2)
            elif key == ord('['):
                self.adjust_pen_start(-2)
            elif key == ord(']'):
                self.adjust_pen_start(+2)
            elif key == ord('1'):
                self.set_pen_shape('circle')
            elif key == ord('2'):
                self.set_pen_shape('square')
            elif key == ord('3'):
                self.set_pen_shape('diamond')
        
        cv2.destroyAllWindows()
    
    def mouse_callback(self, event, x, y, flags, param):
        """Handle mouse events."""
        shift_pressed = (flags & cv2.EVENT_FLAG_SHIFTKEY) != 0
        
        if event == cv2.EVENT_LBUTTONDOWN:
            if shift_pressed:
                # Shift+click: Toggle fixed/free on nearest point
                seg_idx, point_idx = self.find_nearest_point(x, y)
                if seg_idx is not None:
                    self.toggle_fixed(seg_idx, point_idx)
            elif self.new_segment_mode:
                # In new segment mode: Start new segment with this point
                self.start_new_segment()
                point = PathPoint(x=float(x), y=float(y))
                self.current_segment().points.append(point)
                seg_num = self.current_segment_idx + 1
                print(f"Started segment {seg_num} with first point at ({x}, {y})")
                self.new_segment_mode = False  # Turn off after use
            else:
                # Regular click: Add point to current segment
                point = PathPoint(x=float(x), y=float(y))
                self.current_segment().points.append(point)
                seg_num = self.current_segment_idx + 1
                point_num = len(self.current_segment().points)
                print(f"Segment {seg_num}, Point {point_num}: ({x}, {y})")
        
        elif event == cv2.EVENT_RBUTTONDOWN:
            # Right-click: Cycle direction on nearest point
            seg_idx, point_idx = self.find_nearest_point(x, y)
            if seg_idx is not None:
                self.cycle_direction(seg_idx, point_idx)
    
    def start_new_segment(self):
        """Start a new disconnected segment."""
        self.segments.append(PathSegment(points=[]))
        self.current_segment_idx = len(self.segments) - 1
    
    def find_nearest_point(self, x: int, y: int, threshold: float = 15.0) -> Tuple[Optional[int], Optional[int]]:
        """Find closest point to (x, y). Returns (segment_idx, point_idx)."""
        min_dist = threshold
        nearest_seg = None
        nearest_point = None
        
        for seg_idx, segment in enumerate(self.segments):
            for point_idx, point in enumerate(segment.points):
                dist = np.sqrt((point.x - x)**2 + (point.y - y)**2)
                if dist < min_dist:
                    min_dist = dist
                    nearest_seg = seg_idx
                    nearest_point = point_idx
        
        return nearest_seg, nearest_point
    
    def cycle_direction(self, seg_idx: int, point_idx: int):
        """Cycle through direction constraints."""
        directions = [None, 'up', 'right', 'down', 'left']
        point = self.segments[seg_idx].points[point_idx]
        
        current_idx = directions.index(point.direction) if point.direction in directions else 0
        next_idx = (current_idx + 1) % len(directions)
        point.direction = directions[next_idx]
        
        dir_str = point.direction or "free"
        print(f"Segment {seg_idx + 1}, Point {point_idx + 1} direction: {dir_str}")
    
    def toggle_fixed(self, seg_idx: int, point_idx: int):
        """Toggle fixed/free status."""
        point = self.segments[seg_idx].points[point_idx]
        point.fixed = not point.fixed
        status = "FIXED" if point.fixed else "FREE"
        print(f"Segment {seg_idx + 1}, Point {point_idx + 1}: {status}")
    
    def delete_last_point(self):
        """Delete last point from current segment."""
        if self.current_segment().points:
            self.current_segment().points.pop()
            print(f"Deleted point. Segment {self.current_segment_idx + 1} has {len(self.current_segment().points)} points.")
        elif len(self.segments) > 1:
            # Delete empty segment
            self.segments.pop()
            self.current_segment_idx = len(self.segments) - 1
            print(f"Deleted empty segment. Now on segment {self.current_segment_idx + 1}")
    
    def clear_all(self):
        """Clear all segments."""
        self.segments = [PathSegment(points=[])]
        self.current_segment_idx = 0
        print("Cleared all segments.")
    
    def adjust_pen_end(self, delta: float):
        """Adjust pen size at segment end."""
        self.current_segment().pen_end += delta
        self.current_segment().pen_end = max(1.0, self.current_segment().pen_end)
        print(f"Segment {self.current_segment_idx + 1} end pen: {self.current_segment().pen_end:.1f}")
    
    def adjust_pen_start(self, delta: float):
        """Adjust pen size at segment start."""
        self.current_segment().pen_start += delta
        self.current_segment().pen_start = max(1.0, self.current_segment().pen_start)
        print(f"Segment {self.current_segment_idx + 1} start pen: {self.current_segment().pen_start:.1f}")
    
    def set_pen_shape(self, shape: str):
        """Set pen shape for current segment."""
        self.current_segment().pen_shape = shape
        print(f"Segment {self.current_segment_idx + 1} pen shape: {shape}")
    
    def render(self):
        """Render current state."""
        self.display = self.specimen_rgb.copy()
        
        # Draw each segment
        for seg_idx, segment in enumerate(self.segments):
            is_current = (seg_idx == self.current_segment_idx)
            
            # Draw path
            if len(segment.points) >= 2:
                for i in range(len(segment.points) - 1):
                    p1 = segment.points[i]
                    p2 = segment.points[i + 1]
                    
                    # Color: yellow for current, cyan for others
                    color = (255, 255, 0) if is_current else (0, 255, 255)
                    
                    cv2.line(
                        self.display,
                        (int(p1.x), int(p1.y)),
                        (int(p2.x), int(p2.y)),
                        color,
                        2
                    )
            
            # Draw control points
            for i, point in enumerate(segment.points):
                # Color based on status
                if point.fixed:
                    color = (255, 0, 0)  # Red = fixed
                else:
                    color = (0, 255, 0)  # Green = free
                
                cv2.circle(self.display, (int(point.x), int(point.y)), 6, color, -1)
                
                # Direction arrow
                if point.direction:
                    arrow_len = 20
                    dx, dy = {
                        'up': (0, -arrow_len),
                        'down': (0, arrow_len),
                        'left': (-arrow_len, 0),
                        'right': (arrow_len, 0)
                    }[point.direction]
                    
                    cv2.arrowedLine(
                        self.display,
                        (int(point.x), int(point.y)),
                        (int(point.x + dx), int(point.y + dy)),
                        (255, 0, 255),
                        2,
                        tipLength=0.3
                    )
                
                # Label
                label = f"{seg_idx + 1}.{i + 1}"
                cv2.putText(
                    self.display,
                    label,
                    (int(point.x) + 10, int(point.y) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.4,
                    (255, 255, 255),
                    1
                )
        
        # Draw info overlay
        self.draw_info_panel()
    
    def draw_info_panel(self):
        """Draw information panel."""
        panel_height = 100
        panel = np.zeros((panel_height, self.width, 3), dtype=np.uint8)
        
        seg = self.current_segment()
        
        lines = [
            f"Segment {self.current_segment_idx + 1}/{len(self.segments)}  |  Points: {len(seg.points)}",
            f"Pen: {seg.pen_start:.1f} -> {seg.pen_end:.1f}  |  Shape: {seg.pen_shape}",
            f"Controls: +/- (end pen)  [/] (start pen)  1/2/3 (shape)",
        ]
        
        y_offset = 25
        for line in lines:
            cv2.putText(panel, line, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.5, (255, 255, 255), 1)
            y_offset += 25
        
        # Append panel to bottom of display
        self.display = np.vstack([self.display, panel])
    
    def generate_metapost(self):
        """Generate METAPOST code from segments."""
        print("\n" + "=" * 60)
        print("GENERATED METAPOST CODE:")
        print("=" * 60)
        
        all_code = [
            "% SVG output configuration",
            "outputformat := \"svg\";",
            "outputtemplate := \"%j-%c.svg\";",
            "",
            "beginfig(1);",
            ""
        ]
        
        # Generate paths
        seg_names = []
        for seg_idx, segment in enumerate(self.segments):
            if len(segment.points) < 2:
                continue
            
            # Use letter suffix: seg_a, seg_b, seg_c...
            seg_name = f"seg_{chr(ord('a') + seg_idx)}"
            seg_names.append((seg_name, segment))
            
            # Generate path
            lines = [f"% Segment {seg_idx + 1}"]
            lines.append(f"path {seg_name};")
            lines.append(f"{seg_name} := ")
            
            for i, point in enumerate(segment.points):
                x = point.x - self.width / 2
                y = self.height / 2 - point.y
                
                if i == 0:
                    line = f"  ({x:.1f}, {y:.1f})"
                else:
                    line = f"  .. tension {point.tension:.2f}\n  .. ({x:.1f}, {y:.1f})"
                
                if point.direction:
                    line += "{" + point.direction + "}"
                
                lines.append(line)
            
            lines.append("  ;")
            lines.append("")
            
            all_code.append("\n".join(lines))
        
        # Declare variables once at top level
        if seg_names:
            all_code.append("% Drawing variables")
            all_code.append("numeric n_seg, plen, i, t_start, t_end, current_pen;")
            all_code.append("n_seg := 20;")
            all_code.append("")
        
        # Generate drawing code for each segment
        for seg_name, segment in seg_names:
            pen_shape_map = {
                'circle': 'pencircle',
                'square': 'pensquare',
                'diamond': 'pensquare rotated 45'
            }
            
            lines = [f"% Draw {seg_name}"]
            
            if abs(segment.pen_start - segment.pen_end) < 0.1:
                # Constant pen
                lines.append(f"pickup {pen_shape_map[segment.pen_shape]} scaled {segment.pen_start:.1f};")
                lines.append(f"draw {seg_name};")
            else:
                # Variable pen
                lines.append(f"plen := length({seg_name});")
                lines.append("for i = 0 upto n_seg - 1:")
                lines.append("  t_start := (i / n_seg) * plen;")
                lines.append("  t_end := ((i + 1) / n_seg) * plen;")
                lines.append(f"  current_pen := {segment.pen_start:.1f} + ")
                lines.append(f"    ({segment.pen_end:.1f} - {segment.pen_start:.1f}) * (i / n_seg);")
                lines.append(f"  pickup {pen_shape_map[segment.pen_shape]} scaled current_pen;")
                lines.append(f"  draw subpath (t_start, t_end) of {seg_name};")
                lines.append("endfor;")
            
            lines.append("")
            all_code.append("\n".join(lines))
        
        all_code.append("endfig;")
        all_code.append("end;")
        
        code = "\n".join(all_code)
        print(code)
        print("=" * 60)
        
        # Save
        output_path = Path("generated_path.mp")
        output_path.write_text(code)
        print(f"\nSaved to: {output_path}")
        
        return code
    
    def generate_metapost_parameterized(self):
        """
        Generate METAPOST with hierarchical parameterization.
        Couples related parameters to reduce optimization space.
        """
        print("\n" + "=" * 60)
        print("GENERATED HIERARCHICAL METAPOST:")
        print("=" * 60)
        
        all_code = [
            "% SVG output configuration",
            "outputformat := \"svg\";",
            "outputtemplate := \"%j-%c.svg\";",
            "",
            "beginfig(1);",
            ""
        ]
        
        # Analyze segments to determine pen size range
        all_pen_sizes = []
        for seg in self.segments:
            if len(seg.points) >= 2:
                all_pen_sizes.extend([seg.pen_start, seg.pen_end])
        
        pen_max = max(all_pen_sizes) if all_pen_sizes else 30.0
        pen_min = min(all_pen_sizes) if all_pen_sizes else 10.0
        
        all_code.append("% ==== HIGH-LEVEL PARAMETERS ====")
        all_code.append("% These are the main controls for optimization")
        all_code.append("")
        
        # Global pen sizes
        all_code.append("% Pen sizes")
        all_code.append(f"pen_thick := {pen_max:.1f};  % Thickest strokes")
        all_code.append(f"pen_thin := {pen_min:.1f};   % Thinnest strokes")
        all_code.append("")
        
        # Global tension
        all_code.append("% Curve tension (how tight the curves are)")
        all_code.append("global_tension := 1.00;")
        all_code.append("")
        
        # Global scale
        all_code.append("% Overall scaling")
        all_code.append("x_scale := 1.0;")
        all_code.append("y_scale := 1.0;")
        all_code.append("")
        
        all_code.append("% ==== BASE COORDINATES ====")
        all_code.append("% Individual point positions (before scaling)")
        all_code.append("")
        
        seg_params = []
        
        for seg_idx, segment in enumerate(self.segments):
            if len(segment.points) < 2:
                continue
            
            seg_letter = chr(ord('a') + seg_idx)
            seg_name = f"seg_{seg_letter}"
            point_params = []
            
            all_code.append(f"% Segment {seg_idx + 1} base coordinates")
            
            # Determine if this segment uses thick or thin pen
            avg_pen = (segment.pen_start + segment.pen_end) / 2
            pen_ratio_start = segment.pen_start / pen_max if pen_max > 0 else 1.0
            pen_ratio_end = segment.pen_end / pen_max if pen_max > 0 else 1.0
            
            # Store pen assignments (as ratios of thick pen)
            all_code.append(f"pen_ratio_start_{seg_letter} := {pen_ratio_start:.3f};")
            all_code.append(f"pen_ratio_end_{seg_letter} := {pen_ratio_end:.3f};")
            all_code.append("")
            
            # Point base coordinates
            for i, point in enumerate(segment.points):
                x_base = point.x - self.width / 2
                y_base = self.height / 2 - point.y
                
                param_x_base = f"x_{seg_letter}_{i}_base"
                param_y_base = f"y_{seg_letter}_{i}_base"
                
                all_code.append(f"{param_x_base} := {x_base:.1f};")
                all_code.append(f"{param_y_base} := {y_base:.1f};")
                
                point_params.append({
                    'x_base': param_x_base,
                    'y_base': param_y_base,
                    'direction': point.direction,
                    'fixed': point.fixed
                })
            
            all_code.append("")
            
            seg_params.append({
                'name': seg_name,
                'letter': seg_letter,
                'segment': segment,
                'points': point_params,
                'pen_ratio_start': pen_ratio_start,
                'pen_ratio_end': pen_ratio_end
            })
        
        all_code.append("% ==== DERIVED PARAMETERS ====")
        all_code.append("% Computed from high-level parameters")
        all_code.append("")
        
        # Apply scaling to get actual coordinates
        for seg_data in seg_params:
            seg_letter = seg_data['letter']
            all_code.append(f"% Segment {seg_letter} scaled coordinates")
            
            for i, point in enumerate(seg_data['points']):
                param_x = f"x_{seg_letter}_{i}"
                param_y = f"y_{seg_letter}_{i}"
                
                all_code.append(f"{param_x} := {point['x_base']} * x_scale;")
                all_code.append(f"{param_y} := {point['y_base']} * y_scale;")
            
            all_code.append("")
        
        # Compute actual pen sizes
        all_code.append("% Pen sizes (derived from ratios)")
        for seg_data in seg_params:
            seg_letter = seg_data['letter']
            all_code.append(f"pen_start_{seg_letter} := pen_thick * pen_ratio_start_{seg_letter};")
            all_code.append(f"pen_end_{seg_letter} := pen_thick * pen_ratio_end_{seg_letter};")
        all_code.append("")
        
        all_code.append("% ==== PATH DEFINITIONS ====")
        all_code.append("")
        
        # Generate paths
        for seg_data in seg_params:
            seg_name = seg_data['name']
            seg_letter = seg_data['letter']
            points = seg_data['points']
            
            all_code.append(f"path {seg_name};")
            all_code.append(f"{seg_name} := ")
            
            for i, point in enumerate(points):
                param_x = f"x_{seg_letter}_{i}"
                param_y = f"y_{seg_letter}_{i}"
                
                if i == 0:
                    line = f"  ({param_x}, {param_y})"
                else:
                    line = f"  .. tension global_tension\n  .. ({param_x}, {param_y})"
                
                if point['direction']:
                    line += "{" + point['direction'] + "}"
                
                all_code.append(line)
            
            all_code.append("  ;")
            all_code.append("")
        
        # Drawing
        all_code.append("% ==== DRAWING ====")
        all_code.append("")
        all_code.append("n_seg := 20;")
        all_code.append("")
        
        for seg_data in seg_params:
            seg_name = seg_data['name']
            seg_letter = seg_data['letter']
            segment = seg_data['segment']
            
            pen_shape_map = {
                'circle': 'pencircle',
                'square': 'pensquare',
                'diamond': 'pensquare rotated 45'
            }
            
            all_code.append(f"% Draw {seg_name}")
            
            if abs(segment.pen_start - segment.pen_end) < 0.1:
                all_code.append(f"pickup {pen_shape_map[segment.pen_shape]} scaled pen_start_{seg_letter};")
                all_code.append(f"draw {seg_name};")
            else:
                all_code.append(f"plen := length({seg_name});")
                all_code.append("for i = 0 upto n_seg - 1:")
                all_code.append("  t_start := (i / n_seg) * plen;")
                all_code.append("  t_end := ((i + 1) / n_seg) * plen;")
                all_code.append(f"  current_pen := pen_start_{seg_letter} + ")
                all_code.append(f"    (pen_end_{seg_letter} - pen_start_{seg_letter}) * (i / n_seg);")
                all_code.append(f"  pickup {pen_shape_map[segment.pen_shape]} scaled current_pen;")
                all_code.append(f"  draw subpath (t_start, t_end) of {seg_name};")
                all_code.append("endfor;")
            
            all_code.append("")
        
        all_code.append("endfig;")
        all_code.append("end;")
        
        code = "\n".join(all_code)
        print(code)
        print("=" * 60)
        
        output_path = Path("generated_path_parameterized.mp")
        output_path.write_text(code)
        print(f"\nSaved to: {output_path}")
        
        # Save metadata with hierarchical structure
        self.save_hierarchical_metadata(seg_params, pen_max, pen_min)
        
        return code

    def save_hierarchical_metadata(self, seg_params, pen_max, pen_min):
        """Save metadata for hierarchical optimization."""
        import json
        
        metadata = {
            'image_width': self.width,
            'image_height': self.height,
            'hierarchy': {
                'global': [
                    {
                        'name': 'pen_thick',
                        'value': pen_max,
                        'min': pen_max * 0.7,
                        'max': pen_max * 1.3,
                        'type': 'pen_size'
                    },
                    {
                        'name': 'pen_thin',
                        'value': pen_min,
                        'min': pen_min * 0.5,
                        'max': pen_min * 1.5,
                        'type': 'pen_size'
                    },
                    {
                        'name': 'global_tension',
                        'value': 1.0,
                        'min': 0.7,
                        'max': 1.5,
                        'type': 'tension'
                    },
                    {
                        'name': 'x_scale',
                        'value': 1.0,
                        'min': 0.8,
                        'max': 1.2,
                        'type': 'scale'
                    },
                    {
                        'name': 'y_scale',
                        'value': 1.0,
                        'min': 0.8,
                        'max': 1.2,
                        'type': 'scale'
                    }
                ],
                'points': []
            }
        }
        
        # Add individual point base coordinates (only if not fixed)
        for seg_data in seg_params:
            seg_letter = seg_data['letter']
            for i, point in enumerate(seg_data['points']):
                if not point['fixed']:
                    x_base = float(point['x_base'].split(':=')[0].strip()) if ':=' in str(point['x_base']) else 0.0
                    y_base = float(point['y_base'].split(':=')[0].strip()) if ':=' in str(point['y_base']) else 0.0
                    
                    # Extract actual values
                    param_x_base = point['x_base']
                    param_y_base = point['y_base']
                    
                    metadata['hierarchy']['points'].append({
                        'x_base': {
                            'name': param_x_base,
                            'optimizable': True,
                            'range_fraction': 0.15  # Allow ±15% movement
                        },
                        'y_base': {
                            'name': param_y_base,
                            'optimizable': True,
                            'range_fraction': 0.15
                        }
                    })
        
        output_path = Path("optimizer_metadata.json")
        with open(output_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"Saved hierarchical metadata to: {output_path}")
        
        # Print summary
        total_params = 5  # Global parameters
        free_points = sum(1 for seg in seg_params for p in seg['points'] if not p['fixed'])
        total_params += free_points * 2  # x_base and y_base for each free point
        
        print(f"\nParameter summary:")
        print(f"  Global parameters: 5 (pen_thick, pen_thin, global_tension, x_scale, y_scale)")
        print(f"  Free point positions: {free_points} points × 2 = {free_points * 2} coordinates")
        print(f"  Fixed points: {sum(1 for seg in seg_params for p in seg['points'] if p['fixed'])}")
        print(f"  TOTAL OPTIMIZABLE: {total_params} parameters")

    def save_optimizer_metadata(self, seg_params):
        """Save metadata for optimizer about which parameters can be adjusted."""
        import json
        
        metadata = {
            'image_width': self.width,
            'image_height': self.height,
            'parameters': []
        }
        
        for seg_data in seg_params:
            seg_info = {
                'segment_name': seg_data['name'],
                'pen_start': {
                    'name': seg_data['pen_start'],
                    'value': seg_data['segment'].pen_start,
                    'min': 1.0,
                    'max': 50.0,
                    'optimizable': True
                },
                'pen_end': {
                    'name': seg_data['pen_end'],
                    'value': seg_data['segment'].pen_end,
                    'min': 1.0,
                    'max': 50.0,
                    'optimizable': True
                },
                'points': []
            }
            
            for point in seg_data['points']:
                seg_info['points'].append({
                    'x': {
                        'name': point['x'],
                        'fixed': point['fixed'],
                        'optimizable': not point['fixed']
                    },
                    'y': {
                        'name': point['y'],
                        'fixed': point['fixed'],
                        'optimizable': not point['fixed']
                    },
                    'tension': {
                        'name': point['t'],
                        'min': 0.5,
                        'max': 2.0,
                        'optimizable': True
                    },
                    'direction': point['direction']
                })
            
            metadata['parameters'].append(seg_info)
        
        output_path = Path("optimizer_metadata.json")
        with open(output_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"Saved optimizer metadata to: {output_path}")

    def save_segments(self):
        """Save segments to JSON file."""
        import json
        
        data = {
            'width': self.width,
            'height': self.height,
            'segments': [
                {
                    'points': [
                        {
                            'x': p.x,
                            'y': p.y,
                            'direction': p.direction,
                            'fixed': p.fixed,
                            'tension': p.tension
                        }
                        for p in seg.points
                    ],
                    'pen_start': seg.pen_start,
                    'pen_end': seg.pen_end,
                    'pen_shape': seg.pen_shape
                }
                for seg in self.segments
            ]
        }
        
        output_path = Path("segments.json")
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Saved segments to: {output_path}")
    
    def load_segments(self):
        """Load segments from JSON file."""
        import json
        
        input_path = Path("segments.json")
        if not input_path.exists():
            print(f"No segments file found: {input_path}")
            return
        
        with open(input_path) as f:
            data = json.load(f)
        
        self.segments = []
        for seg_data in data['segments']:
            points = [
                PathPoint(
                    x=p['x'],
                    y=p['y'],
                    direction=p.get('direction'),
                    fixed=p.get('fixed', False),
                    tension=p.get('tension', 1.0)
                )
                for p in seg_data['points']
            ]
            
            segment = PathSegment(
                points=points,
                pen_start=seg_data.get('pen_start', 12.0),
                pen_end=seg_data.get('pen_end', 12.0),
                pen_shape=seg_data.get('pen_shape', 'circle')
            )
            
            self.segments.append(segment)
        
        self.current_segment_idx = len(self.segments) - 1
        print(f"Loaded {len(self.segments)} segments from: {input_path}")
    
    def optimize_path(self):
        """Optimize free parameters."""
        print("\n" + "=" * 60)
        print("OPTIMIZATION")
        print("=" * 60)
        print("Pen sizes can be set manually with +/- and [/]")
        print("Point positions will be optimized to match specimen")
        print("(Full optimization not yet implemented)")
        print("=" * 60)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Interactive path editor')
    parser.add_argument('specimen', type=Path, help='Specimen image')
    
    args = parser.parse_args()
    
    if not args.specimen.exists():
        print(f"ERROR: File not found: {args.specimen}")
        return
    
    editor = InteractivePathEditor(args.specimen)
    editor.run()

if __name__ == '__main__':
    main()
