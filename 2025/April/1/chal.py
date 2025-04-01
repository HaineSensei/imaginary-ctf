from Crypto.Util.number import bytes_to_long, getPrime
flag = b'ictf{This_is_not_the_flag}'

e = 0x10001
p,q = getPrime(1024),getPrime(1024)
n = p * q
c = pow(bytes_to_long(flag),e,n)

print("n = ",n)
print("c =",c)
print("P =",p & (1 << 341) - 1)
print("Q =",q & (1 << 341) - 1)
