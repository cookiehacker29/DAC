#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522


# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

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
                pass
            print idrfid
    except IOError:
        print("arrive aps a lire rfid")
        pass
