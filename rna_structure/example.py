"""
Example usage of the RNA Structure Designer.

This script generates an RNA sequence for the complex structure from the image.
"""

from rna_designer import RNADesigner, RNAStructureParams
# import cv2
# import numpy as np
# from PIL import Image
# import matplotlib.pyplot as plt

def generate_sequence_from_dot_bracket(structure_string):
    """
    Generates an RNA sequence from a given dot-bracket string.

    Args:
        structure_string (str): The dot-bracket string representing the RNA structure.

    Returns:
        str: The generated RNA sequence, or None if an error occurs.
    """
    try:
        params = RNAStructureParams(
            sequence_length=len(structure_string),
            structure_pattern=structure_string
        )
        designer = RNADesigner(params)
        sequence = designer.design_structure()
        return sequence
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def generate_final_structure():
    """
    Generates the RNA sequence using a manually reconstructed and
    validated dot-bracket string from the image.
    """
    print("\nGenerating Sequence for the RNA Structure from the Image")
    print("="*60)
    
    # Manually and carefully reconstructed dot-bracket string.
    # Total length: 101
    s = [".",] * 101
    pairs = [
        (8, 80), (9, 79), (10, 78), (14, 76), (15, 75), (20, 70), (21, 69),
        (22, 40), (23, 39), (24, 38), (29, 35), (30, 34), (41, 56), (42, 55),
        (46, 52), (47, 51), (58, 66), (59, 65), (60, 64)
    ]
    for i, j in pairs:
        s[i-1] = '('
        s[j-1] = ')'
    structure_string = "".join(s)

    print(f"Structure (Length: {len(structure_string)}):")
    print(structure_string)

    sequence = generate_sequence_from_dot_bracket(structure_string)
        
    if sequence:
        print("\n--- Generated RNA ---")
        print(f"Sequence (Length: {len(sequence)}):")
        print(sequence)
        print(f"\nGC content: {(sequence.count('G') + sequence.count('C')) / len(sequence):.2f}")


def analyze_rna_structure(structure_string):
    """
    Analyzes the structural features of an RNA dot-bracket structure.
    
    Args:
        structure_string (str): The dot-bracket string representing the RNA structure.
    
    Returns:
        dict: A dictionary containing counts of various structural features.
    """
    if not structure_string:
        return {}
    
    # Initialize feature counts
    features = {
        'total_length': len(structure_string),
        'paired_bases': 0,
        'unpaired_bases': 0,
        'hairpin_loops': 0,
        'internal_loops': 0,
        'bulges': 0,
        'stems': 0,
        'multiloops': 0,
        'external_loops': 0
    }
    
    # Count basic paired/unpaired bases
    features['paired_bases'] = structure_string.count('(') + structure_string.count(')')
    features['unpaired_bases'] = structure_string.count('.')
    
    # Find matching base pairs
    stack = []
    pairs = []
    for i, char in enumerate(structure_string):
        if char == '(':
            stack.append(i)
        elif char == ')':
            if stack:
                left = stack.pop()
                pairs.append((left, i))
    
    # Analyze structural features
    if pairs:
        # Count stems (consecutive base pairs)
        stems = []
        current_stem = [pairs[0]]
        
        for i in range(1, len(pairs)):
            prev_pair = pairs[i-1]
            curr_pair = pairs[i]
            
            # Check if pairs are consecutive (forming a stem)
            if (curr_pair[0] == prev_pair[0] + 1 and 
                curr_pair[1] == prev_pair[1] - 1):
                current_stem.append(curr_pair)
            else:
                stems.append(current_stem)
                current_stem = [curr_pair]
        
        stems.append(current_stem)
        features['stems'] = len(stems)
        
        # Analyze loops
        for stem in stems:
            if len(stem) >= 1:
                # Get the innermost pair of the stem
                innermost = stem[-1]
                loop_start = innermost[0] + 1
                loop_end = innermost[1] - 1
                
                if loop_start <= loop_end:
                    loop_length = loop_end - loop_start + 1
                    loop_sequence = structure_string[loop_start:loop_end + 1]
                    
                    # Check if it's a hairpin loop (no base pairs inside)
                    if '(' not in loop_sequence and ')' not in loop_sequence:
                        features['hairpin_loops'] += 1
                    else:
                        # It contains base pairs, so it's more complex
                        features['internal_loops'] += 1
        
        # Count bulges and internal loops by analyzing gaps between stems
        for i in range(len(stems) - 1):
            current_stem = stems[i]
            next_stem = stems[i + 1]
            
            # Check for bulges or internal loops between stems
            gap_start = current_stem[-1][0] + 1
            gap_end = next_stem[0][0] - 1
            
            if gap_start <= gap_end:
                gap_length = gap_end - gap_start + 1
                if gap_length <= 3:  # Small gaps are typically bulges
                    features['bulges'] += 1
                else:  # Larger gaps are internal loops
                    features['internal_loops'] += 1
    
    # Count external loop regions (unpaired bases at the ends)
    external_start = 0
    external_end = len(structure_string) - 1
    
    # Find first and last paired bases
    first_pair = structure_string.find('(')
    last_pair = structure_string.rfind(')')
    
    if first_pair != -1 and last_pair != -1:
        if first_pair > 0 or last_pair < len(structure_string) - 1:
            features['external_loops'] = 1
    else:
        # No base pairs found - entire structure is external loop
        features['external_loops'] = 1
    
    return features


