import socket
import time

UDP_IP = "192.168.1.54" # mettre l'adresse de la Rpi
UDP_IP_DEST = "192.168.1.101"
UDP_PORT = 5500
coucou=0
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
sock.setblocking(0)

while True:
        try:
                if coucou==1:
                        time.sleep(3)
                        f=open("basededonee.csv", "r")
                        DATA=f.readlines()
                        for ligne in DATA:
                                sock.sendto(ligne,(UDP_IP_DEST, UDP_PORT))
                                print(ligne)
                        sock.sendto("fin", (UDP_IP_DEST, UDP_PORT))
                        time.sleep(.5)
                        coucou=0
        except IOError:
                print ("Error")
        try :
                if coucou==0:
                        #recevoir le message
                        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
                        print ("received message:", data)
                        coucou=int(data)
                        print(type(int(coucou)))
                        print(coucou)
                elif coucou==2:
                        data, addr = sock.recvfrom(1024)
                        print(data)
                        f=open("basededonee.csv", "w")
                        f.write(data)
                        f.close()
        except IOError :
                #on ne fait rien
                pass
