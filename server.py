import socket
import sys

s = socket.socket()
host = socket.gethostname()
port = 10110
s.bind((host, port))
print(host)
nimi='Projekt.txt'
fail=open(nimi)
s.listen(1)
saadetised=[]
while True:
    c, addr = s.accept()
    print("Sain ühenduse")
    pakk=fail.read(1024)
    pakk1=nimi+'$$'+pakk
    c.send(pakk1.encode())
    c.close()

    
