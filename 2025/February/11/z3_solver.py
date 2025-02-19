import z3
from z3 import Solver, Bool, And, Xor, is_true, BoolVal

def create_matrix_vars(name, rows, cols):
    """Create a matrix of Z3 boolean variables"""
    return [[Bool(f'{name}_{i}_{j}') for j in range(cols)] for i in range(rows)]

def create_vector_vars(name, size):
    """Create a vector of Z3 boolean variables"""
    return [Bool(f'{name}_{i}') for i in range(size)]

def matrix_vector_multiply(matrix, vector):
    """Multiply matrix by vector in F2 (using XOR and AND)"""
    n = len(vector)
    result = []
    for i in range(n):
        row_result = False
        for j in range(n):
            term = And(matrix[i][j], vector[j])
            row_result = Xor(row_result, term)
        result.append(row_result)
    return result

def matrix_multiply(A, B):
    """Multiply two matrices in F2"""
    n = len(A)
    result = [[False for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                term = And(A[i][k], B[k][j])
                result[i][j] = Xor(result[i][j], term)
    return result

# Initialize solver
solver = Solver()

# Create variables for the matrix and initial vector
M = create_matrix_vars('M', 64, 64)
v = create_vector_vars('v', 64)

# Define the characteristic polynomial terms
# x^64 + x^63 + x^62 + x^61 + x^59 + x^56 + x^55 + x^54 + x^53 + x^50 + x^49 + x^47 + 
# x^40 + x^38 + x^37 + x^32 + x^27 + x^25 + x^24 + x^20 + x^19 + x^16 + x^15 + x^14 + 
# x^12 + x^9 + x^8 + x^7 + x + 1
charpoly_powers = [64, 63, 62, 61, 59, 56, 55, 54, 53, 50, 49, 47, 40, 38, 37, 32, 
                  27, 25, 24, 20, 19, 16, 15, 14, 12, 9, 8, 7, 1, 0]

def matrix_copy(A):
    """Deep copy a matrix"""
    return [[A[i][j] for j in range(len(A))] for i in range(len(A))]

def matrix_sum(A, B):
    """Add two matrices in F2 (using XOR)"""
    n = len(A)
    result = [[False for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = Xor(A[i][j], B[i][j])
    return result

# Add all constraints as we go
def add_constraints():
    current_sum = matrix_copy(M)
    current_mat = matrix_copy(M)
    for i in range(2,1024):
        current_mat = matrix_multiply(current_mat,M)
        #current_mat = M^i
        if i in primes:
            current_vec = matrix_vector_multiply(current_mat,v)
            ind = primes.index(i)
            expected_value = z3.BoolVal(prime_cuts[ind] == 1)
            solver.add(current_vec[-1] == expected_value)
        
        if i in charpoly_powers:
            current_sum = matrix_sum(current_sum,current_mat)
        
        print(f"matrix multiplication reached power {i}")

    print("Adding characteristic polynomial constraints...")
    #current_sum = charpoly(M) + I
    for i in range(64):
        for j in range(64):
            sum_component = current_sum[i][j]
            if i == j:
                solver.add(sum_component == True)
            else:
                solver.add(sum_component == False)  # Sum should be 0 in F2
            n = i*64 + j
            if n % 100 == 0:
                print(f"{n}/{64*64}")


# Add characteristic polynomial constraints
# In F2, M must satisfy: M^64 + M^63 + ... + M + I = 0
def add_charpoly_constraints():
    # We'll build up powers of M and combine them
    current = M
    power_matrices = {1: M}
    
    # Precompute needed powers
    max_power = max(charpoly_powers)
    for i in range(2, max_power + 1):
        if i in charpoly_powers:
            current = matrix_multiply(current, M)
            power_matrices[i] = current
    
    # Add constraints that sum of matrices = I (identity)
    for i in range(64):
        for j in range(64):
            sum_term = False
            for power in charpoly_powers:
                if power == 0:
                    # Add identity matrix term
                    sum_term = Xor(sum_term, i == j)
                else:
                    sum_term = Xor(sum_term, power_matrices[power][i][j])
            solver.add(sum_term == False)  # Sum should be 0 in F2

# Define the prime numbers and their corresponding outputs
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997, 1009, 1013, 1019, 1021]

prime_cuts = [0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0]

# Add prime cuts constraints
def add_prime_cuts_constraints():
    current = v
    for i in range(1,1024):
        current = matrix_vector_multiply(M, current)
        # current = M^i*v
        try:
            ind = primes.index(i)
        except ValueError:
            continue
        # Convert integer to boolean and add constraint
        expected_value = z3.BoolVal(prime_cuts[ind] == 1)
        solver.add(current[-1] == expected_value)

# Add all constraints
print("Adding prime cuts constraints...")
add_constraints()

print("Solving...")
if solver.check() == z3.sat:
    model = solver.model()
    # Extract solution
    solution_matrix = [[is_true(model[M[i][j]]) for j in range(64)] for i in range(64)]
    solution_vector = [is_true(model[v[i]]) for i in range(64)]
    print("Solution found!")

    print(solution_matrix)
    print(solution_vector)
else:
    print("No solution found")