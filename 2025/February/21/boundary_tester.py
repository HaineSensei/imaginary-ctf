import numpy as np
from scipy.fftpack import dct

def get_block_pattern(block_i, block_j):
    """
    For an 8x8 block at position (i,j), determine how QR modules intersect
    Returns a template showing which QR module each pixel belongs to
    """
    pixel_x = block_j * 8
    pixel_y = block_i * 8
    
    # Create template showing which QR module each pixel belongs to
    template = np.zeros((8, 8), dtype=int)
    for y in range(8):
        for x in range(8):
            qr_y = (pixel_y + y) // 10
            qr_x = (pixel_x + x) // 10
            template[y, x] = qr_y * 1000 + qr_x  # Unique ID for each QR module
    
    # Get unique QR modules this block intersects with
    unique_modules = np.unique(template)
    
    # Generate all possible patterns
    n_modules = len(unique_modules)
    patterns = []
    for bits in range(2**n_modules):
        # Create a mapping of module ID to color (0 or 1)
        module_colors = {}
        for i, module_id in enumerate(unique_modules):
            module_colors[module_id] = (bits >> i) & 1
        
        # Create the pattern
        pattern = np.zeros((8, 8))
        for y in range(8):
            for x in range(8):
                module_id = template[y, x]
                pattern[y, x] = module_colors[module_id]
        patterns.append(pattern)
    
    return patterns

# Test for a specific block
def transform_pattern(pattern):
    """Apply the same transform as in the challenge"""
    return A @ dct(pattern.flatten(), norm='ortho')

def find_best_pattern(patterns, target_output):
    """Find which pattern best matches the target output"""
    best_error = float('inf')
    best_pattern = None
    
    for pattern in patterns:
        transformed = transform_pattern(pattern)
        error = np.linalg.norm(transformed - target_output)
        if error < best_error:
            best_error = error
            best_pattern = pattern
    
    return best_pattern, best_error

# Load data
A = np.load('A.npy')
output = np.load('output.npy')

# Test for a few blocks
test_blocks = [(0,0), (0,1), (1,1), (7,22)]
for bi, bj in test_blocks:
    print(f"\nTesting block ({bi},{bj}):")
    patterns = get_block_pattern(bi, bj)
    print(f"Found {len(patterns)} possible patterns")
    best_pattern, error = find_best_pattern(patterns, output[bi * 46 + bj])
    print(f"Best pattern error: {error}")
    print("Pattern:")
    print(best_pattern)