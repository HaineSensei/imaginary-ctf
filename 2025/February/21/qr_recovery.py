import numpy as np
from scipy.fftpack import dct, idct
from PIL import Image
import qrcode

# First, load our data
A = np.load('A.npy')  # 20x64 random matrix
output = np.load('output.npy')  # List of transformed blocks

# The process we need to reverse is:
# 1. QR code -> 8x8 blocks -> flattened blocks (64-length)
# 2. DCT on each flattened block
# 3. Multiply each 64-length DCT result by 20x64 matrix A to get 20-length result

# So to reverse, for each 20-length output block we need to:
# 1. Solve system A @ x = output_block where x is 64-length DCT coefficients
# 2. Apply IDCT to get back original flattened block
# 3. Reshape to 8x8
# 4. Combine all blocks back into full QR code

def solve_for_block(A, output_block):
    """
    Solve the underdetermined system A @ x = output_block
    A is 20x64, output_block is length 20, we want x which is length 64
    """
    # Using numpy's least squares solver with regularization
    x, residuals, rank, s = np.linalg.lstsq(A, output_block, rcond=None)
    return x

def process_block(A, output_block):
    """Process a single output block back to original 8x8 block"""
    # Solve system to get DCT coefficients
    dct_coeffs = solve_for_block(A, output_block)
    
    # Apply inverse DCT
    block = idct(dct_coeffs, norm='ortho')
    
    # Reshape back to 8x8
    return block.reshape(8, 8)

def recover_qr():
    """Recover the full QR code"""
    # Calculate dimensions
    n_blocks = len(output)
    blocks_per_side = int(np.sqrt(n_blocks))
    
    # Process all blocks
    processed_blocks = [process_block(A, block) for block in output]
    
    # Reconstruct the full image
    # We need to arrange blocks_per_side × blocks_per_side blocks
    qr_size = blocks_per_side * 8
    full_qr = np.zeros((qr_size, qr_size))
    
    for i in range(blocks_per_side):
        for j in range(blocks_per_side):
            block_idx = i * blocks_per_side + j
            full_qr[i*8:(i+1)*8, j*8:(j+1)*8] = processed_blocks[block_idx]
    
    return full_qr

# Recover and save the QR code
qr = recover_qr()
print("QR code shape:", qr.shape)
print("Value range:", qr.min(), "to", qr.max())

# Save as image
# We'll need to normalize and convert to 0-255 range
qr_normalized = ((qr - qr.min()) / (qr.max() - qr.min()) * 255).astype(np.uint8)
Image.fromarray(qr_normalized).save('recovered_qr.png')