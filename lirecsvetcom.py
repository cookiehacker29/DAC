import socket
from time import *
ippc = "192.168.1.103"
iprpi="127.0.0.1"
UDP_PORT = 5500
sauvebdd=""
f=open("basededonee.csv", "r")
fin="fin"

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((iprpi, UDP_PORT))
sock.setblocking(0)

sauvebdd=f.readlines()
f.close()
while 1:
    f=open("basededonee.csv", "r")
    while 1:                        #envoyer en udp 
        data=f.readline()
        if not data:
            break
        print (data)
        sock.sendto(data, (ippc, 5005))  #ippc
    break 
sock.sendto(bytes("fin"), (ippc, 5005)) # fin émition  ippc
print("fin de lenvoi")
f.close()
f=open("basededonee.csv", "w")


for ligne in sauvebdd:
    f.write(ligne)
f.close()




f=open("basededonee.csv", "w")
#sock.bind(("192.168.1.54", 5500)) #iprpi
while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print ("received message:", data)
    f.write(data.decode("utf-8"))
    f.close()
    break
print("fin")

