#!/usr/bin/env python3
"""
PNG to SVG Converter

This script converts PNG images to SVG format by embedding the PNG data
as a base64-encoded image within an SVG container.

Usage:
    python png_to_svg_converter.py input.png output.svg
    python png_to_svg_converter.py input.png  # Creates input.svg
    python png_to_svg_converter.py  # Interactive mode
"""

import base64
import os
import sys
from pathlib import Path
from PIL import Image
import argparse


def png_to_svg(png_path, svg_path=None, resize_width=None, resize_height=None):
    """
    Convert a PNG image to SVG format.
    
    Args:
        png_path (str): Path to input PNG file
        svg_path (str, optional): Path to output SVG file. If None, uses PNG name with .svg extension
        resize_width (int, optional): Resize image to this width (maintains aspect ratio if height not specified)
        resize_height (int, optional): Resize image to this height
    
    Returns:
        str: Path to the created SVG file
    
    Raises:
        FileNotFoundError: If the PNG file doesn't exist
        ValueError: If the file is not a valid PNG
    """
    
    # Validate input file
    png_path = Path(png_path)
    if not png_path.exists():
        raise FileNotFoundError(f"PNG file not found: {png_path}")
    
    if not png_path.suffix.lower() == '.png':
        raise ValueError(f"Input file must be a PNG: {png_path}")
    
    # Determine output path
    if svg_path is None:
        svg_path = png_path.with_suffix('.svg')
    else:
        svg_path = Path(svg_path)
    
    try:
        # Open and process the image
        with Image.open(png_path) as img:
            # Get original dimensions
            original_width, original_height = img.size
            
            # Handle resizing
            if resize_width or resize_height:
                if resize_width and resize_height:
                    # Both dimensions specified
                    new_size = (resize_width, resize_height)
                elif resize_width:
                    # Only width specified, maintain aspect ratio
                    aspect_ratio = original_height / original_width
                    new_size = (resize_width, int(resize_width * aspect_ratio))
                else:
                    # Only height specified, maintain aspect ratio
                    aspect_ratio = original_width / original_height
                    new_size = (int(resize_height * aspect_ratio), resize_height)
                
                img = img.resize(new_size, Image.Resampling.LANCZOS)
                width, height = new_size
            else:
                width, height = original_width, original_height
            
            # Convert image to base64
            img_format = 'PNG'
            if img.mode in ('RGBA', 'LA'):
                # Keep transparency for RGBA and LA modes
                pass
            elif img.mode == 'P' and 'transparency' in img.info:
                # Convert palette mode with transparency to RGBA
                img = img.convert('RGBA')
            else:
                # Convert other modes to RGB for smaller file size
                img = img.convert('RGB')
                img_format = 'PNG'  # Keep as PNG to preserve quality
            
            # Save to bytes and encode to base64
            import io
            buffer = io.BytesIO()
            img.save(buffer, format=img_format, optimize=True)
            img_data = buffer.getvalue()
            base64_data = base64.b64encode(img_data).decode('utf-8')
        
        # Create SVG content
        svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" 
     xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{width}" 
     height="{height}" 
     viewBox="0 0 {width} {height}">
  <title>Converted from {png_path.name}</title>
  <image x="0" y="0" 
         width="{width}" 
         height="{height}" 
         xlink:href="data:image/png;base64,{base64_data}"/>
