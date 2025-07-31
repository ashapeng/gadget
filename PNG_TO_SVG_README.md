# PNG to SVG Converter

This project provides Python scripts to convert PNG images to SVG format. The conversion embeds the PNG data as base64-encoded content within an SVG container.

## Files

- `png_to_svg_converter.py` - Full-featured converter with command-line interface
- `simple_png_to_svg.py` - Simple converter for basic usage
- `png_to_svg_requirements.txt` - Required Python packages

## Installation

1. Install required dependencies:
```bash
pip install -r png_to_svg_requirements.txt
```

Or install Pillow directly:
```bash
pip install Pillow
```

## Usage

### Full-Featured Converter (`png_to_svg_converter.py`)

#### Command Line Usage

**Convert single file:**
```bash
python png_to_svg_converter.py image.png
python png_to_svg_converter.py image.png output.svg
```

**Batch convert all PNG files in a directory:**
```bash
python png_to_svg_converter.py --batch ./images/
python png_to_svg_converter.py --batch ./images/ --output-dir ./svg_output/
```

**Convert with resizing:**
```bash
python png_to_svg_converter.py image.png --width 500
python png_to_svg_converter.py image.png --width 500 --height 300
```

**Interactive mode:**
```bash
python png_to_svg_converter.py --interactive
```

#### Python API Usage

```python
from png_to_svg_converter import png_to_svg, batch_convert

# Convert single file
png_to_svg('input.png', 'output.svg')

# Convert with resizing
png_to_svg('input.png', 'output.svg', resize_width=500)

# Batch convert
batch_convert('./images/', './svg_output/')
```

### Simple Converter (`simple_png_to_svg.py`)

```python
from simple_png_to_svg import simple_png_to_svg

# Basic conversion
simple_png_to_svg('image.png')  # Creates image.svg
simple_png_to_svg('image.png', 'custom_name.svg')
```

## Features

### Full Converter
- ✅ Single file conversion
- ✅ Batch conversion of entire directories
- ✅ Image resizing (with aspect ratio preservation)
- ✅ Command-line interface
- ✅ Interactive mode
- ✅ Transparency preservation
- ✅ Automatic file naming
- ✅ Error handling and validation
- ✅ Progress reporting

### Simple Converter
- ✅ Basic PNG to SVG conversion
- ✅ Minimal dependencies
- ✅ Easy to integrate into other projects

## How It Works

The converter:
1. Opens the PNG image using Pillow (PIL)
2. Converts the image data to base64 encoding
3. Embeds the base64 data in an SVG `<image>` element
4. Creates a properly formatted SVG file

The resulting SVG files:
- Maintain the original image quality
- Preserve transparency (for RGBA images)
- Can be scaled without quality loss (vector container)
- Are compatible with web browsers and vector graphics software

## Examples

### Convert RNA Structure Image
If you have the RNA structure image in your project:

```python
python simple_png_to_svg.py
# This will automatically convert rna_structure/rna_img.png if it exists
```

### Batch Convert Project Images
```bash
python png_to_svg_converter.py --batch ./rna_structure/ --output-dir ./svg_images/
```

### Interactive Conversion
```bash
python png_to_svg_converter.py
# Follow the prompts to convert images interactively
```

## Output Format

The generated SVG files follow this structure:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" 
     xmlns:xlink="http://www.w3.org/1999/xlink"
     width="WIDTH" height="HEIGHT" 
     viewBox="0 0 WIDTH HEIGHT">
  <title>Converted from FILENAME</title>
  <image x="0" y="0" width="WIDTH" height="HEIGHT" 
         xlink:href="data:image/png;base64,BASE64_DATA"/>
</svg>
```

## Error Handling

The scripts include comprehensive error handling for:
- Missing input files
- Invalid file formats
- Corrupt images
- Permission issues
- Invalid dimensions for resizing

## Limitations

- The output SVG files will be larger than the original PNG due to base64 encoding overhead (approximately 33% larger)
- This method embeds raster data in vector format - it doesn't create true vector graphics
- For true vectorization of images, consider using specialized tools like `autotrace` or `potrace`

## Requirements

- Python 3.6+
- Pillow (PIL) 9.0.0+

## License

This code is provided as-is for educational and practical use.
