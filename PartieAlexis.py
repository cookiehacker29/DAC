# -*- coding: utf-8 -*-
from grovepi import *
from time import *
from math import *
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
Casse = 0 #Valeur incrémenter pour test.
Stop = 0 #Valeur incrémenter pour test.
ValeurCool = 0 #Nombre de ligne dans la base de donnée.
TestValeur = 0 #Valeur incrémenter pour test.
ChangeB = "" #Masse de concentré à recopier quand Midi ou Minuit.
Changement = "" #Lignes à recopier après l'édition de Midi ou Minuit.
TestVache = 0 #Valeur incrémenté pour répéter le nombre de fois pour arriver à la bonne ligne.
Autre = 2 #Sert à déclencher soit Minuit sois Midi la première fois.
ultrasonic_ranger = 4
TestSur = 0 #Sert de condition selon le nombre de vache passé depuis le démarrage.
MangeCasse = 0 #Repère de valeur.
while True:
        try:
#Partie réception de l'ID et récupération de la position dans la database.
            NumeroVache = raw_input("ID de la vache : ") #Id reçu.
            Fichier=open("basededonee3.csv","r")
            while True:
                LigneA = Fichier.readline() #LigneA : Ligne du fichier prise une par une.
                if not LigneA:
                    raise GetOutOfLoop
                for Valeur in LigneA.split(";"): #Valeur : Id de la base de donnée similaire.
                    TestValeur = TestValeur + 1
                    if TestValeur == 3:
                        TestValeur=0
                        if Valeur == NumeroVache:
                            for ValeurVrai in LigneA.split(";"): #ValeurVrai : Numéro de ligne correspondant à l'id.
                                TestSur = TestSur +1
                                break
                            Fichier.close()
                            raise GetOutOfLoop
        except GetOutOfLoop:
            pass        
#Fin partie.
#Partie réception de la distance du capteur et marge d'erreur.
        try:
            if TestSur > 1: #Vrai si une deuxième vache est passée.
                TestA = ultrasonicRead(ultrasonic_ranger) #Première valeur prise du capteur.
                TestB = ultrasonicRead(ultrasonic_ranger) #Deuixème valeur prise du capteur.
                TestC = ultrasonicRead(ultrasonic_ranger) #Troisème valeur prise du capteur.
                TestD = ultrasonicRead(ultrasonic_ranger) #Quatrième valeur prise du capteur.
                if TestA > 200: #Longue série de test pour prendre la valeur la plus appropriée.
                    TestA = 0
                if TestB > 200:
                    TestB = 0
                if TestC > 200:
                    TestC = 0
                if TestD > 200:
                    TestD = 0
                if TestA < 180:
                    TestA = 0
                if TestB < 180:
                    TestB = 0
                if TestC < 180:
                    TestC = 0
                if TestD < 180:
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
                if Distance == 0: #Pour éviter que le calcul bug si la distance trouvé est 0.
                    Distance = 200
#Fin partie.
#Calcul de la masse restante.
                Reste = abs(((sqrt((((200-Distance)/6.67*8.33+8.33)**2)-((200-Distance)+6.67)**2)*2)**2*((200-Distance)+6.67)-(10**2*6.67))/3*0.00065)
                if Distance == 200: #Si la distance était égale à 0, on dit qu'il n'y a pas de reste.
                    Reste = 0
#Fin partie.
#Partie édition de la database pour la vache précédente.
                Fichier=open("basededonee3.csv","r")
                for MangeA in range(ValeurAvant): #MangeA : Ligne du fichier prise une par une jusqu'à celle de la vache passé AVANT.
                    MangeA = Fichier.readline()
                for Mange in MangeA.split(';'): #Mange : Ce que la vache à la droit de manger.
                    MangeCasse=MangeCasse+1
                    if MangeCasse == 4:
                        MangeCasse = 0
                        raise GetOutOfLoop1
        except GetOutOfLoop1:
            pass
        try:
            if TestSur > 1:
                Fichier=open("basededonee3.csv","r")
                for LigneAChanger in range(ValeurAvant): #LigneAChanger : Récupère la ligne de la vache d'AVANT.
                    LigneAChanger = Fichier.readline()
                for ResteAvant in LigneAChanger.split(';'): #ResteAvant : Reste actuel.
                    pass
                Mange = int(Mange)
                Reste = Mange - Reste #Soustrait ce que la vache peut manger par le reste calculé pour resortir ce qu'il lui restera à manger.
                StringReste = str(Reste)
                NouvelleLigne=LigneAChanger.replace(ResteAvant,StringReste)+"\n" #NouvelleLigne : Ligne avec le reste modifié de la vache d'AVANT.
                Fichier.close()
                Fichier=open("basededonee3.csv","r")
                ToutesLignes=Fichier.readlines() #ToutesLignes : Toutes les lignes de la base de donnée.
                Fichier.close()
                Fichier=open("basededonee3.csv","w")
                TestVache=0
                for LigneB in ToutesLignes: #LigneB : String utilisé pour réécrire les lignes de la base de donnée une par une.
                    if LigneB!=LigneAChanger:
                        Fichier.write(LigneB)
                    TestVache=TestVache+1
                    if TestVache==ValeurAvant:
                        Fichier.write(NouvelleLigne)
                Fichier.close()
            if TestSur >= 1: #Zone utilisé pour attribuer les valeurs de la vache arrivée en dernière en tant que vache d'AVANT.
                VacheAvant = NumeroVache
                ValeurAvant = int(ValeurVrai)
#Fin partie.
        except IOError:
                pass
        except NameError:
                pass
#Partie recherche de l'heure.
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
                if HeMi == "12:0" and Autre == 0 or HeMi == "12:0" and Autre == 2: #Test pour voir si il est midi.
                        try:
                                Fichier=open("basededonee3.csv","r")
                                while True:
                                        Rien = Fichier.readline() #Rien : Permet de savoir le nombre de ligne dans la base de donnée.
                                        if not Rien:
                                                raise GetOutOfLoopMid
                                        ValeurCool = ValeurCool + 1
                        except GetOutOfLoopMid:
                                Fichier.close()
                                Fichier=open("basededonee3.csv","r")
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
                                Fichier=open("basededonee3.csv","w")
                                Fichier.write(Changement)
                                Fichier.close()
                                Changement = ""
                                ValeurCool = 0
                                Autre = 1 #Valeur de test pour ne pas répéter les lignes si Minuit (Ou Midi sans le cas de Minuit) n'est pas encore passée.
#Fin partie.
#Partie "Minuit" (Se référer à la partier "Midi" pour connaître la signification des valeurs.).
                if HeMi == "0:0" and Autre == 1 or HeMi == "0:0" and Autre == 2:
                        try:
                                Fichier=open("basededonee3.csv","r")
                                while True:
                                        Rien = Fichier.readline()
                                        if not Rien:
                                                raise GetOutOfLoopMin
                                        ValeurCool = ValeurCool + 1
                        except GetOutOfLoopMin:
                                Fichier.close()
                                Fichier=open("basededonee3.csv","r")
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
                                Fichier=open("basededonee3.csv","w")
                                Fichier.write(Changement)
                                Fichier.close()
                                Changement = ""
                                ValeurCool = 0
                                Autre = 0
        except IOError:
                pass
#Fin partie.
