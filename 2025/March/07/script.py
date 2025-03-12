#!/usr/bin/env python3
import binascii
import numpy as np
import time
from base64 import b64encode
from hashlib import md5, sha3_256
from zlib import crc32

def magic_hash(x):
    """Calculate the magic hash as defined in the challenge"""
    h = md5(x).digest()
    h += crc32(h + x).to_bytes(4, "little")
    return sha3_256(h).digest()

def hex_to_bytes(hex_str):
    """Convert hexadecimal string to bytes, removing spaces"""
    return binascii.unhexlify(hex_str.replace(" ", ""))

def calculate_crc32_basis_vectors(initial_crc, length=4):
    """
    Calculate basis vectors for CRC32 linear space.
    Each vector shows how a specific byte at a specific position affects the CRC32 value.
    """
    basis_vectors = []
    
    # CRC32 polynomial (reversed)
    poly = 0xEDB88320
    
    # Create CRC32 lookup table
    crc_table = []
    for i in range(256):
        crc = i
        for j in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ poly
            else:
                crc = crc >> 1
        crc_table.append(crc)
    
    # For each position in the suffix
    for pos in range(length):
        # For each possible byte value (0-255)
        pos_vectors = []
        for val in range(256):
            # Calculate how this byte affects the CRC32
            crc = initial_crc
            
            # Skip to the position (simulating preceding zeros)
            for _ in range(pos):
                crc = ((crc >> 8) ^ crc_table[(crc ^ 0) & 0xFF])
            
            # Apply the actual byte
            crc = ((crc >> 8) ^ crc_table[(crc ^ val) & 0xFF])
            
            # Complete with trailing zeros if needed
            for _ in range(length - pos - 1):
                crc = ((crc >> 8) ^ crc_table[(crc ^ 0) & 0xFF])
            
            pos_vectors.append((val, crc))
        
        basis_vectors.append(pos_vectors)
    
    return basis_vectors

