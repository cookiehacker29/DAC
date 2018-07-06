from grovepi import *
import pdb
from math import *
ultrasonic_ranger = 4
#pdb.set_trace()
while True:
    try:
                TestA = ultrasonicRead(ultrasonic_ranger) * 0.77#Première valeur prise du capteur.
                print TestA
    except TypeError:
        pass
