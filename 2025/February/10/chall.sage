from Crypto.Util.number import getPrime, bytes_to_long
from secret import flag

p = getPrime(512)
q = getPrime(512)
n = p*q

m = bytes_to_long(flag.encode())
e = 65537
c = pow(m,e,n)

P.<x,y> = PolynomialRing(ZZ)
x, y = P.gens()

terms = []
for i in range(16):
    terms += [(x**i)*(y**j) for j in range(16-i)]

T = RealDistribution('gaussian', 2)
coefs = [round(T.get_random_element()) for _ in range(len(terms))]

f = sum([term*coef for term,coef in zip(terms,coefs)])
w = pow(2,f(p,q),n)

with open('out.txt', 'w') as file:
    file.write(f'{n = }\n')
    file.write(f'{e = }\n')
    file.write(f'{c = }\n')
    file.write(f'{f = }\n')
    file.write(f'{w = }\n')