def find_collision_linear_algebra():
    """Find a magic_hash collision using linear algebra approach"""
    
    # These are Wang's MD5 collision blocks
    m1_hex = (
        "d131dd02c5e6eec4693d9a0698aff95c"
        "2fcab58712467eab4004583eb8fb7f89"
        "55ad340609f4b30283e488832571415a"
        "085125e8f7cdc99fd91dbdf280373c5b"
        "d8823e3156348f5bae6dacd436c919c6"
        "dd53e2b487da03fd02396306d248cda0"
        "e99f33420f577ee8ce54b67080a80d1e"
        "c69821bcb6a8839396f9652b6ff72a70"
    )
    
    m2_hex = (
        "d131dd02c5e6eec4693d9a0698aff95c"
        "2fcab50712467eab4004583eb8fb7f89"
        "55ad340609f4b30283e4888325f1415a"
        "085125e8f7cdc99fd91dbd7280373c5b"
        "d8823e3156348f5bae6dacd436c919c6"
        "dd53e23487da03fd02396306d248cda0"
        "e99f33420f577ee8ce54b67080280d1e"
        "c69821bcb6a8839396f965ab6ff72a70"
    )
    
    m1 = hex_to_bytes(m1_hex)
    m2 = hex_to_bytes(m2_hex)
    
    # Verify they produce an MD5 collision
    common_md5 = md5(m1).digest()
    if md5(m2).digest() != common_md5:
        print("Error: The provided blocks don't produce an MD5 collision!")
        return None, None
    
    print(f"Confirmed MD5 collision: {common_md5.hex()}")
    
    # Calculate original CRC32 values
    crc1 = crc32(common_md5 + m1)
    crc2 = crc32(common_md5 + m2)
    
    print(f"Original CRC32 values: {crc1} (0x{crc1:08x}) vs {crc2} (0x{crc2:08x})")
    
    # Calculate the difference we need to eliminate
    crc_diff = crc1 ^ crc2
    print(f"CRC32 difference (XOR): 0x{crc_diff:08x}")
    
    start_time = time.time()
    
    # Let's try various suffix lengths
    for suffix_length in range(1, 9):
        print(f"\nTrying with suffix length {suffix_length}...")
        
        # Calculate basis vectors for both CRCs
        print("Calculating CRC32 basis vectors...")
        basis1 = calculate_crc32_basis_vectors(crc1, suffix_length)
        
        # For each position, create a mapping of CRC32 results to byte values
        crc_maps = []
        for pos in range(suffix_length):
            crc_map = {}
            for val, resulting_crc in basis1[pos]:
                # Store the value that produces this CRC
                crc_map[resulting_crc] = val
            crc_maps.append(crc_map)
        
        # Now, systematically search for a solution using the basis vectors
        print("Searching for CRC32-canceling suffix...")
        
        # Try combinations of basis vectors
        for i in range(256**suffix_length):
            if i % 1000000 == 0 and i > 0:
                print(f"  Tried {i:,} combinations...")
            
            # Convert i to a list of bytes
            suffix = []
            temp = i
            for _ in range(suffix_length):
                suffix.append(temp % 256)
                temp //= 256
            
            # Calculate how this suffix affects both CRCs
            suffix_bytes = bytes(suffix)
            new_m1 = m1 + suffix_bytes
            new_m2 = m2 + suffix_bytes
            
            # Verify MD5 collision is preserved
            if md5(new_m1).digest() != md5(new_m2).digest():
                # This shouldn't happen with identical suffixes
                print("Error: MD5 collision broken!")
                continue
            
            # Calculate new CRC32 values
            new_md5 = md5(new_m1).digest()
            new_crc1 = crc32(new_md5 + new_m1)
            new_crc2 = crc32(new_md5 + new_m2)
            
            if new_crc1 == new_crc2:
                elapsed = time.time() - start_time
                print(f"Found collision with suffix {suffix_bytes.hex()} after {elapsed:.2f} seconds!")
                return new_m1, new_m2
            
            # If the search space is too large, use a smarter approach
            if i >= 1000000 and suffix_length > 2:
                break
        
        # If brute force is too slow, try a more directed approach
        if suffix_length >= 3:
            print("Using directed search based on CRC32 properties...")
            
            # For each position, calculate how bytes at that position affect the CRC
            effect_table = []
            for pos in range(suffix_length):
                effects = {}
                for val in range(256):
                    # Create a suffix with just this byte at this position
                    test_suffix = bytearray([0] * suffix_length)
                    test_suffix[pos] = val
                    
                    # See how it affects the CRC difference
                    test_m1 = m1 + bytes(test_suffix)
                    test_m2 = m2 + bytes(test_suffix)
                    
                    test_md5 = md5(test_m1).digest()
                    test_crc1 = crc32(test_md5 + test_m1)
                    test_crc2 = crc32(test_md5 + test_m2)
                    
                    # Store the effect on the CRC difference
                    effect = test_crc1 ^ test_crc2
                    effects[val] = effect
                
                effect_table.append(effects)
            
            # Now try to find a combination of bytes that cancels out the CRC difference
            # Use a greedy approach for larger suffix lengths
            for _ in range(1000):  # Try multiple starting points
                suffix = bytearray([0] * suffix_length)
                
                # Start with random values
                for pos in range(suffix_length):
                    suffix[pos] = np.random.randint(0, 256)
                
                # Iteratively improve each position
                for iteration in range(10):
                    for pos in range(suffix_length):
                        # Try all possible values at this position
                        best_val = suffix[pos]
                        best_diff = crc_diff
                        
                        for val in range(256):
                            # Temporarily change this byte
                            old_val = suffix[pos]
                            suffix[pos] = val
                            
                            # Calculate new CRCs
                            test_m1 = m1 + bytes(suffix)
                            test_m2 = m2 + bytes(suffix)
                            
                            test_md5 = md5(test_m1).digest()
                            test_crc1 = crc32(test_md5 + test_m1)
                            test_crc2 = crc32(test_md5 + test_m2)
                            
                            # Calculate new difference
                            new_diff = test_crc1 ^ test_crc2
                            
                            # If this is better, keep it
                            if bin(new_diff).count('1') < bin(best_diff).count('1'):
                                best_val = val
                                best_diff = new_diff
                            
                            # If we found a match, we're done
                            if new_diff == 0:
                                elapsed = time.time() - start_time
                                print(f"Found collision with suffix {bytes(suffix).hex()} after {elapsed:.2f} seconds!")
                                return test_m1, test_m2
                            
                            # Restore the original value
                            suffix[pos] = old_val
                        
                        # Update with the best value found
                        suffix[pos] = best_val
                
                # Check if we found a solution
                test_m1 = m1 + bytes(suffix)
                test_m2 = m2 + bytes(suffix)
                
                test_md5 = md5(test_m1).digest()
                test_crc1 = crc32(test_md5 + test_m1)
                test_crc2 = crc32(test_md5 + test_m2)
                
                if test_crc1 == test_crc2:
                    elapsed = time.time() - start_time
                    print(f"Found collision with directed search after {elapsed:.2f} seconds!")
                    return test_m1, test_m2
    
    # Try a different approach - aligning to MD5 block boundaries
    # MD5 processes data in 64-byte blocks
    # By adding padding to align with block boundaries, we might get more predictable behavior
    print("\nTrying MD5 block-aligned approach...")
    
    for padding_blocks in range(1, 3):
        padding_size = (64 - (len(m1) % 64)) % 64
        if padding_size == 0 and padding_blocks > 0:
            padding_size = 64
        
        padding_size += 64 * (padding_blocks - 1)
        
        print(f"Using padding of size {padding_size} to align with MD5 blocks")
        
        # Try different padding patterns
        for pattern_type in range(4):
            for base_val in range(0, 256, 32):  # Try different base values
                # Generate padding pattern
                padding = bytearray()
                
                if pattern_type == 0:
                    # Simple repeated pattern
                    for i in range(padding_size):
                        padding.append((base_val + i) % 256)
                
                elif pattern_type == 1:
                    # Pattern based on CRC difference
                    for i in range(padding_size):
                        padding.append((base_val + ((crc_diff >> (8 * (i % 4))) & 0xFF)) % 256)
                
                elif pattern_type == 2:
                    # Alternating pattern
                    for i in range(padding_size):
                        if i % 2 == 0:
                            padding.append(base_val)
                        else:
                            padding.append(255 - base_val)
                
                else:
                    # Random but consistent pattern
                    import random
                    random.seed(base_val)
                    for i in range(padding_size):
                        padding.append(random.randint(0, 255))
                
                # Apply padding to both messages
                padded_m1 = m1 + bytes(padding)
                padded_m2 = m2 + bytes(padding)
                
                # Verify MD5 collision is preserved
                padded_md5 = md5(padded_m1).digest()
                if padded_md5 != md5(padded_m2).digest():
                    print("Error: MD5 collision broken by padding!")
                    continue
                
                # Calculate CRC32 values
                padded_crc1 = crc32(padded_md5 + padded_m1)
                padded_crc2 = crc32(padded_md5 + padded_m2)
                
                if padded_crc1 == padded_crc2:
                    elapsed = time.time() - start_time
                    print(f"Found collision with block-aligned padding after {elapsed:.2f} seconds!")
                    return padded_m1, padded_m2
            
            print(f"  Tried pattern type {pattern_type}...")
    
    return None, None

if __name__ == "__main__":
    print("=== Linear Algebra Based Magic Hash Collision Finder ===")
    
    try:
        m1, m2 = find_collision_linear_algebra()
        
        # Verify and output the collision
        if m1 is not None and m2 is not None:
            print("\nVerifying collision...")
            h1 = magic_hash(m1)
            h2 = magic_hash(m2)
            
            if h1 == h2 and m1 != m2 and max(len(m1), len(m2)) <= 4321:
                print("✓ Verification successful! Found valid collision.")
                print(f"m1 length: {len(m1)} bytes")
                print(f"m2 length: {len(m2)} bytes")
                print(f"m1: {b64encode(m1).decode()}")
                print(f"m2: {b64encode(m2).decode()}")
            else:
                print("✗ Verification failed.")
                if h1 != h2:
                    print("  The magic hashes don't match.")
                if m1 == m2:
                    print("  The messages are identical.")
                if max(len(m1), len(m2)) > 4321:
                    print("  Messages exceed length limit of 4321 bytes.")
        else:
            print("\nNo collision found.")
    
    except KeyboardInterrupt:
        print("\nSearch interrupted by user.")