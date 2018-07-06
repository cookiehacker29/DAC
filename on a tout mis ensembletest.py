#!/usr/bin/env python
# -*- coding: utf8 -*-
from grovepi import *
from time import *
from math import *
import RPi.GPIO as GPIO
import MFRC522
import socket
class GetOutOfLoop(Exception): #Truc utile pour sortir des boucles dans des boucles dans des boucles...
        pass
class GetOutOfLoop1(Exception):
        pass
class GetOutOfLoop2(Exception):
        pass
class GetOutOfLoopMid(Exception):
        pass
class GetOutOfLoopMin(Exception):
        pass
#########################################Valeur a Allez scie ! ce couillon 
Casse = 0 #Valeur incrémenter pour test.
Stop = 0 #Valeur incrémenter pour test.
ValeurCool = 0 #Nombre de ligne dans la base de donnée.
TestValeur = 0 #Valeur incrémenter pour test.
ChangeB = "" #Masse de concentré à recopier quand Midi ou Minuit.
Changement = "" #Lignes à recopier après l'édition de Midi ou Minuit.
TestVache = 0 #Valeur incrémenté pour répéter le nombre de fois pour arriver à la bonne ligne.
NumeroVache = "" #Ne m'enerve pas.
Autre = 2 #Sert à déclencher soit Minuit sois Midi la première fois.
ultrasonic_ranger = 4
TestSur = 0 #Sert de condition selon le nombre de vache passé depuis le démarrage.
MangeCasse = 0 #Repère de valeur.
Poke = 0 #Valeur de test.
#########################################Valeur a Allez scie ! ce couillon
#########################################Valeur a Air 1 ce couillon 
MIFAREReader = MFRC522.MFRC522()
idrfid=""
AntiAFK = 0
Campouse = 0
#########################################Valeur a Air 1 ce couillon
#########################################Valeur a T'es haut d'or ce dieu
UDP_IP = "192.168.1.54" # mettre l'adresse de la Rpi (peut etre 127.0.0.1)
UDP_IP_DEST = "192.168.1.101" #ip du pc
UDP_PORT = 5500 #port sur lequel on communique (il sert a l'envoi et a la reception)
mode=0   #Pour savoir en quelle mode on est (0=attente de message; 1=envoi de la BDD; 2= Recevoir la BDD)
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT)) # on écoute 
sock.setblocking(0) #on attend pas indéfiniment si on ne recoit pas
GPIO.setmode(GPIO.BOARD)#On utilise la numérotation en
GPIO.setup(37,GPIO.OUT)#on définit le port 37 (port board) comme port pour le moteur et on dit que c'est une sortie
entier=84
numcolone=1 #on part de la colone 1 
idcsv="rien" #id en train d'être lue sur le csv
quantiterestant=0#quantiée a donner a la vache
trigger = 0
#########################################Valeur a T'es haut d'or ce dieu 
# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while True:
    try:
        # Scan for cards
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        # Get the UID of the card       
        (status,uid) = MIFAREReader.MFRC522_Anticoll()
        # If we have the UID, continue
        if status == MIFAREReader.MI_OK: 
            # Print UID
            a,b,c,d,e = str(uid).split(", ")
            sauvegarde = str(a)+str(b)+str(c)+str(d)+str(e)
            sauvegarde = sauvegarde[:-1]
            for idrfid in sauvegarde.split('['):
                NumeroVache = idrfid #Id reçu.
            print idrfid
            Campouse = 0
    except IOError:
        pass
    try:
#Partie réception de l'ID et récupération de la position dans la database.
            Fichier=open("basededonee.csv","r")
            while True:
                LigneA = Fichier.readline() #LigneA : Ligne du fichier prise une par une.
                TestValeur=0
                if not LigneA:
                    raise GetOutOfLoop
                for Valeur in LigneA.split(";"): #Valeur : Id de la base de donnée similaire.
                    TestValeur = TestValeur + 1
                    if TestValeur == 3:
                        if Valeur == NumeroVache:
                            for ValeurVrai in LigneA.split(";"): #ValeurVrai : Numéro de ligne correspondant à l'id.
                                TestSur = TestSur +1
                                if AntiAFK == 0:
                                        Poke = 1
                                        trigger = 1
                                NumeroVache = ""
                                print ValeurVrai
                                break
                            Fichier.close()
                            raise GetOutOfLoop
    except GetOutOfLoop:
        pass        
