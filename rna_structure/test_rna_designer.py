"""
Test suite for the RNA Structure Designer module.
"""

import unittest
from rna_designer import RNADesigner, RNAStructureParams

class TestRNADesigner(unittest.TestCase):
    def setUp(self):
        """Set up test cases."""
        self.simple_params = RNAStructureParams(
            sequence_length=6,
            structure_pattern="((..))"
        )
        self.designer = RNADesigner(self.simple_params)

    def test_structure_validation(self):
        """Test structure pattern validation."""
        # Test invalid length
        with self.assertRaises(ValueError):
            RNADesigner(RNAStructureParams(
                sequence_length=5,
                structure_pattern="((..))"
            ))

        # Test unmatched brackets
        with self.assertRaises(ValueError):
            RNADesigner(RNAStructureParams(
                sequence_length=6,
                structure_pattern="((...))"
            ))

        # Test invalid characters
        with self.assertRaises(ValueError):
            RNADesigner(RNAStructureParams(
                sequence_length=6,
                structure_pattern="((x.))"
            ))

    def test_sequence_generation(self):
        """Test sequence generation."""
        sequence = self.designer.design_structure()
        
        # Test length
        self.assertEqual(len(sequence), 6)
        
        # Test valid bases
        self.assertTrue(all(base in 'ACGU' for base in sequence))
        
        # Test base pairing
        self.assertTrue(
            (sequence[0], sequence[5]) in self.designer.BASE_PAIRS or
            (sequence[5], sequence[0]) in self.designer.BASE_PAIRS
        )
        self.assertTrue(
            (sequence[1], sequence[4]) in self.designer.BASE_PAIRS or
            (sequence[4], sequence[1]) in self.designer.BASE_PAIRS
        )

    def test_structure_info(self):
        """Test structure information generation."""
        sequence = self.designer.design_structure()
        info = self.designer.get_structure_info(sequence)
        
        self.assertEqual(info['length'], 6)
        self.assertEqual(info['structure'], "((..))")
        self.assertEqual(info['paired_positions'], 2)
        
        # Test GC content calculation
        gc_count = sequence.count('G') + sequence.count('C')
        expected_gc_content = gc_count / len(sequence)
        self.assertEqual(info['gc_content'], expected_gc_content)

if __name__ == '__main__':
    unittest.main() 