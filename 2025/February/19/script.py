def scytale_decrypt(text, rod_size):
    """Decrypt text using scytale cipher with given rod size."""
    num_columns = (len(text) + rod_size - 1) // rod_size
    result = ''
    
    # Read down each column
    for col in range(num_columns):
        for row in range(rod_size):
            index = row * num_columns + col
            if index < len(text):
                result += text[index]
    
    return result

def analyze_file(filename):
    """Analyze the file with different rod sizes and look for flag patterns."""
    # Read the file
    with open(filename, 'r') as f:
        text = f.read().strip()
    
    print(f"File length: {len(text)}")
    
    # Find factors of text length
    factors = []
    for i in range(1, len(text)):
        if len(text) % i == 0:
            factors.append(i)
    print(f"Factors under 100: {factors}")
    
    # Try decryption with various rod sizes
    test_sizes = []
    
    # Add sizes based on factors
    for factor in factors:
        test_sizes.append(len(text) // factor)
    
    # Add sizes around length/11 (since we know that's promising)
    base_size = len(text) // 11
    for i in range(-5, 6):
        test_sizes.append(base_size + i)
    
    # Remove duplicates and sort
    test_sizes = sorted(list(set(test_sizes)))
    
    print("\nTrying rod sizes...")
    for rod_size in test_sizes:
        decrypted = scytale_decrypt(text, rod_size)
        
        # Look for promising patterns
        patterns = [ 'ictf{', '{the_']
        
        for pattern in patterns:
            if pattern in decrypted:
                print(f"\nFound '{pattern}' with rod size {rod_size}:")
                # Show context around the pattern
                idx = decrypted.index(pattern)
                start = max(0, idx - 20)
                end = min(len(decrypted), idx + 200)
                print(decrypted[start:end])
                
                # Try to extract complete flag if it exists
                if '{' in decrypted:
                    try:
                        flag_start = decrypted.index('{', max(0, idx-5))
                        flag_end = decrypted.index('}', flag_start) + 1
                        print(f"\nPossible flag: {decrypted[flag_start:flag_end]}")
                    except ValueError:
                        pass

if __name__ == "__main__":
    # Usage
    analyze_file('Long_Rods.txt')