import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional

@dataclass
class GlobalParameters:
    """Font-wide parameters from header"""
    # Geometric dimensions
    x_radius: Optional[float] = None
    y_radius: Optional[float] = None
    cap_height: Optional[float] = None
    x_height: Optional[float] = None
    
    # Pen definitions
    thin_pen: Optional[str] = None  # e.g., "pencircle scaled 0.5pt"
    thick_pen: Optional[str] = None
    loz_pen: Optional[str] = None
    
    # Spacing
    em_width: Optional[float] = None
    
    # Any other font-wide constants
    raw_header: str = ""

def parse_metapost_value(value_str: str):
    """Parse a METAPOST value string into a Python value"""
    value_str = value_str.strip().rstrip('pt')
    try:
        return float(value_str)
    except ValueError:
        return value_str

def parse_header(header_file: Path) -> GlobalParameters:
    """Extract global variable definitions"""
    content = header_file.read_text()
    params = GlobalParameters(raw_header=content)
    
    # Find variable assignments
    # x_radius := 10pt;
    assignments = re.findall(
        r'(\w+)\s*:=\s*([^;]+);',
        content
    )
    
    for var_name, value in assignments:
        if hasattr(params, var_name):
            setattr(params, var_name, parse_metapost_value(value))
    
    # Find pen definitions
    # thin_pen := pencircle scaled 0.5pt rotated 15;
    pen_defs = re.findall(
        r'(\w+_pen)\s*:=\s*([^;]+);',
        content
    )
    
    for pen_name, definition in pen_defs:
        if hasattr(params, pen_name):
            setattr(params, pen_name, definition)
    
    return params
