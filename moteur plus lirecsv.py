import time
from grovepi import *
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(37,GPIO.OUT)

# Connect the Grove LED to digital port D5
#moteur = 4
#pinMode(moteur,"OUTPUT")
time.sleep(1)
numcolone=1 #on part de la colone 1 
idcsv="rien"
quantiterestant=0#quantiée a donner a la vache
while True:
    try:
        idvache=input("Identifiant de la vache : ") # quand une ache arrive
        f=open("basededonee.csv", "r")
        while idcsv<>str(idvache):#      On verifi iu est la vache dans9 la BDD
            ligne=f.readline()
            if not ligne:
                break
            ligne.split
            for col in ligne.split(";"):
                if numcolone==3:
                    idcsv=col
                numcolone=numcolone+1
            #print(idcsv)
            numcolone=1#   On verifi iu est la vache dans la BDD
        for col in ligne.split(";"): #combien on donne a manger
            if numcolone==5:
                quantiterestant=col
                print(quantiterestant)
            numcolone=numcolone+1
        numcolone=1
        quantiterestant=quantiterestant[:-1]
        print(quantiterestant)#activer le moteur avec la valeur 1tour moteur = 500g 1tour = 1.4s

        GPIO.output(37,GPIO.HIGH)   # Send HIGH to switch on moteur
        print ("Allumer")
        print((float(quantiterestant)*2)*1.4)
        time.sleep((float(quantiterestant)*2)*1.4)
        
        GPIO.output(37,GPIO.LOW)# Send LOW to switch off moteur
        print ("Etein")














        

    except KeyboardInterrupt:	# Turn LED off before stopping
        digitalWrite(moteur,0)
        break
    except IOError:				# Print "Error" if communication error encountered
        print ("Error")
        digitalWrite(moteur,0)
