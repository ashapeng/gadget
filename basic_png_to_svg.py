#!/usr/bin/env python3
"""
Basic PNG to SVG Converter (No External Dependencies)

This version uses only Python standard library modules.
It simply embeds the PNG file as base64 data in an SVG container
without any image processing capabilities.
"""

import base64
import os
import sys
from pathlib import Path


def basic_png_to_svg(png_file, svg_file=None):
    """
    Convert PNG to SVG using only standard library (no PIL/Pillow required).
    
    Note: This version cannot determine image dimensions, so it creates
    an SVG with default dimensions that will scale to fit the container.
    
    Args:
        png_file (str): Path to PNG file
        svg_file (str, optional): Output SVG path. If None, uses PNG name with .svg extension
    
    Returns:
        str: Path to created SVG file
    
    Raises:
        FileNotFoundError: If the PNG file doesn't exist
        ValueError: If the file is not a valid PNG
    """
    
    png_path = Path(png_file)
    
    # Check if file exists
    if not png_path.exists():
        raise FileNotFoundError(f"PNG file not found: {png_path.absolute()}")
    
    # Check if it's a PNG file
    if png_path.suffix.lower() != '.png':
        raise ValueError(f"File must be a PNG image: {png_path}")
    
    if svg_file is None:
        svg_path = png_path.with_suffix('.svg')
    else:
        svg_path = Path(svg_file)
    
    # Read PNG file and convert to base64
    with open(png_path, 'rb') as f:
        png_data = f.read()
        base64_data = base64.b64encode(png_data).decode('utf-8')
    
    # Create SVG content (with responsive dimensions)
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet">
  <title>Converted from {png_path.name}</title>
  <image x="0" y="0" width="100" height="100" 
         preserveAspectRatio="xMidYMid meet"
         xlink:href="data:image/png;base64,{base64_data}"/>
</svg>'''
    
    # Write SVG file
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    print(f"Converted {png_path.name} to {svg_path.name}")
    print(f"Note: Using responsive SVG dimensions (will scale to container)")
    return str(svg_path)


def basic_png_to_svg_with_size(png_file, svg_file=None, width=None, height=None):
    """
    Convert PNG to SVG with specified dimensions.
    
    Args:
        png_file (str): Path to PNG file
        svg_file (str, optional): Output SVG path
        width (int, optional): SVG width in pixels
        height (int, optional): SVG height in pixels
    
    Returns:
        str: Path to created SVG file
    """
    
    png_path = Path(png_file)
    
    if not png_path.exists():
        raise FileNotFoundError(f"PNG file not found: {png_path.absolute()}")
    
    if png_path.suffix.lower() != '.png':
        raise ValueError(f"File must be a PNG image: {png_path}")
    
    if svg_file is None:
        svg_path = png_path.with_suffix('.svg')
    else:
        svg_path = Path(svg_file)
    
    # Use default dimensions if not specified
    if width is None:
        width = 400
    if height is None:
        height = 400
    
    # Read PNG file and convert to base64
    with open(png_path, 'rb') as f:
        png_data = f.read()
        base64_data = base64.b64encode(png_data).decode('utf-8')
    
    # Create SVG content with specified dimensions
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <title>Converted from {png_path.name}</title>
  <image x="0" y="0" width="{width}" height="{height}" 
         xlink:href="data:image/png;base64,{base64_data}"/>
</svg>'''
    
    # Write SVG file
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    print(f"Converted {png_path.name} to {svg_path.name}")
    print(f"SVG dimensions: {width}x{height}")
    return str(svg_path)


# Example usage and command line interface
if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        
        # Parse additional arguments
        output_file = None
        width = None
        height = None
        
        for i, arg in enumerate(sys.argv[2:], 2):
            if arg.startswith('--width='):
                width = int(arg.split('=')[1])
            elif arg.startswith('--height='):
                height = int(arg.split('=')[1])
            elif not arg.startswith('--'):
                output_file = arg
        
        try:
            if width or height:
                result = basic_png_to_svg_with_size(input_file, output_file, width, height)
            else:
                result = basic_png_to_svg(input_file, output_file)
            print(f"✅ Success! Created: {result}")
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
    else:
        # Check for RNA image
        rna_img_path = Path("rna_structure/rna_img.png")
        
        if rna_img_path.exists():
            print("Converting RNA image...")
            try:
                result = basic_png_to_svg(rna_img_path)
                print(f"✅ Success! Created: {result}")
            except Exception as e:
                print(f"❌ Error: {e}")
        else:
            print("Basic PNG to SVG Converter (No External Dependencies)")
            print("=" * 50)
            print("No PNG file specified. Usage:")
            print()
            print("Command line:")
            print("  python basic_png_to_svg.py image.png")
            print("  python basic_png_to_svg.py image.png output.svg")
            print("  python basic_png_to_svg.py image.png --width=500 --height=400")
            print()
            print("Python code:")
            print("  from basic_png_to_svg import basic_png_to_svg")
            print("  basic_png_to_svg('image.png')")
            print("  basic_png_to_svg_with_size('image.png', width=500, height=400)")
            print()
            print("Note: This version doesn't require Pillow but cannot auto-detect")
            print("      image dimensions. Use the simple_png_to_svg.py for full features.")
