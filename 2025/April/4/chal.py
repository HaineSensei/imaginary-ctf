from Crypto.Util.number import long_to_bytes
from secret import base, message

encoded = 0
for i in message:
    encoded *= base
    encoded += i
encoded = long_to_bytes(encoded)
print(encoded)
