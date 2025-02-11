from Crypto.Util.number import getPrime, bytes_to_long
from secret import flag

p = getPrime(512)
q = getPrime(512)
n = p*q

m = bytes_to_long(flag.encode())
e = 65537
c = pow(m,e,n)

P.<x> = PolynomialRing(ZZ)
x = P.gens()[0]

terms = [x**i for i in range(137)]

T = RealDistribution('gaussian', 2)
coefs = [round(T.get_random_element()) for _ in range(len(terms))]

f = sum([term*coef for term,coef in zip(terms,coefs)])
w = pow(2,f(p),n)

with open('out.txt', 'w') as file:
    file.write(f'{n = }\n')
    file.write(f'{e = }\n')
    file.write(f'{c = }\n')
    file.write(f'{f = }\n')
    file.write(f'{w = }\n')