</svg>'''
        
        # Write SVG file
        with open(svg_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        
        print(f"✅ Successfully converted {png_path.name} to {svg_path.name}")
        print(f"   Original size: {original_width}x{original_height}")
        print(f"   Output size: {width}x{height}")
        print(f"   Output file: {svg_path}")
        
        return str(svg_path)
        
    except Exception as e:
        raise ValueError(f"Error processing image {png_path}: {str(e)}")


def batch_convert(input_dir, output_dir=None, resize_width=None, resize_height=None):
    """
    Convert all PNG files in a directory to SVG format.
    
    Args:
        input_dir (str): Directory containing PNG files
        output_dir (str, optional): Output directory. If None, uses input_dir
        resize_width (int, optional): Resize images to this width
        resize_height (int, optional): Resize images to this height
    
    Returns:
        list: List of created SVG file paths
    """
    
    input_path = Path(input_dir)
    if not input_path.exists():
        raise FileNotFoundError(f"Input directory not found: {input_path}")
    
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = input_path
    
    png_files = list(input_path.glob('*.png'))
    if not png_files:
        print(f"No PNG files found in {input_path}")
        return []
    
    created_files = []
    print(f"Found {len(png_files)} PNG files to convert...")
    
    for png_file in png_files:
        try:
            svg_file = output_path / f"{png_file.stem}.svg"
            result = png_to_svg(png_file, svg_file, resize_width, resize_height)
            created_files.append(result)
        except Exception as e:
            print(f"❌ Error converting {png_file.name}: {str(e)}")
    
    print(f"\n✅ Batch conversion complete! Created {len(created_files)} SVG files.")
    return created_files


def interactive_mode():
    """Run the converter in interactive mode."""
    print("=== PNG to SVG Converter ===")
    print()
    
    while True:
        print("Options:")
        print("1. Convert single PNG file")
        print("2. Batch convert all PNG files in a directory")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            png_path = input("Enter PNG file path: ").strip()
            if not png_path:
                print("❌ Please enter a valid file path.")
                continue
                
            svg_path = input("Enter SVG output path (or press Enter for auto): ").strip()
            if not svg_path:
                svg_path = None
            
            # Optional resizing
            resize = input("Resize image? (y/n): ").strip().lower()
            resize_width = resize_height = None
            
            if resize == 'y':
                try:
                    width_input = input("Enter new width (or press Enter to skip): ").strip()
                    height_input = input("Enter new height (or press Enter to skip): ").strip()
                    
                    if width_input:
                        resize_width = int(width_input)
                    if height_input:
                        resize_height = int(height_input)
                except ValueError:
                    print("❌ Invalid dimensions. Proceeding without resizing.")
            
            try:
                png_to_svg(png_path, svg_path, resize_width, resize_height)
            except Exception as e:
                print(f"❌ Error: {str(e)}")
        
        elif choice == '2':
            input_dir = input("Enter directory path containing PNG files: ").strip()
            if not input_dir:
                print("❌ Please enter a valid directory path.")
                continue
                
            output_dir = input("Enter output directory (or press Enter for same directory): ").strip()
            if not output_dir:
                output_dir = None
            
            # Optional resizing
            resize = input("Resize all images? (y/n): ").strip().lower()
            resize_width = resize_height = None
            
            if resize == 'y':
                try:
                    width_input = input("Enter new width (or press Enter to skip): ").strip()
                    height_input = input("Enter new height (or press Enter to skip): ").strip()
                    
                    if width_input:
                        resize_width = int(width_input)
                    if height_input:
                        resize_height = int(height_input)
                except ValueError:
                    print("❌ Invalid dimensions. Proceeding without resizing.")
            
            try:
                batch_convert(input_dir, output_dir, resize_width, resize_height)
            except Exception as e:
                print(f"❌ Error: {str(e)}")
        
        elif choice == '3':
            print("Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")
        
        print("\n" + "="*50 + "\n")


def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(
        description="Convert PNG images to SVG format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python png_to_svg_converter.py image.png                    # Convert single file
  python png_to_svg_converter.py image.png output.svg         # Convert with custom output name
  python png_to_svg_converter.py --batch ./images/            # Convert all PNGs in directory
  python png_to_svg_converter.py image.png --width 500        # Convert and resize to width 500px
  python png_to_svg_converter.py --interactive                # Run in interactive mode
        """
    )
    
    parser.add_argument('input', nargs='?', help='Input PNG file or directory (for batch mode)')
    parser.add_argument('output', nargs='?', help='Output SVG file (optional)')
    parser.add_argument('--batch', action='store_true', help='Batch convert all PNG files in input directory')
    parser.add_argument('--output-dir', help='Output directory for batch conversion')
    parser.add_argument('--width', type=int, help='Resize width (maintains aspect ratio if height not specified)')
    parser.add_argument('--height', type=int, help='Resize height')
    parser.add_argument('--interactive', action='store_true', help='Run in interactive mode')
    
    args = parser.parse_args()
    
    # Interactive mode
    if args.interactive or (not args.input and len(sys.argv) == 1):
        interactive_mode()
        return
    
    # Validate input
    if not args.input:
        parser.error("Input file or directory required (or use --interactive)")
    
    try:
        if args.batch:
            # Batch conversion
            batch_convert(args.input, args.output_dir, args.width, args.height)
        else:
            # Single file conversion
            png_to_svg(args.input, args.output, args.width, args.height)
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
