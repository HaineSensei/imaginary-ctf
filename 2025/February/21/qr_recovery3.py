import numpy as np
from scipy.fftpack import dct, idct
from PIL import Image
import cvxpy as cp

# Load data
A = np.load('A.npy')
output = np.load('output.npy')

def solve_block_l1_binary(A, y, lambda_tv=0.1):
    """
    Solve the compressed sensing problem using L1 minimization
    with binary encouragement and total variation regularization
    """
    n = A.shape[1]
    x = cp.Variable(n)
    
    # L1 norm of DCT coefficients
    l1_norm = cp.norm1(x)
    
    # Measurement constraint
    measurement_error = cp.norm2(A @ x - y)
    
    # Binary encouragement term - pushes values towards -1 or 1
    binary_penalty = cp.sum(cp.multiply(x - 1, x + 1))
    
    # Total variation in 1D (since we're working with flattened blocks)
    tv_norm = cp.norm1(x[1:] - x[:-1])
    
    # Combined objective
    objective = cp.Minimize(l1_norm + binary_penalty + lambda_tv * tv_norm)
    
    # Constraints - allow small measurement error
    constraints = [measurement_error <= 1e-4]
    
    # Solve
    prob = cp.Problem(objective, constraints)
    try:
        prob.solve()
        return x.value
    except:
        print("Warning: Optimization failed for a block, falling back to basic L1")
        # Fallback to basic L1
        objective = cp.Minimize(cp.norm1(x))
        prob = cp.Problem(objective, constraints)
        prob.solve()
        return x.value

def process_block(A, output_block):
    """Process a single output block back to original 8x8 block"""
    # Get DCT coefficients
    dct_coeffs = solve_block_l1_binary(A, output_block)
    
    # Apply inverse DCT
    block = idct(dct_coeffs, norm='ortho')
    
    # Reshape to 8x8
    return block.reshape(8, 8)

def post_process_qr(qr):
    """
    Post-process the QR code to improve quality
    """
    # First normalize to [-1, 1]
    qr = (qr - qr.min()) / (qr.max() - qr.min()) * 2 - 1
    
    # Apply bilateral filter to reduce noise while preserving edges
    from scipy.ndimage import gaussian_filter
    
    # Compute edge weights
    sigma = 1.0
    edge_weights = np.exp(-np.abs(gaussian_filter(qr, sigma)))
    
    # Smooth but preserve edges
    smoothed = gaussian_filter(qr, sigma) * edge_weights + qr * (1 - edge_weights)
    
    # Strong thresholding - use Otsu's method
    from skimage.filters import threshold_otsu
    thresh = threshold_otsu(smoothed)
    binary = smoothed > thresh
    
    return binary.astype(np.uint8) * 255

def recover_qr():
    """Recover the full QR code"""
    n_blocks = len(output)
    blocks_per_side = int(np.sqrt(n_blocks))
    qr_size = blocks_per_side * 8
    full_qr = np.zeros((qr_size, qr_size))
    
    print(f"Processing {n_blocks} blocks...")
    for i in range(blocks_per_side):
        for j in range(blocks_per_side):
            block_idx = i * blocks_per_side + j
            if block_idx % 10 == 0:
                print(f"Block {block_idx}/{n_blocks}")
            full_qr[i*8:(i+1)*8, j*8:(j+1)*8] = process_block(A, output[block_idx])
    
    return full_qr

# Main execution
print("Starting QR code recovery...")
qr = recover_qr()

# Post-process and save
final_qr = post_process_qr(qr)
Image.fromarray(final_qr).save('recovered_qr_improved.png')

print("Done! Saved as recovered_qr_improved.png")