from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import json
import numpy as np
import time

def solve_linear_system(A, b):
    """
    Solve the linear system to find the bits of a.
    
    The system is:
    For each bit i of a:
      if a[i] == 1: b ^= A[i]
    
    This means we're looking for a subset of A that XORs to b.
    Since we're working with XOR, we're essentially solving a system of linear equations in GF(2).
    """
    # Convert the problem to a matrix form over GF(2)
    n = len(A)
    matrix = np.zeros((64, n), dtype=np.uint8)
    
    # Fill the matrix with the bits of each A[i]
    for i in range(n):
        for j in range(64):
            matrix[j, i] = (A[i] >> j) & 1
    
    # Convert b to a column vector of bits
    b_bits = np.zeros(64, dtype=np.uint8)
    for j in range(64):
        b_bits[j] = (b >> j) & 1
    
    # Solve the system using Gaussian elimination in GF(2)
    # Note: This is a simplified version and may not handle all cases
    augmented = np.column_stack((matrix, b_bits))
    
    # Perform Gaussian elimination
    rank = 0
    for j in range(64):
        # Find pivot
        pivot_row = None
        for i in range(rank, n):
            if augmented[j, i] == 1:
                pivot_row = i
                break
        
        if pivot_row is None:
            # No pivot found, check if the equation is consistent
            if augmented[j, -1] == 1:
                # Inconsistent equation: b[j] = 1 but no A[i][j] = 1
                return None  # No solution
            continue
        
        # Swap rows to get pivot at the top
        if pivot_row != rank:
            augmented[:, [rank, pivot_row]] = augmented[:, [pivot_row, rank]]
        
        # Eliminate below
        for i in range(rank + 1, n):
            if augmented[j, i] == 1:
                augmented[:, i] ^= augmented[:, rank]
        
        rank += 1
    
    # Check if the system is consistent
    for j in range(rank, 64):
        if augmented[j, -1] == 1:
            return None  # Inconsistent system
    
    # Back-substitution
    solution = np.zeros(n, dtype=np.uint8)
    for i in range(rank - 1, -1, -1):
        solution[i] = augmented[i, -1]
        for j in range(i + 1, rank):
            if augmented[i, j] == 1:
                solution[i] ^= solution[j]
    
    # Convert solution to an integer
    a = 0
    for i in range(n):
        if solution[i] == 1:
            a |= (1 << i)
    
    return a

def solve_brute_force(A, b, max_bits=48):
    """
    Brute force approach to find 'a' by trying all possible combinations
    of the first few bits of 'a'.
    
    This is useful when the linear system doesn't yield a unique solution.
    """
    # Try all combinations of setting the first max_bits bits
    for bits in range(2**max_bits):
        if bits % 1000000 == 0 and bits > 0:
            print(f"Tried {bits} combinations...")
        
        test_b = 0
        for i in range(len(A)):
            if (bits >> i) & 1:
                test_b ^= A[i]
        
        if test_b == b:
            return bits
    
    return None

def decrypt_flag(a, c):
    """
    Decrypt the flag using the recovered value of 'a'.
    """
    # Split c into ciphertext and IV
    parts = c.split(';')
    if len(parts) != 2:
        return "Invalid ciphertext format"
    
    ciphertext = bytes.fromhex(parts[0])
    iv = bytes.fromhex(parts[1])
    
    # Derive the key from a
    hsh = sha256(str(a).encode())
    key = hsh.digest()
    
    # Decrypt
    cipher = AES.new(key, AES.MODE_CBC, IV=iv)
    try:
        plaintext = unpad(cipher.decrypt(ciphertext), 16)
        return plaintext.decode('utf-8')
    except Exception as e:
        return f"Decryption failed: {str(e)}"

def analyze_system(A, b):
    """
    Analyze the system to determine if c can be uniquely determined.
    """
    # Count the number of independent equations
    n = len(A)
    matrix = np.zeros((64, n), dtype=np.uint8)
    
    for i in range(n):
        for j in range(64):
            matrix[j, i] = (A[i] >> j) & 1
    
    # Compute rank of the system
    rank = np.linalg.matrix_rank(matrix)
    
    # If rank == n, the system has a unique solution
    # If rank < n, the system has 2^(n-rank) solutions
    possible_solutions = 2**(n - rank)
    
    return {
        "rank": int(rank),
        "variables": n,
        "possible_solutions": possible_solutions,
        "uniquely_determined": rank == n
    }

def main():
    # Load the data
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
        
        A = data['A']
        b = data['b']
        c = data['c']
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return
    
    # Analyze the system
    print("Analyzing the system...")
    analysis = analyze_system(A, b)
    print(f"Rank: {analysis['rank']}/{analysis['variables']}")
    print(f"Possible solutions: {analysis['possible_solutions']}")
    print(f"Is uniquely determined: {analysis['uniquely_determined']}")
    
    # Try to solve the system
    print("\nAttempting to solve the linear system...")
    start_time = time.time()
    a = solve_linear_system(A, b)
    end_time = time.time()
    
    if a is not None:
        print(f"Found solution a = {a} in {end_time - start_time:.2f} seconds")
        
        print("\nDecrypting the flag...")
        flag = decrypt_flag(a, c)
        print(f"Flag: {flag}")
    else:
        print("Linear system has no unique solution")
        
        # If the system has a small number of possible solutions, try brute force
        if analysis['possible_solutions'] <= 2**20:
            print(f"\nAttempting brute force (up to {analysis['possible_solutions']} solutions)...")
            max_bits = min(20, 48)  # Limit to 20 bits for reasonable time
            start_time = time.time()
            a = solve_brute_force(A, b, max_bits)
            end_time = time.time()
            
            if a is not None:
                print(f"Found solution a = {a} via brute force in {end_time - start_time:.2f} seconds")
                
                print("\nDecrypting the flag...")
                flag = decrypt_flag(a, c)
                print(f"Flag: {flag}")
            else:
                print(f"Brute force failed to find a solution within {2**max_bits} attempts")
        else:
            print("Too many possible solutions for brute force approach")

if __name__ == "__main__":
    main()