#Fin partie.
#Partie réception de la distance du capteur et marge d'erreur.
        try:
            if TestSur > 1 and Poke == 1 and AntiAFK == 0: #Vrai si une deuxième vache est passée.
                TestA = ultrasonicRead(ultrasonic_ranger) #Première valeur prise du capteur.
                TestB = ultrasonicRead(ultrasonic_ranger) #Deuixème valeur prise du capteur.
                TestC = ultrasonicRead(ultrasonic_ranger) #Troisème valeur prise du capteur.
                TestD = ultrasonicRead(ultrasonic_ranger) #Quatrième valeur prise du capteur.
                if TestA > 74: #Longue série de test pour prendre la valeur la plus appropriée.
                    TestA = 0
                if TestB > 74:
                    TestB = 0
                if TestC > 74:
                    TestC = 0
                if TestD > 74:
                    TestD = 0
                if TestA < 54:
                    TestA = 0
                if TestB < 54:
                    TestB = 0
                if TestC < 54:
                    TestC = 0
                if TestD < 54:
                    TestD = 0
                if TestA >= TestB:
                    if TestA >= TestC:
                        if TestA >= TestD:
                            Distance = TestA
                if TestB >= TestA:
                    if TestB >= TestC:
                        if TestB >= TestD:
                            Distance = TestB
                if TestC >= TestA:
                    if TestC >= TestB:
                        if TestC >= TestD:
                            Distance = TestC
                if TestD >= TestA:
                    if TestD >= TestB:
                        if TestD >= TestC:
                            Distance = TestD
                print Distance
                if Distance == 0: #Pour éviter que le calcul bug si la distance trouvé est 0.
                    Distance = 74
#Fin partie.
#Calcul de la masse restante.
                Reste = abs(((sqrt((((74-Distance)/6.67*8.33+8.33)**2)-((74-Distance)+6.67)**2)*2)**2*((74-Distance)+6.67)-(10**2*6.67))/3*0.00065)
                if Distance == 74: #Si la distance était égale à 0, on dit qu'il n'y a pas de reste.
                    Reste = 0
#Fin partie.
#Partie édition de la database pour la vache précédente.
                Fichier=open("basededonee.csv","r")
                for MangeA in range(ValeurAvant): #MangeA : Ligne du fichier prise une par une jusqu'à celle de la vache passé AVANT.
                    MangeA = Fichier.readline()
                for Mange in MangeA.split(';'): #Mange : Ce que la vache à la droit de manger.
                    MangeCasse=MangeCasse+1
                    if MangeCasse == 4:
                        MangeCasse = 0
                        raise GetOutOfLoop1
        except GetOutOfLoop1:
            pass
        except IOError:
                pass
        except NameError:
                pass
        except TypeError:
                pass
        try:
            if TestSur > 1 and Poke == 1 and AntiAFK == 0:
                Fichier=open("basededonee.csv","r")
                for LigneAChanger in range(ValeurAvant): #LigneAChanger : Récupère la ligne de la vache d'AVANT.
                    LigneAChanger = Fichier.readline()
                for ResteAvant in LigneAChanger.split(';'): #ResteAvant : Reste actuel.
                    pass
                Mange = int(Mange)
                ResteA = Reste
                Reste = Mange - Reste #Soustrait ce que la vache peut manger par le reste calculé pour resortir ce qu'il lui restera à manger.
                if ResteA == 0:
                        Reste = 0
                StringReste = str(Reste)
                NouvelleLigne=LigneAChanger.replace(ResteAvant,StringReste)+"\n" #NouvelleLigne : Ligne avec le reste modifié de la vache d'AVANT.
                Fichier.close()
                Fichier=open("basededonee.csv","r")
                ToutesLignes=Fichier.readlines() #ToutesLignes : Toutes les lignes de la base de donnée.
                Fichier.close()
                Fichier=open("basededonee.csv","w")
                TestVache=0
                for LigneB in ToutesLignes: #LigneB : String utilisé pour réécrire les lignes de la base de donnée une par une.
                    if LigneB!=LigneAChanger:
                        Fichier.write(LigneB)
                    TestVache=TestVache+1
                    if TestVache==ValeurAvant:
                        Fichier.write(NouvelleLigne)
                Fichier.close()
                Poke = 0
            if TestSur >= 1: #Zone utilisé pour attribuer les valeurs de la vache arrivée en dernière en tant que vache d'AVANT.
                VacheAvant = NumeroVache
                ValeurAvant = int(ValeurVrai)
