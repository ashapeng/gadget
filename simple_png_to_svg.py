#!/usr/bin/env python3
"""
Simple PNG to SVG Converter Example

This is a simplified version for quick conversions.
"""

import base64
from pathlib import Path
from PIL import Image
import io


def simple_png_to_svg(png_file, svg_file=None):
    """
    Simple function to convert PNG to SVG.
    
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
    
    # Open image and get dimensions
    with Image.open(png_path) as img:
        width, height = img.size
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_data = buffer.getvalue()
        base64_data = base64.b64encode(img_data).decode('utf-8')
    
    # Create SVG
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <image x="0" y="0" width="{width}" height="{height}" 
         xlink:href="data:image/png;base64,{base64_data}"/>
</svg>'''
    
    # Write SVG file
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    print(f"Converted {png_path.name} to {svg_path.name}")
    return str(svg_path)


# Example usage
if __name__ == "__main__":
    import sys
    
    # If command line argument provided, use it
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        
        try:
            result = simple_png_to_svg(input_file, output_file)
            print(f"✅ Success! Created: {result}")
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
    else:
        # Example: Convert the RNA image if it exists
        rna_img_path = Path("rna_structure/rna_img.png")
        
        if rna_img_path.exists():
            print("Converting RNA image...")
            try:
                result = simple_png_to_svg(rna_img_path)
                print(f"✅ Success! Created: {result}")
            except Exception as e:
                print(f"❌ Error: {e}")
        else:
            print("No RNA image found. Please specify a PNG file to convert.")
            print("\nUsage:")
            print("  python simple_png_to_svg.py your_image.png")
            print("  python simple_png_to_svg.py input.png output.svg")
            print("\nOr use in Python:")
            print("  from simple_png_to_svg import simple_png_to_svg")
            print("  simple_png_to_svg('your_image.png')")
            print("  simple_png_to_svg('input.png', 'output.svg')")
