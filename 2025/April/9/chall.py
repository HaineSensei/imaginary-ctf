from Crypto.Util.number import getPrime, bytes_to_long
from secrets import randbits


flag = b'ictf{REDACTED}'

p,q = getPrime(1024),getPrime(1024)
assert((p-1) % e != 0)
assert((q-1) % e != 0)
e = 0x10001

M1,M2 = randbits(1024) | randbits(1024) ,randbits(1024) | randbits(1024)

P,Q = p & M1, q & M2


n = p*q
c = pow(bytes_to_long(flag),e,n)



print(f"c = {c}")
print(f"n = {n}")
print(f"M1 = {M1}")
print(f"M2 = {M2}")
print(f"P = {P}")
print(f"Q = {Q}")






