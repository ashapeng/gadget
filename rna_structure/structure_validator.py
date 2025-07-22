"""
RNA Structure Validator and Analyzer
"""

def analyze_structure(structure: str) -> dict:
    """
    Analyze an RNA structure in dot-bracket notation.
    Returns detailed information about the structure and any issues found.
    """
    result = {
        'valid': True,
        'length': len(structure),
        'dots': 0,
        'opening_brackets': 0,
        'closing_brackets': 0,
        'issues': [],
        'stack_trace': []
    }
    
    stack = []
    
    # Check for invalid characters
    invalid_chars = set(structure) - set('.()')
    if invalid_chars:
        result['valid'] = False
        result['issues'].append(f"Invalid characters found: {invalid_chars}")
    
    # Count elements and check bracket matching
    for i, char in enumerate(structure):
        if char == '.':
            result['dots'] += 1
        elif char == '(':
            result['opening_brackets'] += 1
            stack.append(i)
        elif char == ')':
            result['closing_brackets'] += 1
            if not stack:
                result['valid'] = False
                result['issues'].append(f"Unmatched closing bracket at position {i}")
            else:
                opening_pos = stack.pop()
                result['stack_trace'].append((opening_pos, i))
    
    # Check for unmatched opening brackets
    if stack:
        result['valid'] = False
        result['issues'].append(f"Unmatched opening brackets at positions: {stack}")
    
    # Check if brackets are balanced
    if result['opening_brackets'] != result['closing_brackets']:
        result['valid'] = False
        result['issues'].append(
            f"Unbalanced brackets: {result['opening_brackets']} opening vs "
            f"{result['closing_brackets']} closing"
        )
    
    return result

def main():
    # Test the complex structure
    structure = ".....(((.(..(.(((((.((((.((...)))).))))((((((...)).))))..(((...)))...))).)..).)))...................."
    
    print("Analyzing RNA Structure")
    print("=" * 50)
    print(f"Input structure: {structure}")
    print()
    
    analysis = analyze_structure(structure)
    print("Analysis Results:")
    print(f"Length: {analysis['length']}")
    print(f"Unpaired bases (dots): {analysis['dots']}")
    print(f"Opening brackets: {analysis['opening_brackets']}")
    print(f"Closing brackets: {analysis['closing_brackets']}")
    print(f"Valid structure: {analysis['valid']}")
    
    if analysis['issues']:
        print("\nIssues found:")
        for issue in analysis['issues']:
            print(f"- {issue}")
    else:
        print("\nNo issues found. Structure is valid!")
        print(f"\nCorrect Structure String: {structure}")
    
    if analysis['stack_trace']:
        print("\nBase pair positions (opening, closing):")
        for pair in analysis['stack_trace']:
            print(f"({pair[0]}, {pair[1]})")

if __name__ == "__main__":
    main() 