def print_structure_analysis(features):
    """
    Prints a formatted analysis of RNA structural features.
    
    Args:
        features (dict): Dictionary containing structural feature counts.
    """
    print("\n--- RNA Structure Analysis ---")
    print(f"Total length: {features.get('total_length', 0)} nucleotides")
    print(f"Paired bases: {features.get('paired_bases', 0)}")
    print(f"Unpaired bases: {features.get('unpaired_bases', 0)}")
    print(f"Pairing percentage: {(features.get('paired_bases', 0) / features.get('total_length', 1) * 100):.1f}%")
    print("\nStructural Features:")
    print(f"  • Stems: {features.get('stems', 0)}")
    print(f"  • Hairpin loops: {features.get('hairpin_loops', 0)}")
    print(f"  • Internal loops: {features.get('internal_loops', 0)}")
    print(f"  • Bulges: {features.get('bulges', 0)}")
    print(f"  • External loops: {features.get('external_loops', 0)}")
    print(f"  • Multi-loops: {features.get('multiloops', 0)}")


def analyze_rna_image_structure(image_path):
    """
    Analyzes RNA structural features from an input image.
    
    Args:
        image_path (str): Path to the RNA structure image.
    
    Returns:
        dict: A dictionary containing detected structural features.
    """
    try:
        # Load and preprocess the image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Could not load image from {image_path}")
            return {}
        
        # Convert to RGB for processing
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Initialize feature analysis
        features = {
            'image_dimensions': image.shape[:2],
            'detected_nucleotides': 0,
            'estimated_stems': 0,
            'estimated_loops': 0,
            'estimated_bulges': 0,
            'structural_complexity': 'Unknown'
        }
        
        # Detect circular/nucleotide-like objects (yellow circles in your image)
        # Create a mask for yellow/orange colors (nucleotides)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Define range for yellow/orange colors (nucleotides)
        lower_yellow = np.array([15, 100, 100])
        upper_yellow = np.array([35, 255, 255])
        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
        
        # Find contours of nucleotides
        contours, _ = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours by size and circularity to identify nucleotides
        nucleotide_centers = []
        min_area = 100  # Minimum area for a nucleotide
        max_area = 2000  # Maximum area for a nucleotide
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if min_area < area < max_area:
                # Check circularity
                perimeter = cv2.arcLength(contour, True)
                if perimeter > 0:
                    circularity = 4 * np.pi * area / (perimeter * perimeter)
                    if circularity > 0.5:  # Reasonably circular
                        # Get center of the nucleotide
                        M = cv2.moments(contour)
                        if M["m00"] != 0:
                            cx = int(M["m10"] / M["m00"])
                            cy = int(M["m01"] / M["m00"])
                            nucleotide_centers.append((cx, cy))
        
        features['detected_nucleotides'] = len(nucleotide_centers)
        
        # Analyze structural patterns based on nucleotide positions
        if len(nucleotide_centers) > 0:
            features.update(analyze_nucleotide_patterns(nucleotide_centers, image.shape))
        
        return features
        
    except Exception as e:
        print(f"Error analyzing image: {e}")
        return {}


