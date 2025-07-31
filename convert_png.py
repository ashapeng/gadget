#!/usr/bin/env python3
"""
Drag-and-Drop PNG to SVG Converter

Usage examples:
1. Command line: python convert_png.py "C:/path/to/image.png"
2. Drag and drop: Drag a PNG file onto this script
3. Interactive: Run without arguments to enter path manually
"""

import base64
import sys
from pathlib import Path


def convert_png_to_svg(png_file_path):
    """
    Convert a PNG file to SVG format.
    
    Args:
        png_file_path (str): Path to the PNG file
        
    Returns:
        str: Path to the created SVG file
        
    Raises:
        Exception: If conversion fails
    """
    
    # Clean up the path (remove quotes, normalize)
    clean_path = str(png_file_path).strip().strip('"').strip("'")
    png_path = Path(clean_path)
    
    print(f"🔍 Checking file: {png_path.absolute()}")
    
    # Validate input
    if not png_path.exists():
        raise FileNotFoundError(f"PNG file not found: {png_path.absolute()}")
    
    if not png_path.suffix.lower() == '.png':
        raise ValueError(f"File must be a PNG image (got: {png_path.suffix})")
    
    # Create output path
    svg_path = png_path.with_suffix('.svg')
    
    print(f"📄 Input:  {png_path.name}")
    print(f"📄 Output: {svg_path.name}")
    print(f"🔄 Converting...")
    
    try:
        # Read PNG file
        with open(png_path, 'rb') as f:
            png_data = f.read()
        
        # Convert to base64
        base64_data = base64.b64encode(png_data).decode('utf-8')
        
        # Create SVG content (responsive, will scale to fit container)
        svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" 
     xmlns:xlink="http://www.w3.org/1999/xlink"
     viewBox="0 0 100 100" 
     preserveAspectRatio="xMidYMid meet"
     style="max-width: 100%; height: auto;">
  <title>Converted from {png_path.name}</title>
  <desc>PNG to SVG conversion - responsive image</desc>
  <image x="0" y="0" 
         width="100" 
         height="100" 
         preserveAspectRatio="xMidYMid meet"
         xlink:href="data:image/png;base64,{base64_data}"/>
</svg>'''
        
        # Write SVG file
        with open(svg_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        
        print(f"✅ SUCCESS!")
        print(f"📁 Created: {svg_path.absolute()}")
        print(f"📊 Original size: {len(png_data):,} bytes")
        print(f"📊 SVG size: {len(svg_content.encode('utf-8')):,} bytes")
        
        return str(svg_path.absolute())
        
    except Exception as e:
        raise Exception(f"Failed to convert {png_path.name}: {str(e)}")


def main():
    """Main function to handle different input methods."""
    
    print("🖼️  PNG to SVG Converter")
    print("=" * 40)
    
    # Check if file path was provided as command line argument
    if len(sys.argv) > 1:
        # File path provided as argument (drag-and-drop or command line)
        input_path = sys.argv[1]
        
        try:
            result = convert_png_to_svg(input_path)
            print(f"\n🎉 Conversion complete!")
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            input("\nPress Enter to exit...")
            sys.exit(1)
    
    else:
        # Interactive mode - ask user for file path
        print("\nNo file specified. Please enter the path to your PNG file.")
        print("💡 Tip: You can also drag and drop a PNG file onto this script!")
        
        while True:
            print("\n" + "-" * 40)
            file_path = input("Enter PNG file path (or 'quit' to exit): ").strip()
            
            if file_path.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not file_path:
                print("❌ Please enter a file path.")
                continue
            
            try:
                result = convert_png_to_svg(file_path)
                print(f"\n🎉 Conversion complete!")
                
                # Ask if user wants to convert another file
                another = input("\nConvert another file? (y/n): ").strip().lower()
                if another not in ['y', 'yes']:
                    print("👋 Goodbye!")
                    break
                    
            except Exception as e:
                print(f"\n❌ ERROR: {e}")
                retry = input("Try again? (y/n): ").strip().lower()
                if retry not in ['y', 'yes']:
                    break
    
    # Keep window open if run by double-clicking
    if len(sys.argv) <= 1:
        input("\nPress Enter to exit...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        input("\nPress Enter to exit...")
        sys.exit(1)
