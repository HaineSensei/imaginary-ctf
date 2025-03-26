import secrets
from Crypto.Util.number import bytes_to_long


flag = b'ictf{REDACTED}'



def get_random_float():
    return 64 + secrets.randbits(64) / (2**57)


bits = bin(bytes_to_long(flag))[2:]
print(bits)
a = 268435456.0
output = []
for i in bits:
    r = get_random_float()
    if (i == '1'):
        output.append(r + a - a)
    else:
        output.append(r)
print(f"output = {output}")
    
    
    