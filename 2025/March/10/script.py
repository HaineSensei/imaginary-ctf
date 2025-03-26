import socket
from time import sleep

val = True
while val:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("155.248.210.243", 42179))
    
    print(f"first: {s.recv(1024).decode()} {s.recv(1024).decode()}")
    s.send("n-n\n".encode())
    x = s.recv(1024).decode() + s.recv(1024).decode()
    print(f"second: {x}")
    if "ictf" in x:
        print(x)
        break