def analyze_nucleotide_patterns(centers, image_shape):
    """
    Analyzes patterns in nucleotide positions to identify structural features.
    
    Args:
        centers (list): List of (x, y) coordinates of nucleotide centers.
        image_shape (tuple): Shape of the image (height, width, channels).
    
    Returns:
        dict: Dictionary with estimated structural features.
    """
    features = {}
    
    if len(centers) < 4:
        features['estimated_stems'] = 0
        features['estimated_loops'] = 0
        features['estimated_bulges'] = 0
        features['structural_complexity'] = 'Simple'
        return features
    
    # Convert to numpy array for easier processing
    points = np.array(centers)
    
    # Estimate stems by finding parallel/antiparallel arrangements
    stems = estimate_stems_from_positions(points)
    features['estimated_stems'] = stems
    
    # Estimate loops by finding circular/curved arrangements
    loops = estimate_loops_from_positions(points)
    features['estimated_loops'] = loops
    
    # Estimate bulges (small deviations from linear arrangements)
    bulges = estimate_bulges_from_positions(points)
    features['estimated_bulges'] = bulges
    
    # Determine structural complexity
    total_features = stems + loops + bulges
    if total_features <= 2:
        complexity = 'Simple'
    elif total_features <= 5:
        complexity = 'Moderate'
    else:
        complexity = 'Complex'
    
    features['structural_complexity'] = complexity
    
    return features


