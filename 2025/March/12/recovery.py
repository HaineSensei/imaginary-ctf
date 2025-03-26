import numpy as np
from collections import Counter
import string

def load_ciphertexts(filename="out.txt"):
    """Load ciphertexts from the file with triple newline separators."""
    with open(filename, "rb") as f:
        content = f.read()
    
    # Split by triple newlines
    ciphertexts = content.split(b"\n\n\n")
    print(f"Loaded {len(ciphertexts)} ciphertexts")
    return ciphertexts

def analyze_byte_frequency(ciphertexts):
    """Analyze byte frequency at each position across all ciphertexts."""
    # Find the length of the shortest ciphertext
    min_length = min(len(ct) for ct in ciphertexts)
    print(f"Analyzing first {min_length} bytes (shortest ciphertext length)")
    
    # Create array to hold byte frequencies at each position
    byte_freqs = [Counter() for _ in range(min_length)]
    
    # Count frequency of each byte value at each position
    for ct in ciphertexts:
        for i in range(min_length):
            byte_freqs[i][ct[i]] += 1
    
    return byte_freqs, min_length

def xor_bytes(a, b):
    """XOR two bytes."""
    return a ^ b

def recover_flag(byte_freqs, min_length):
    """Try to recover the flag from byte frequencies."""
    flag = bytearray()
    
    # Common flag formats for validation
    flag_formats = [b"flag{", b"FLAG{", b"ctf{", b"CTF{", b"HTB{", b"htb{", b"CHTB{", b"chtb{", b"ictf{"]
    
    # First, we'll try using statistical approaches
    print("Analyzing statistical patterns in ciphertexts...")
    
    # Method 1: Looking for statistical patterns
    # This works on the assumption that XORing the flag with many random streams
    # might produce detectable patterns
    
    # Use the average byte value at each position
    avg_bytes = []
    for i in range(min_length):
        values = list(byte_freqs[i].keys())
        counts = list(byte_freqs[i].values())
        avg = sum(v * c for v, c in zip(values, counts)) / sum(counts)
        avg_bytes.append(int(avg))
    
    print("Method 1 (Average): Possible flag patterns:")
    print(bytes(avg_bytes))
    
    # Method 2: Use the most common byte at each position
    common_bytes = []
    for i in range(min_length):
        common_bytes.append(byte_freqs[i].most_common(1)[0][0])
    
    print("Method 2 (Most Common): Possible flag patterns:")
    print(bytes(common_bytes))
    
    # Method 3: Try brute-force guessing of the first few bytes
    # based on common flag formats, then extend
    print("Method 3 (Format-based): Looking for common flag patterns...")
    
    # For each potential flag format
    for format_start in flag_formats:
        if min_length < len(format_start):
            continue
            
        # Calculate what the key stream would be for this format
        keystream = bytearray()
        for i in range(len(format_start)):
            # For each position, find the most common byte that,
            # when XORed with the format byte, produces a valid flag byte
            most_common = byte_freqs[i].most_common()
            keystream.append(most_common[0][0] ^ format_start[i])
        
        # Now use this keystream to decode the rest
        candidate = bytearray()
        for i in range(min_length):
            if i < len(keystream):
                candidate.append(common_bytes[i] ^ keystream[i % len(keystream)])
            else:
                # For bytes beyond our known format, just use the most common value
                # This is a simplification but might work
                candidate.append(common_bytes[i])
        
        print(f"Trying format {format_start}: {bytes(candidate)}")
        
        # Check if the result looks like a flag (contains printable characters)
        is_printable = all(c in string.printable.encode() for c in candidate)
        if is_printable:
            print(f"Found promising candidate: {bytes(candidate)}")
    
    # Method 4: Visualize the distributions to look for patterns
    # For visual analysis in terminal
    print("\nMethod 4 (Visual): Entropy at each byte position:")
    for i in range(min(8, min_length)):  # Show first 8 positions only
        counts = list(byte_freqs[i].values())
        total = sum(counts)
        entropy = -sum((c/total) * np.log2(c/total) for c in counts if c > 0)
        bars = "#" * int(entropy * 5)
        print(f"Position {i}: Entropy {entropy:.2f} {bars}")
        
    # Return the likely flag candidates    
    return bytes(common_bytes)

def main():
    # Load ciphertexts
    ciphertexts = load_ciphertexts()
    
    # Analyze byte frequencies
    byte_freqs, min_length = analyze_byte_frequency(ciphertexts)
    
    # Try to recover the flag
    flag = recover_flag(byte_freqs, min_length)
    
    print("\nAnalysis complete.")
    print("Examine the output above for possible flag patterns.")
    print("You may need to try different combinations or visual inspection of the byte frequency distribution.")

if __name__ == "__main__":
    main()