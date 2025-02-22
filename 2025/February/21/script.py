import numpy as np

## MATRIX:

# Load and display the random matrix
A = np.load('A.npy')

# Print basic information about the matrix
print(f"Matrix shape: {A.shape}")
print(f"Matrix data type: {A.dtype}")
print(f"Matrix memory size: {A.nbytes / 1024:.2f} KB")

# Configure numpy print options for better readability
np.set_printoptions(precision=4, suppress=True, linewidth=120)

print("\nFirst 5 rows of the matrix (showing first 8 columns):")
print(A[:5, :8])

# Print some basic statistics
print("\nMatrix statistics:")
print(f"Min value: {A.min():.4f}")
print(f"Max value: {A.max():.4f}")
print(f"Mean value: {A.mean():.4f}")
print(f"Standard deviation: {A.std():.4f}")

# Optional: If you want to see the full matrix, uncomment this line
print("\nFull matrix:")
print(A[0:-1,0:-1])

## OUTPUT:

# Load the output data
output = np.load('output.npy')

# Print basic information
print(f"Output shape: {output.shape}")
print(f"Output data type: {output.dtype}")
print(f"Number of blocks: {len(output)}")
if len(output) > 0:
    print(f"Length of each block: {len(output[0])}")
print(f"Memory size: {output.nbytes / 1024:.2f} KB")

# Configure numpy print options for better readability
np.set_printoptions(precision=4, suppress=True, linewidth=120)

# Show first few blocks
print("\nFirst 3 transformed blocks:")
for i in range(min(3, len(output))):
    print(f"\nBlock {i}:")
    print(output[i])

# Print some statistics
print("\nStatistics across all blocks:")
output_array = np.array(output)
print(f"Min value: {output_array.min():.4f}")
print(f"Max value: {output_array.max():.4f}")
print(f"Mean value: {output_array.mean():.4f}")
print(f"Standard deviation: {output_array.std():.4f}")

# Calculate how many 8x8 blocks we should have based on dimensions
qr_size = int(np.sqrt(len(output)) * 8)  # Since blocks are 8x8
print(f"\nThis suggests the original QR code was approximately {qr_size}x{qr_size} pixels")