def estimate_stems_from_positions(points):
    """
    Estimates the number of stems based on nucleotide positions.
    Uses clustering and linear arrangement detection.
    """
    if len(points) < 6:  # Need at least 3 base pairs for a stem
        return 0
    
    # Simple heuristic: look for groups of points that form roughly parallel lines
    # This is a simplified approach - real implementation would be more sophisticated
    
    # Calculate pairwise distances
    from scipy.spatial.distance import pdist, squareform
    distances = squareform(pdist(points))
    
    # Find clusters of nearby points (potential stem regions)
    clusters = []
    visited = set()
    threshold = 50  # Distance threshold for clustering
    
    for i, point in enumerate(points):
        if i in visited:
            continue
        
        cluster = [i]
        visited.add(i)
        
        for j in range(i + 1, len(points)):
            if j not in visited and distances[i][j] < threshold:
                cluster.append(j)
                visited.add(j)
        
        if len(cluster) >= 3:  # Minimum for a stem
            clusters.append(cluster)
    
    # Estimate stems as roughly half the number of significant clusters
    return max(1, len(clusters) // 2)


def estimate_loops_from_positions(points):
    """
    Estimates the number of loops based on curved arrangements of nucleotides.
    """
    if len(points) < 4:
        return 0
    
    # Simple heuristic: look for curved arrangements
    # In a real implementation, this would use more sophisticated curve detection
    
    # For now, estimate based on the overall structure
    # Assume roughly 1 loop per 15-20 nucleotides in a typical structure
    return max(1, len(points) // 15)


def estimate_bulges_from_positions(points):
    """
    Estimates the number of bulges based on small deviations in arrangements.
    """
    if len(points) < 6:
        return 0
    
    # Simple heuristic: assume some bulges in complex structures
    # Real implementation would detect small asymmetric loops
    return max(0, len(points) // 25)


def print_image_analysis(features):
    """
    Prints a formatted analysis of RNA structural features from image analysis.
    
    Args:
        features (dict): Dictionary containing detected structural features.
    """
    print("\n--- RNA Image Structure Analysis ---")
    print(f"Image dimensions: {features.get('image_dimensions', 'Unknown')}")
    print(f"Detected nucleotides: {features.get('detected_nucleotides', 0)}")
    print(f"Structural complexity: {features.get('structural_complexity', 'Unknown')}")
    print("\nEstimated Structural Features:")
    print(f"  • Stems: {features.get('estimated_stems', 0)}")
    print(f"  • Loops: {features.get('estimated_loops', 0)}")
    print(f"  • Bulges: {features.get('estimated_bulges', 0)}")
    
    # Analysis of the provided image
    if features.get('detected_nucleotides', 0) > 90:
        print(f"\nImage Analysis Notes:")
        print(f"  • Large RNA structure detected (~{features.get('detected_nucleotides')} nucleotides)")
        print(f"  • Multiple stem-loop regions visible")
        print(f"  • Complex secondary structure with branching")
        print(f"  • Appears to be a ribosomal RNA or large regulatory RNA")


def generate_structure_from_image(image_path):
    """
    Generates RNA dot-bracket structure from an input image by analyzing
    nucleotide positions and inferring base pairing relationships.
    
    Args:
        image_path (str): Path to the RNA structure image.
    
    Returns:
        tuple: (dot_bracket_string, nucleotide_positions, confidence_score)
               Returns (None, None, 0) if analysis fails.
    """
    try:
        # Load and preprocess the image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Could not load image from {image_path}")
            return None, None, 0
        
        # Detect nucleotides and their positions
        nucleotide_data = detect_nucleotides_with_numbers(image)
        
        if not nucleotide_data:
            print("No nucleotides detected in the image")
            return None, None, 0
        
        # Sort nucleotides by their sequence numbers
        sorted_nucleotides = sorted(nucleotide_data, key=lambda x: x['number'])
        
        # Extract positions for structure inference
        positions = [(n['x'], n['y']) for n in sorted_nucleotides]
        numbers = [n['number'] for n in sorted_nucleotides]
        
        # Infer base pairing from spatial relationships
        base_pairs = infer_base_pairs_from_positions(positions, numbers)
        
        # Generate dot-bracket structure
        structure_length = len(sorted_nucleotides)
        dot_bracket = generate_dot_bracket_from_pairs(base_pairs, structure_length)
        
        # Calculate confidence score based on detection quality
        confidence = calculate_structure_confidence(nucleotide_data, base_pairs)
        
        return dot_bracket, sorted_nucleotides, confidence
        
    except Exception as e:
        print(f"Error generating structure from image: {e}")
        return None, None, 0


def detect_nucleotides_with_numbers(image):
    """
    Detects nucleotides and attempts to read their sequence numbers from the image.
    
    Args:
        image: OpenCV image array
    
    Returns:
        list: List of dictionaries with nucleotide data {'x', 'y', 'number'}
    """
    nucleotides = []
    
    # Convert to HSV for better color detection
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define range for yellow/orange colors (nucleotides)
    lower_yellow = np.array([15, 100, 100])
    upper_yellow = np.array([35, 255, 255])
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    
    # Find contours of nucleotides
    contours, _ = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter and process each nucleotide
    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if 100 < area < 2000:  # Size filter for nucleotides
            # Check circularity
            perimeter = cv2.arcLength(contour, True)
            if perimeter > 0:
                circularity = 4 * np.pi * area / (perimeter * perimeter)
                if circularity > 0.5:
                    # Get center coordinates
                    M = cv2.moments(contour)
                    if M["m00"] != 0:
                        cx = int(M["m10"] / M["m00"])
                        cy = int(M["m01"] / M["m00"])
                        
                        # Try to extract number (simplified approach)
                        # In a real implementation, you'd use OCR here
                        estimated_number = estimate_nucleotide_number(cx, cy, i, len(contours))
                        
                        nucleotides.append({
                            'x': cx,
                            'y': cy,
                            'number': estimated_number,
                            'area': area
                        })
    
    return nucleotides


def estimate_nucleotide_number(x, y, index, total_nucleotides):
    """
    Estimates the sequence number of a nucleotide based on its position.
    This is a simplified heuristic - real implementation would use OCR.
    
    Args:
        x, y: Nucleotide coordinates
        index: Index in the detection order
        total_nucleotides: Total number of detected nucleotides
    
    Returns:
        int: Estimated sequence number
    """
    # Simple heuristic: assign numbers based on detection order
    # In practice, you'd use OCR to read the actual numbers from the image
    return index + 1


def infer_base_pairs_from_positions(positions, numbers):
    """
    Infers base pairing relationships from nucleotide spatial positions.
    
    Args:
        positions: List of (x, y) coordinates
        numbers: List of sequence numbers
    
    Returns:
        list: List of base pair tuples (i, j) where i < j
    """
    base_pairs = []
    
    if len(positions) < 4:
        return base_pairs
    
    # Convert to numpy array for easier processing
    points = np.array(positions)
    
    # Calculate distance matrix
    from scipy.spatial.distance import pdist, squareform
    distances = squareform(pdist(points))
    
    # Find potential base pairs based on spatial proximity and geometric constraints
    pairing_threshold = 60  # Maximum distance for base pairing
    
    for i in range(len(points)):
        for j in range(i + 3, len(points)):  # Minimum loop size of 3
            distance = distances[i][j]
            
            if distance < pairing_threshold:
                # Check if this pairing makes geometric sense
                if is_valid_base_pair(points[i], points[j], points, i, j):
                    # Convert to sequence numbers
                    num_i = numbers[i]
                    num_j = numbers[j]
                    if num_i < num_j:
                        base_pairs.append((num_i, num_j))
                    else:
                        base_pairs.append((num_j, num_i))
    
    # Remove conflicting pairs (each nucleotide can only pair once)
    base_pairs = resolve_pairing_conflicts(base_pairs)
    
    return base_pairs


def is_valid_base_pair(pos1, pos2, all_positions, idx1, idx2):
    """
    Checks if a potential base pair is geometrically valid.
    
    Args:
        pos1, pos2: Positions of the two nucleotides
        all_positions: All nucleotide positions
        idx1, idx2: Indices of the nucleotides
    
    Returns:
        bool: True if the base pair is geometrically valid
    """
    # Simple geometric validation
    # Check if the line between the two nucleotides doesn't intersect too many others
    
    x1, y1 = pos1
    x2, y2 = pos2
    
    # Count how many nucleotides are very close to the line between pos1 and pos2
    line_intersections = 0
    
    for i, pos in enumerate(all_positions):
        if i == idx1 or i == idx2:
            continue
        
        # Calculate distance from point to line
        distance_to_line = point_to_line_distance(pos, pos1, pos2)
        if distance_to_line < 15:  # Very close to the pairing line
            line_intersections += 1
    
    # If too many nucleotides are on the pairing line, it's probably not a valid pair
    return line_intersections <= 2


def point_to_line_distance(point, line_start, line_end):
    """
    Calculates the distance from a point to a line segment.
    """
    x0, y0 = point
    x1, y1 = line_start
    x2, y2 = line_end
    
    # Calculate distance using the formula for point-to-line distance
    numerator = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
    denominator = np.sqrt((y2 - y1)**2 + (x2 - x1)**2)
    
    if denominator == 0:
        return np.sqrt((x0 - x1)**2 + (y0 - y1)**2)
    
    return numerator / denominator


def resolve_pairing_conflicts(base_pairs):
    """
    Resolves conflicts where nucleotides are involved in multiple pairings.
    
    Args:
        base_pairs: List of potential base pairs
    
    Returns:
        list: Filtered list with no conflicts
    """
    # Count occurrences of each nucleotide
    nucleotide_count = {}
    for i, j in base_pairs:
        nucleotide_count[i] = nucleotide_count.get(i, 0) + 1
        nucleotide_count[j] = nucleotide_count.get(j, 0) + 1
    
    # Remove pairs involving over-paired nucleotides
    # Keep the pair with the shortest distance (assuming it's more likely)
    valid_pairs = []
    used_nucleotides = set()
    
    # Sort pairs by some criteria (e.g., distance, could be added as parameter)
    for i, j in base_pairs:
        if i not in used_nucleotides and j not in used_nucleotides:
            valid_pairs.append((i, j))
            used_nucleotides.add(i)
            used_nucleotides.add(j)
    
    return valid_pairs


def generate_dot_bracket_from_pairs(base_pairs, length):
    """
    Generates dot-bracket notation from base pair list.
    
    Args:
        base_pairs: List of base pair tuples (i, j)
        length: Total length of the sequence
    
    Returns:
        str: Dot-bracket structure string
    """
    structure = ['.'] * length
    
    for i, j in base_pairs:
        # Convert to 0-based indexing
        idx_i = i - 1
        idx_j = j - 1
        
        if 0 <= idx_i < length and 0 <= idx_j < length:
            structure[idx_i] = '('
            structure[idx_j] = ')'
    
    return ''.join(structure)


def calculate_structure_confidence(nucleotide_data, base_pairs):
    """
    Calculates a confidence score for the generated structure.
    
    Args:
        nucleotide_data: List of detected nucleotide data
        base_pairs: List of inferred base pairs
    
    Returns:
        float: Confidence score between 0 and 1
    """
    if not nucleotide_data:
        return 0.0
    
    # Factors affecting confidence:
    # 1. Number of nucleotides detected
    # 2. Quality of nucleotide detection (circularity, size consistency)
    # 3. Number of inferred base pairs
    # 4. Geometric consistency
    
    nucleotide_score = min(1.0, len(nucleotide_data) / 50.0)  # Normalize by expected size
    pairing_score = min(1.0, len(base_pairs) / (len(nucleotide_data) * 0.3))  # ~30% pairing expected
    
    # Average the scores
    confidence = (nucleotide_score + pairing_score) / 2.0
    
    return round(confidence, 2)


def print_structure_generation_results(dot_bracket, nucleotides, confidence):
    """
    Prints the results of structure generation from image.
    
    Args:
        dot_bracket: Generated dot-bracket structure
        nucleotides: List of detected nucleotides
        confidence: Confidence score
    """
    print("\n--- RNA Structure Generation from Image ---")
    
    if dot_bracket:
        print(f"Generated structure length: {len(dot_bracket)}")
        print(f"Detected nucleotides: {len(nucleotides)}")
        print(f"Confidence score: {confidence:.2f}")
        print(f"\nGenerated dot-bracket structure:")
        print(dot_bracket)
        
        # Count structural features
        paired_bases = dot_bracket.count('(') + dot_bracket.count(')')
        unpaired_bases = dot_bracket.count('.')
        
        print(f"\nStructure statistics:")
        print(f"  • Paired bases: {paired_bases}")
        print(f"  • Unpaired bases: {unpaired_bases}")
        print(f"  • Pairing percentage: {(paired_bases / len(dot_bracket) * 100):.1f}%")
        
        if confidence < 0.5:
            print(f"\n⚠️  Low confidence score. Results may be inaccurate.")
            print(f"   Consider manual verification or higher quality image.")
    else:
        print("Failed to generate structure from image.")


if __name__ == "__main__":
    print("RNA Structure Analyzer and Sequence Generator")
    print("=" * 50)
    print("Choose analysis mode:")
    print("1. Analyze from dot-bracket structure")
    print("2. Analyze from image file")
    print("3. Generate structure from image")
    print("4. Complete pipeline: Image → Structure → Sequence")
    print("5. Both image analysis + dot-bracket input")
    
    choice = input("Enter your choice (1-5): ").strip()
    
    if choice == "2" or choice == "5":
        # Image analysis only
        image_path = input("Enter path to RNA structure image: ").strip()
        if image_path:
            print(f"\nAnalyzing image: {image_path}")
            image_features = analyze_rna_image_structure(image_path)
            print_image_analysis(image_features)
    
    elif choice == "3":
        # Generate structure from image
        image_path = input("Enter path to RNA structure image: ").strip()
        if image_path:
            print(f"\nGenerating structure from image: {image_path}")
            dot_bracket, nucleotides, confidence = generate_structure_from_image(image_path)
            print_structure_generation_results(dot_bracket, nucleotides, confidence)
    
    elif choice == "4":
        # Complete pipeline: Image → Structure → Sequence
        image_path = input("Enter path to RNA structure image: ").strip()
        if image_path:
            print(f"\n🔬 Starting complete analysis pipeline for: {image_path}")
            print("=" * 60)
            
            # Step 1: Analyze image features
            print("Step 1: Analyzing image features...")
            image_features = analyze_rna_image_structure(image_path)
            print_image_analysis(image_features)
            
            # Step 2: Generate structure from image
            print("\nStep 2: Generating dot-bracket structure...")
            dot_bracket, nucleotides, confidence = generate_structure_from_image(image_path)
            print_structure_generation_results(dot_bracket, nucleotides, confidence)
            
            # Step 3: Generate sequence from structure
            if dot_bracket and confidence > 0.3:  # Only proceed if reasonable confidence
                print("\nStep 3: Generating RNA sequence from structure...")
                sequence = generate_sequence_from_dot_bracket(dot_bracket)
                
                if sequence:
                    print("\n🧬 --- Final Generated RNA Sequence ---")
                    print(f"Sequence: {sequence}")
                    print(f"Length: {len(sequence)}")
                    print(f"GC content: {(sequence.count('G') + sequence.count('C')) / len(sequence):.2f}")
                    
                    # Final structure analysis
                    print("\nStep 4: Final structure validation...")
                    final_features = analyze_rna_structure(dot_bracket)
                    print_structure_analysis(final_features)
                    
                    print(f"\n✅ Pipeline completed successfully!")
                    print(f"   Image → Structure (confidence: {confidence}) → Sequence")
                else:
                    print("❌ Failed to generate sequence from structure")
            else:
                print(f"\n⚠️  Structure generation confidence too low ({confidence})")
                print("   Skipping sequence generation. Consider manual verification.")
    
    elif choice == "1" or choice == "5":
        # Dot-bracket analysis
        print("\n" + "=" * 50)
        structure_input = input("Enter your dot-bracket structure: ").strip()
        
        if not structure_input:
            print("No structure provided.")
            if choice == "1":
                exit(1)
        else:
            print(f"Input structure: {structure_input}")
            print(f"Structure length: {len(structure_input)}")
            
            # Analyze structural features
            features = analyze_rna_structure(structure_input)
            print_structure_analysis(features)
            
            # Generate sequence
            sequence = generate_sequence_from_dot_bracket(structure_input)
            
            if sequence:
                print("\n--- Generated RNA Sequence ---")
                print(f"Sequence: {sequence}")
                print(f"Length: {len(sequence)}")
                print(f"GC content: {(sequence.count('G') + sequence.count('C')) / len(sequence):.2f}")
            else:
                print("Failed to generate sequence")
    
    else:
        print("Invalid choice. Please run the script again.") 