#Fin partie.
        except IOError:
                pass
        except NameError:
                pass
    try:
            if trigger == 1 and AntiAFK == 0:
                idvache=idrfid
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
                sleep((float(quantiterestant)*2)*1.4)
                GPIO.output(37,GPIO.LOW)# Send LOW to switch off moteur
                trigger = 0
                idcsv="rien"
                print ("Eteint")
                AntiAFK = 1
    except IOError:
        GPIO.output(37,GPIO.LOW)
        pass
    except NameError:
        GPIO.output(37,GPIO.LOW) 
        pass
    except TypeError:
        GPIO.output(37,GPIO.LOW) 
        pass
    try:
        if mode==0:
            data, addr=sock.recvfrom(1024) # buffer size is 1024 octet
            print ("received message:", data)
            mode=int(data)
            print("mode : ",mode)
        elif mode==2:
            data, addr=sock.recvfrom(1024)
            print(data)
            f=open("basededonee.csv", "w")
            f.write(data)
            f.close()
            mode=0
    except IOError:
        pass
    try:# on envoitt la bdd a ce pc qui crache
        if mode==1:
            sleep(.5)#delay de une seconde pour pas flood
            f=open("basededonee.csv","r")
            DATA=f.readlines()
            for ligne in DATA:
                sock.sendto(ligne,(UDP_IP_DEST, UDP_PORT))
                print("Envoi :",ligne)
            sock.sendto("fin",(UDP_IP_DEST, UDP_PORT))
            print("fin")
            sleep(.5)
            mode=0
            f.close()
    except IOError:
        print ("Error")
        pass
    try:
                Temps = localtime() #Temps : Année, mois , jour, heure, minutes, secondes.
                Temps = str(Temps)
                for TestTemps in Temps.split(","): #TestTemps : Valeur prise une par une de Temps.
                        pass
                        Casse = Casse + 1
                        if Casse == 4:
                                HeureA=TestTemps #HeureA : Heure non traitée.
                                for Heure in HeureA.split('='): #Heure : Heure.
                                        pass
                        if Casse == 5:
                                MinuteA=TestTemps #MinuteA : Minute non traitée.
                                Casse = 0
                                for Minute in MinuteA.split('='): #Minute : Minute.
                                        pass
                                raise GetOutOfLoop2   
    except GetOutOfLoop2:
                HeMi=Heure + ":" + Minute #Hemi : Heure + Minute assemblée.
#Fin Partie.
#Partie "Midi".
                print HeMi
                if HeMi == "12:0" and Autre == 0 or Autre == 2: #Test pour voir si il est midi.
                        try:
                                Fichier=open("basededonee.csv","r")
                                while True:
                                        Rien = Fichier.readline() #Rien : Permet de savoir le nombre de ligne dans la base de donnée.
                                        if not Rien:
                                                raise GetOutOfLoopMid
                                        ValeurCool = ValeurCool + 1
                        except GetOutOfLoopMid:
                                Fichier.close()
                                Fichier=open("basededonee.csv","r")
                                for Change in range(ValeurCool): #Change : Chaque ligne à changer une par une.
                                        Change = Fichier.readline()
                                        for ChangeA in Change.split(';'): #ChangeA : Reste à changer.
                                                Stop = Stop + 1
                                                if Stop == 4:
                                                        ChangeB = str(ChangeA) #ChangeB : Masse de concentré à recopier.
                                                if Stop == 5:
                                                        Stop=0
                                                        NouvelleLigneA=Change.replace(ChangeA,ChangeB)
                                                        Changement = Changement + NouvelleLigneA + "\n" #Changement : toutes les lignes à recopier.
                                Fichier.close()
                                Fichier=open("basededonee.csv","w")
                                Fichier.write(Changement)
                                print "Fini"
                                Fichier.close()
                                Changement = ""
                                ValeurCool = 0
                                Autre = 1 #Valeur de test pour ne pas répéter les lignes si Minuit (Ou Midi sans le cas de Minuit) n'est pas encore passée.
                                HeMi = ""
#Fin partie.
#Partie "Minuit" (Se référer à la partier "Midi" pour connaître la signification des valeurs.).
                if HeMi == "0:0" and Autre == 1 or Autre == 2:
                        try:
                                Fichier=open("basededonee.csv","r")
                                while True:
                                        Rien = Fichier.readline()
                                        if not Rien:
                                                raise GetOutOfLoopMin
                                        ValeurCool = ValeurCool + 1
                        except GetOutOfLoopMin:
                                Fichier.close()
                                Fichier=open("basededonee.csv","r")
                                for Change in range(ValeurCool):
                                        Change = Fichier.readline()
                                        for ChangeA in Change.split(';'):
                                                Stop = Stop + 1
                                                if Stop == 4:
                                                        ChangeB = str(ChangeA)
                                                if Stop == 5:
                                                        Stop=0
                                                        NouvelleLigneA=Change.replace(ChangeA,ChangeB)
                                                        Changement = Changement + NouvelleLigneA + "\n"
                                Fichier.close()
                                Fichier=open("basededonee.csv","w")
                                Fichier.write(Changement)
                                print "Fini"
                                Fichier.close()
                                Changement = ""
                                ValeurCool = 0
                                Autre = 0
                                HeMi = ""

#Fin partie.
    try:
            if AntiAFK == 1:
                    Campouse = Campouse + 1
                    print Campouse
                    if Campouse == 20:
                            Campouse = 0
                            AntiAFK = 0
    except IOError:
            pass
