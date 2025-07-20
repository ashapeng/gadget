"""
RNA Structure Designer Module

This module provides functionality for designing RNA structures with specific base-pairing rules.
It implements random selection of bases for both paired and unpaired positions following these rules:
1. Only uses standard RNA bases: A, C, G, U
2. Unpaired positions: Random selection from A, C, G, U with equal probability
3. Paired positions: Preferential selection of GC/CG pairs, with limited use of AU/UA pairs

Author: AI RNA Structure Specialist
"""

import random
from typing import List, Tuple, Dict
from dataclasses import dataclass

@dataclass
class RNAStructureParams:
    """Parameters for RNA structure design"""
    sequence_length: int
    structure_pattern: str  # dot-bracket notation

class RNADesigner:
    """
    Main class for designing RNA structures with specific base-pairing rules.
    """
    
    # Define valid base pairs with their relative energies
    BASE_PAIRS = {
        ('G', 'C'): -3.0,  # Stronger base pair
        ('C', 'G'): -3.0,  # Stronger base pair
        ('A', 'U'): -2.0,  # Weaker base pair
        ('U', 'A'): -2.0   # Weaker base pair
    }
    
    # All possible bases for unpaired positions
    UNPAIRED_BASES = ['A', 'C', 'G', 'U']

    def __init__(self, params: RNAStructureParams):
        """
        Initialize the RNA designer with given parameters.
        
        Args:
            params: RNAStructureParams object containing design parameters
        """
        self.params = params
        self._validate_params()

    def _validate_params(self) -> None:
        """Validate the input parameters."""
        if len(self.params.structure_pattern) != self.params.sequence_length:
            raise ValueError("Structure pattern length must match sequence length")
        
        # Check for valid dot-bracket notation
        stack = []
        for char in self.params.structure_pattern:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    raise ValueError("Invalid structure pattern: unmatched brackets")
                stack.pop()
            elif char != '.':
                raise ValueError(f"Invalid character in structure pattern: {char}")
        if stack:
            raise ValueError("Invalid structure pattern: unmatched brackets")

    def _select_random_unpaired_base(self) -> str:
        """Select a random unpaired base with equal probability."""
        return random.choice(self.UNPAIRED_BASES)

    def _select_base_pair(self) -> Tuple[str, str]:
        """
        Select a base pair with preference for GC/CG pairs.
        Returns:
            Tuple of (5' base, 3' base)
        """
        # 70% chance for GC/CG, 30% chance for AU/UA
        if random.random() < 0.7:
            return random.choice([('G', 'C'), ('C', 'G')])
        else:
            return random.choice([('A', 'U'), ('U', 'A')])

    def design_structure(self) -> str:
        """
        Design an RNA structure following the specified rules.
        
        Returns:
            str: The designed RNA sequence
        """
        sequence = ['N'] * self.params.sequence_length
        paired_positions = []
        
        # First pass: identify paired positions
        stack = []
        for i, char in enumerate(self.params.structure_pattern):
            if char == '(':
                stack.append(i)
            elif char == ')':
                if stack:
                    left_pos = stack.pop()
                    paired_positions.append((left_pos, i))

        # Second pass: fill in paired positions
        for left_pos, right_pos in paired_positions:
            base_5p, base_3p = self._select_base_pair()
            sequence[left_pos] = base_5p
            sequence[right_pos] = base_3p

        # Third pass: fill in unpaired positions
        for i, char in enumerate(self.params.structure_pattern):
            if char == '.':
                sequence[i] = self._select_random_unpaired_base()

        return ''.join(sequence)

    def get_structure_info(self, sequence: str) -> Dict:
        """
        Get information about the designed structure.
        
        Args:
            sequence: The designed RNA sequence
            
        Returns:
            Dict containing structure information
        """
        return {
            'sequence': sequence,
            'structure': self.params.structure_pattern,
            'length': len(sequence),
            'gc_content': (sequence.count('G') + sequence.count('C')) / len(sequence),
            'paired_positions': sequence.count('(')
        } 