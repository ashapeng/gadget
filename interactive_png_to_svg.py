#!/usr/bin/env python3
"""
Interactive PNG to SVG Converter

This script prompts the user for input paths and options.
"""

import base64
import os
import sys
from pathlib import Path


def interactive_png_to_svg():
    """Interactive PNG to SVG converter that prompts for all inputs."""
    
    print("🖼️  Interactive PNG to SVG Converter")
    print("=" * 40)
    
    while True:
        # Get input file path
        png_path_input = input("\nEnter the path to your PNG file: ").strip().strip('"')
        
        if not png_path_input:
            print("❌ Please enter a file path.")
            continue
            
        png_path = Path(png_path_input)
        
        # Check if file exists
        if not png_path.exists():
            print(f"❌ File not found: {png_path.absolute()}")
            retry = input("Try again? (y/n): ").strip().lower()
            if retry != 'y':
                return
            continue
        
        # Check if it's a PNG file
        if png_path.suffix.lower() != '.png':
            print(f"❌ File must be a PNG image: {png_path}")
            retry = input("Try again? (y/n): ").strip().lower()
            if retry != 'y':
                return
            continue
        
        break
    
    # Get output file path
    print(f"\nInput file: {png_path}")
    default_output = png_path.with_suffix('.svg')
    
    svg_path_input = input(f"\nEnter output SVG path (or press Enter for '{default_output.name}'): ").strip().strip('"')
    
    if svg_path_input:
        svg_path = Path(svg_path_input)
    else:
        svg_path = default_output
    
    # Get dimensions option
    print("\nDimension options:")
    print("1. Auto-responsive (scales to container)")
    print("2. Specify custom dimensions")
    print("3. Use default 400x400")
    
    while True:
        choice = input("Choose option (1-3): ").strip()
        
        if choice == '1':
            width = height = None
            use_responsive = True
            break
        elif choice == '2':
            try:
                width_input = input("Enter width in pixels: ").strip()
                height_input = input("Enter height in pixels: ").strip()
                width = int(width_input) if width_input else 400
                height = int(height_input) if height_input else 400
                use_responsive = False
                break
            except ValueError:
                print("❌ Please enter valid numbers.")
                continue
        elif choice == '3':
            width = height = 400
            use_responsive = False
            break
        else:
            print("❌ Please choose 1, 2, or 3.")
            continue
    
    # Perform conversion
    try:
        print(f"\n🔄 Converting {png_path.name}...")
        
        # Read PNG file and convert to base64
        with open(png_path, 'rb') as f:
            png_data = f.read()
            base64_data = base64.b64encode(png_data).decode('utf-8')
        
        # Create SVG content
        if use_responsive:
            svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet">
  <title>Converted from {png_path.name}</title>
  <image x="0" y="0" width="100" height="100" 
         preserveAspectRatio="xMidYMid meet"
         xlink:href="data:image/png;base64,{base64_data}"/>
</svg>'''
        else:
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
        
        print(f"✅ Success! Created: {svg_path.absolute()}")
        if use_responsive:
            print("📐 Using responsive dimensions (scales to container)")
        else:
            print(f"📐 SVG dimensions: {width}x{height}")
        
        # Ask if user wants to convert another file
        another = input("\nConvert another file? (y/n): ").strip().lower()
        if another == 'y':
            interactive_png_to_svg()
        
    except Exception as e:
        print(f"❌ Error: {e}")


def quick_convert_with_path():
    """Quick converter that asks only for the file path."""
    
    print("🚀 Quick PNG to SVG Converter")
    print("=" * 30)
    
    png_path_input = input("Enter PNG file path: ").strip().strip('"')
    
    if not png_path_input:
        print("❌ No file path provided.")
        return
    
    png_path = Path(png_path_input)
    
    if not png_path.exists():
        print(f"❌ File not found: {png_path.absolute()}")
        return
    
    if png_path.suffix.lower() != '.png':
        print(f"❌ File must be a PNG image: {png_path}")
        return
    
    svg_path = png_path.with_suffix('.svg')
    
    try:
        # Read PNG and convert
        with open(png_path, 'rb') as f:
            png_data = f.read()
            base64_data = base64.b64encode(png_data).decode('utf-8')
        
        # Create responsive SVG
        svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet">
  <title>Converted from {png_path.name}</title>
  <image x="0" y="0" width="100" height="100" 
         preserveAspectRatio="xMidYMid meet"
         xlink:href="data:image/png;base64,{base64_data}"/>
</svg>'''
        
        with open(svg_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        
        print(f"✅ Success! Created: {svg_path.absolute()}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # If path provided as argument, use quick convert
        png_file = sys.argv[1]
        png_path = Path(png_file)
        
        if not png_path.exists():
            print(f"❌ File not found: {png_path.absolute()}")
            sys.exit(1)
        
        if png_path.suffix.lower() != '.png':
            print(f"❌ File must be a PNG image: {png_path}")
            sys.exit(1)
        
        svg_path = png_path.with_suffix('.svg')
        
        try:
            with open(png_path, 'rb') as f:
                png_data = f.read()
                base64_data = base64.b64encode(png_data).decode('utf-8')
            
            svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet">
  <title>Converted from {png_path.name}</title>
  <image x="0" y="0" width="100" height="100" 
         preserveAspectRatio="xMidYMid meet"
         xlink:href="data:image/png;base64,{base64_data}"/>
</svg>'''
            
            with open(svg_path, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            
            print(f"✅ Success! Created: {svg_path.absolute()}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
    else:
        # Interactive mode
        print("Choose conversion mode:")
        print("1. Interactive (full options)")
        print("2. Quick (just enter file path)")
        
        choice = input("Enter choice (1 or 2): ").strip()
        
        if choice == '1':
            interactive_png_to_svg()
        elif choice == '2':
            quick_convert_with_path()
        else:
            print("Invalid choice. Using interactive mode...")
            interactive_png_to_svg()
