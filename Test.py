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
Autre = 2
Casse = 0
Stop = 0
ValeurCool = 0
Changement = ""
while True:
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
                if HeMi == "12:0" and Autre == 0 or HeMi == "12:0" and Autre == 2: #Test pour voir si il est midi.
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
                                sleep(2)
                                Fichier.close()
                                Changement = ""
                                ValeurCool = 0
                                Autre = 1 #Valeur de test pour ne pas répéter les lignes si Minuit (Ou Midi sans le cas de Minuit) n'est pas encore passée.
                                HeMi = ""
#Fin partie.
#Partie "Minuit" (Se référer à la partier "Midi" pour connaître la signification des valeurs.).
                if HeMi == "0:0" and Autre == 1 or HeMi == "0:0" and Autre == 2:
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
                                sleep(2)
                                Fichier.close()
                                Changement = ""
                                ValeurCool = 0
                                Autre = 0
                                HeMi = ""
