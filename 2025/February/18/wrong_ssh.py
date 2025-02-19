from Crypto.Hash import MD4
from secrets import choice
from string import printable

flag = b'ictf{REDACTED}'
password = (''.join(choice(printable) for _ in range(4))).encode('utf-8')
print(password)
#super-secure-hash :)
def ssh(ct):
    hasher = MD4.new()
    hasher.update(ct)
    hashed = hasher.digest()
    for i in range(20000):
        hasher.update(hashed)
        intermediate = hasher.digest()
        hashed = bytes(i ^ j for i,j in zip(hashed,intermediate))
    return hashed

def password_checker(A):
    for i in range(len(flag)):
        if ssh(A[:i + 1]) != ssh(password[:i + 1]):
            return False
    return True



def main():
    while(True):
        your_flag = str(input('gimme your password:\t')).encode()
        if password_checker(your_flag):
            print('yep!',flag)
            return
        else:
            print('Nope!')


if __name__ == '__main__':
    main()



    

