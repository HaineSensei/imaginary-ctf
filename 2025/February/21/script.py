import numpy as np

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