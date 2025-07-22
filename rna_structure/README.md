# RNA Structure Designer

A Python module for designing RNA sequences with specific structural constraints, following established base-pairing rules and energy considerations.

## Features

- Design RNA sequences with custom secondary structures using dot-bracket notation
- Implements biologically relevant base-pairing rules:
  - Uses only standard RNA bases (A, C, G, U)
  - Random selection for unpaired positions
  - Preference for GC/CG pairs over AU/UA pairs due to energy considerations
- Comprehensive input validation
- Detailed structure information including GC content analysis
- Well-documented code with type hints
- Comprehensive test suite

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd rna_structure
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

The module provides a simple interface for designing RNA structures. Here's a basic example:

```python
from rna_designer import RNADesigner, RNAStructureParams

# Create parameters for a simple stem-loop structure
params = RNAStructureParams(
    sequence_length=9,
    structure_pattern="((.....))"  # Two paired bases enclosing 5 unpaired bases
)

# Initialize the designer
designer = RNADesigner(params)

# Generate a sequence
sequence = designer.design_structure()

# Get structure information
info = designer.get_structure_info(sequence)
print(f"Sequence: {info['sequence']}")
print(f"Structure: {info['structure']}")
print(f"GC content: {info['gc_content']:.2f}")
```

See `example.py` for more detailed usage examples.

## Structure Notation

The module uses dot-bracket notation to specify RNA secondary structures:
- `.` represents an unpaired base
- `(` represents a base that pairs with a corresponding `)`
- Matching parentheses must be properly nested

Examples:
- `((....))`: Simple stem-loop with 4 unpaired bases
- `((..((....))..))`: Complex structure with nested stems

## Testing

Run the test suite:
```bash
python -m unittest test_rna_designer.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 