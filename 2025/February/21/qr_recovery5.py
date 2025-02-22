import numpy as np
from scipy.fftpack import dct
from PIL import Image

def get_block_pattern(block_i, block_j):
    """
    For an 8x8 block at position (i,j), determine how QR modules intersect
    Returns all possible patterns for this block
    """
    pixel_x = block_j * 8
    pixel_y = block_i * 8
    
    # Create template showing which QR module each pixel belongs to
    template = np.zeros((8, 8), dtype=int)
    for y in range(8):
        for x in range(8):
            qr_y = (pixel_y + y) // 10
            qr_x = (pixel_x + x) // 10
            template[y, x] = qr_y * 1000 + qr_x
    
    # Get unique QR modules this block intersects with
    unique_modules = np.unique(template)
    
    # Generate all possible patterns
    n_modules = len(unique_modules)
    patterns = []
    for bits in range(2**n_modules):
        module_colors = {}
        for i, module_id in enumerate(unique_modules):
            module_colors[module_id] = (bits >> i) & 1
        
        pattern = np.zeros((8, 8))
        for y in range(8):
            for x in range(8):
                module_id = template[y, x]
                pattern[y, x] = module_colors[module_id]
        patterns.append(pattern)
    
    return patterns

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

# Calculate dimensions
blocks_per_side = int(np.sqrt(len(output)))  # Should be 46
qr_size = blocks_per_side * 8  # Should be 368

# Recover the full QR code
print(f"Recovering QR code ({blocks_per_side}x{blocks_per_side} blocks)")
recovered = np.zeros((qr_size, qr_size))

for i in range(blocks_per_side):
    for j in range(blocks_per_side):
        if (i * blocks_per_side + j) % 50 == 0:
            print(f"Processing block ({i},{j})")
            
        block_idx = i * blocks_per_side + j
        patterns = get_block_pattern(i, j)
        best_pattern, error = find_best_pattern(patterns, output[block_idx])
        
        if error > 1e-6:
            print(f"Block ({i},{j}) error: {error}")
            
        recovered[i*8:(i+1)*8, j*8:(j+1)*8] = best_pattern

# Save the result
Image.fromarray(recovered * 255).convert('L').save('recovered_qr_boundaries.png')
print("Done! Saved as recovered_qr_boundaries.png")