import socket
import time
from grovepi import *
import RPi.GPIO as GPIO
##############################################################################Definition des paramètre de communication#######################################################################################
UDP_IP = "192.168.1.54" # mettre l'adresse de la Rpi (peut etre 127.0.0.1)
UDP_IP_DEST = "192.168.1.104" #ip du pc
UDP_PORT = 5500 #port sur lequel on communique (il sert a l'envoi et a la reception)
coucou=0   #Pour savoir en quelle mode on est (0=attente de message; 1=envoi de la BDD; 2= Recevoir la BDD)
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT)) # on écoute 
sock.setblocking(0) #on attend pas indéfiniment si on ne recoit pas
##############################################################################Definition des paramètre de communication#######################################################################################
##############################################################################Paramètre du moteur#############################################################################################################
GPIO.setmode(GPIO.BOARD)#On utilise la numérotation en
GPIO.setup(37,GPIO.OUT)#on définit le port 37 (port board) comme port pour le moteur et on dit que c'est une sortie
entier=84
##############################################################################Paramètre du moteur#############################################################################################################
##############################################################################Lecture du fichier csv##########################################################################################################
numcolone=1 #on part de la colone 1 
idcsv="rien" #id en train d'être lue sur le csv
quantiterestant=0#quantiée a donner a la vache
##############################################################################Lecture du fichier csv##########################################################################################################
##############################################################################La boucle infinie(et c'est long)################################################################################################
while True:
    try:
        idvache=input("Identifiant de la vache : ")# avant cette partie il faut lire si une vache est présente et récupérer son UID dans idvache
        f=open("basededonee.csv", "r") 
        while idcsv<>str(idvache):
            ligne=f.readline()
            if not ligne:
                break
            ligne.split
            for col in ligne.split(";"):
                if numcolone==3:
                    idcsv=col
                numcolone=numcolone+1
            numcolone=1
        for col in ligne.split(";"):
            if numcolone==5:
                quantiterestant=col
            numcolone=numcolone+1
        numcolone=1
        print(type(quantiterestant))
        if type(quantiterestant)!=type(entier):
            quantiterestant=quantiterestant[:-1]#enlever le saut de ligne pour garder que le chifre
        f.close()
        print(quantiterestant)
        GPIO.output(37,GPIO.HIGH)
        print((float(quantiterestant)*2)*1.4)
        time.sleep((float(quantiterestant)*2)*1.4)
        GPIO.output(37,GPIO.LOW)# Send LOW to switch off moteur
        print ("Etein")
    except IOError:
        digitalWrite(moteur,0)
        pass

    try:
        if coucou==0:
            data, addr=sock.recvfrom(1024) # buffer size is 1024 octet
            print ("received message:", data)
            coucou=int(data)
            print("mode : ",coucou)
        elif coucou==2:
            data, addr=sock.recvfrom(1024)
            print(data)
            f=open("basededonee.csv", "w")
            f.write(data)
            f.close()
            coucou=0
    except IOError:
        print("Erreur dans la partie de reception de bdd")
        pass

    try:# on envoitt la bdd a ce pc qui crache
        if coucou==1:
            time.sleep(.5)#delay de une seconde pour pas flood
            f=open("basededonee.csv","r")
            DATA=f.readlines()
            for ligne in DATA:
                sock.sendto(ligne,(UDP_IP_DEST, UDP_PORT))
                print("Envoi :",ligne)
            sock.sendto("fin",(UDP_IP_DEST, UDP_PORT))
            print("fin")
            time.sleep(.5)
            coucou=0
    except IOError:
        print ("Error")
        pass
