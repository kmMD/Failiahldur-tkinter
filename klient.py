import socket
import sys
import os 

s = socket.socket()
host = '172.19.22.74'
port = 10110


s.connect((host, port))
sisu=(s.recv(1024).decode())
jupid=sisu.split('$$')
nimi=jupid[0]
save_path=os.getcwd()+"/Saadetised"
complete_name=os.path.join(save_path,nimi)
uus_fail=open(complete_name,'w')
uus_fail.write(jupid[1])
uus_fail.close()
s.close
