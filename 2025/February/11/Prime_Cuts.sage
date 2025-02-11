from Crypto.Hash import SHA256
from Crypto.Cipher import AES

flag = b'ictf{REDACTED}'

def bits_to_bytes(bits):
    byte_array = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for bit in bits[i:i+8]:
            byte = (byte << 1) | int(bit)
        byte_array.append(byte)
    return byte_array



F = GF(2)

M = random_matrix(F,64,64)
   
initial_value = random_vector(F,64)
sequence = [(M^i * initial_value)[-1] for i in range(1024)]



key = bits_to_bytes(sequence)

hashed = SHA256.new(key).digest()
cipher = AES.new(hashed,AES.MODE_ECB)
encrypted = cipher.encrypt(flag)

print(f'encrypted = {encrypted}')

poly = M.charpoly()
prime_cuts = []
for i in range(1024):
    if (is_prime(i)):
        prime_cuts.append(sequence[i])


print(f'prime_cuts = {prime_cuts}')
print(f'poly = {poly}')