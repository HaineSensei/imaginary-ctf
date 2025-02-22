import numpy as np
from scipy.fftpack import dct, idct
from PIL import Image
import cvxpy as cp

# Load data
A = np.load('A.npy')
output = np.load('output.npy')

def solve_block_l1_smooth(A, y, lambda_tv=0.1):
    """
    Solve the compressed sensing problem using L1 minimization
    with total variation regularization, but without binary constraints
    """
    n = A.shape[1]
    x = cp.Variable(n)
    
    # L1 norm of DCT coefficients
    l1_norm = cp.norm1(x)
    
    # Total variation in 1D (helps preserve edges while reducing noise)
    tv_norm = cp.norm1(x[1:] - x[:-1])
    
    # Combined objective
    objective = cp.Minimize(l1_norm + lambda_tv * tv_norm)
    
    # Measurement constraints - small error allowed
    constraints = [cp.norm2(A @ x - y) <= 1e-4]
    
    # Solve
    prob = cp.Problem(objective, constraints)
    try:
        prob.solve()
        return x.value
    except:
        print("Warning: Optimization failed for a block, trying with relaxed constraints")
        constraints = [cp.norm2(A @ x - y) <= 1e-3]  # Relaxed constraint
        prob = cp.Problem(objective, constraints)
        prob.solve()
        return x.value

def process_block(A, output_block):
    """Process a single output block back to original 8x8 block"""
    # Get DCT coefficients
    dct_coeffs = solve_block_l1_smooth(A, output_block)
    
    # Apply inverse DCT
    block = idct(dct_coeffs, norm='ortho')
    
    # Reshape to 8x8
    return block.reshape(8, 8)

def post_process_qr(qr):
    """
    Post-process the QR code with more gentle smoothing
    """
    # Normalize to [0, 1] range
    qr = (qr - qr.min()) / (qr.max() - qr.min())
    
    # Apply gentle Gaussian smoothing
    from scipy.ndimage import gaussian_filter
    smoothed = gaussian_filter(qr, sigma=0.7)
    
    # Use local adaptive thresholding
    from skimage.filters import threshold_local
    block_size = 35  # Should be odd and larger than QR module size
    binary = smoothed > threshold_local(smoothed, block_size, offset=0)
    
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

# Post-process and save both versions
print("Post-processing...")
final_qr = post_process_qr(qr)
Image.fromarray(final_qr).save('recovered_qr_fixed.png')

# Also save the raw version before thresholding
raw_qr = ((qr - qr.min()) / (qr.max() - qr.min()) * 255).astype(np.uint8)
Image.fromarray(raw_qr).save('recovered_qr_fixed_raw.png')

print("Done! Saved both processed and raw versions.")