import numpy as np
from scipy.fftpack import dct
import qrcode

# Load output to get number of blocks
output = np.load('output.npy')
n_blocks = len(output)
blocks_per_side = int(np.sqrt(n_blocks))
pixel_size = blocks_per_side * 8

print(f"Number of blocks: {n_blocks}")
print(f"Blocks per side: {blocks_per_side}")
print(f"Total pixel size: {pixel_size}x{pixel_size}")

# Let's try a few versions to see which matches
for version in range(1, 11):  # Try versions 1-10
    qr = qrcode.QRCode(
        version=version,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data("ictf{test}")  # Use dummy flag to see size
    qr.make(fit=True)
    img = np.array(qr.make_image())
    print(f"Version {version}: {img.shape[0]}x{img.shape[1]} pixels")