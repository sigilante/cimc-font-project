#!/usr/bin/env python3
"""
Build all font weights by modifying pen_height and running mpost.
"""

import os
import re
import shutil
import subprocess
from pathlib import Path

# Weight definitions: name -> pen_height multiplier
WEIGHTS = {
    "UltraLight": 0.06,
    "Light": 0.09,
    "Normal": 0.12,
    "SemiBold": 0.15,
    "Bold": 0.18,
    "Black": 0.21,
}

# Paths
SCRIPT_DIR = Path(__file__).parent
SRC_FILE = SCRIPT_DIR / "src" / "calyptapis.mp"
OUTPUT_DIR = SCRIPT_DIR / "maj"


def modify_pen_height(content: str, multiplier: float) -> str:
    """Replace pen_height value in the MetaPost source."""
    pattern = r"(pen_height\s*:=\s*)[\d.]+(\s*\*\s*font_size)"
    replacement = rf"\g<1>{multiplier}\2"
    return re.sub(pattern, replacement, content)


def run_mpost() -> bool:
    """Run mpost on the source file."""
    result = subprocess.run(
        ["mpost", "src/calyptapis.mp"],
        cwd=SCRIPT_DIR,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"mpost error:\n{result.stderr}")
        return False
    return True


def copy_svgs(weight_name: str) -> int:
    """Move generated SVGs to the weight's directory."""
    dest_dir = OUTPUT_DIR / weight_name
    dest_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for svg_file in SCRIPT_DIR.glob("calyptapis-*.svg"):
        dest_file = dest_dir / svg_file.name
        shutil.move(svg_file, dest_file)
        count += 1

    return count


def main():
    # Read original source
    original_content = SRC_FILE.read_text()

    try:
        for weight_name, multiplier in WEIGHTS.items():
            print(f"Building {weight_name} (pen_height = {multiplier} * font_size)...")

            # Modify source with new pen_height
            modified_content = modify_pen_height(original_content, multiplier)
            SRC_FILE.write_text(modified_content)

            # Run mpost
            if not run_mpost():
                print(f"  Failed to build {weight_name}")
                continue

            # Copy SVGs to weight directory
            count = copy_svgs(weight_name)
            print(f"  Copied {count} SVGs to maj/{weight_name}/")

    finally:
        # Restore original source
        SRC_FILE.write_text(original_content)
        print("\nRestored original calyptapis.mp")


if __name__ == "__main__":
    main()
