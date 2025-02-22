import numpy as np
from scipy.fftpack import dct, idct
from PIL import Image
import cvxpy as cp

# Load data
A = np.load('A.npy')
output = np.load('output.npy')

def solve_block_l1(A, y):
    """
    Solve the compressed sensing problem using L1 minimization
    A: measurement matrix (20x64)
    y: measurements (length 20)
    Returns: recovered signal (length 64)
    """
    n = A.shape[1]  # length of signal (64)
    x = cp.Variable(n)
    objective = cp.Minimize(cp.norm1(x))
    constraints = [A @ x == y]
    prob = cp.Problem(objective, constraints)
    
    # Solve the problem
    try:
        prob.solve()
        return x.value
    except:
        # If strict equality fails, try with some tolerance
        constraints = [cp.norm2(A @ x - y) <= 1e-4]
        prob = cp.Problem(objective, constraints)
        prob.solve()
        return x.value

def process_block(A, output_block):
    """Process a single output block back to original 8x8 block"""
    # Get DCT coefficients using L1 minimization
    dct_coeffs = solve_block_l1(A, output_block)
    
    # Apply inverse DCT
    block = idct(dct_coeffs, norm='ortho')
    
    # Reshape back to 8x8
    return block.reshape(8, 8)

def recover_qr():
    """Recover the full QR code"""
    # Calculate dimensions
    n_blocks = len(output)
    blocks_per_side = int(np.sqrt(n_blocks))
    qr_size = blocks_per_side * 8
    full_qr = np.zeros((qr_size, qr_size))
    
    # Process blocks with progress indicator
    print(f"Processing {n_blocks} blocks...")
    processed_blocks = []
    for i, block in enumerate(output):
        if i % 10 == 0:
            print(f"Block {i}/{n_blocks}")
        processed_blocks.append(process_block(A, block))
    
    # Reconstruct the full image
    for i in range(blocks_per_side):
        for j in range(blocks_per_side):
            block_idx = i * blocks_per_side + j
            full_qr[i*8:(i+1)*8, j*8:(j+1)*8] = processed_blocks[block_idx]
    
    return full_qr

# Recover and save the QR code
print("Starting QR code recovery...")
qr = recover_qr()
print("QR code shape:", qr.shape)
print("Value range:", qr.min(), "to", qr.max())

# Normalize to 0-255 range
qr_normalized = ((qr - qr.min()) / (qr.max() - qr.min()) * 255).astype(np.uint8)

# Save both raw and thresholded versions
Image.fromarray(qr_normalized).save('recovered_qr_l1.png')

# Also save a thresholded version
threshold = qr_normalized.mean()
qr_binary = (qr_normalized > threshold).astype(np.uint8) * 255
Image.fromarray(qr_binary).save('recovered_qr_l1_binary.png')