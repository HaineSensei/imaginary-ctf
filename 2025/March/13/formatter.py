import json

def to_binary_array(n, bits=64):
    return [(n >> i) & 1 for i in range(bits)]

try:
    with open('data.json', 'r') as f:
        data = json.load(f)
    
    A = data['A']
    b = data['b']
except Exception as e:
    print(f"Error loading data: {str(e)}")

# Create the binary matrix and vector
A_bin = []
for i in range(64):  # For each bit position
    row = []
    for a in A:
        row.append((a >> i) & 1)
    A_bin.append(row)

b_bin = to_binary_array(b)

# Format the matrix for the calculator
def format_matrix(matrix):
    result = "{"
    for i, row in enumerate(matrix):
        result += ",".join(str(x) for x in row)
        if i < len(matrix) - 1:
            result += ";"
    result += "}"
    return result

def format_vector(vector):
    result = "{"
    result += ",".join(str(x) for x in vector)
    result += "}"
    return result

# Generate the matrix and vector in the requested format
A_formatted = format_matrix(A_bin)
b_formatted = format_vector(b_bin)

# Print the command for the matrix calculator
print(f"multinverse({A_formatted})*{b_formatted}")

# Also save to files in case the output is too long for the console
with open('A_matrix.txt', 'w') as f:
    f.write(A_formatted)

with open('b_vector.txt', 'w') as f:
    f.write(b_formatted)

with open('command.txt', 'w') as f:
    f.write(f"multinverse({A_formatted})*{b_formatted}")

print("Matrix and vector have been formatted and saved to files.")