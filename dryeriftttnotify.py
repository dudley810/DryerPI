import requests as req
import RPi.GPIO as GPIO
import sys
from time import sleep
import datetime
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4,GPIO.IN)
GPIO.setup(25,GPIO.OUT)
NotificationSeconds = 300

def CallIfTTT(url,whoto):
    response = req.get(url)
    if (response.status_code == 200):
        print("Message has been sent to " + whoto)
        return True
    else:
        return False
   
lastnotify = None
while True:
    dryerdone = False    
    if (GPIO.input(4)):
        dryerdone = False    
    else:
        dryerdone = True
        
    GPIO.output(25,dryerdone)

    cannotify = False
    if (lastnotify == None):
        cannotify = True
    else:
        diffvalue = datetime.datetime.now() - lastnotify
        if (diffvalue.seconds > NotificationSeconds):
            cannotify = True
        else:
            cannotify = False

    if (dryerdone == True and cannotify):
        print ("sending ifttt messages")
        peggy = CallIfTTT("YOUR MAKER IFTTT.COM URL","peggy")
        ken = CallIfTTT("YOUR MAKER IFTTT.COM URL","ken")
        if (peggy and ken):
            lastnotify = datetime.datetime.now()
            print("sent ifttt message at " + lastnotify.strftime("%m/%d/%Y, %H:%M:%S"))

    else:
        if (dryerdone):
            if (lastnotify == None):
                print("The Dryer is done but we are trying to reach you.")
            else:
                print("The Dryer is done but already notified you at: " + lastnotify.strftime("%m/%d/%Y, %H:%M:%S"))
        else:
            if (lastnotify == None):
                print("Waiting for the dryer to be done never notified before.")
            else:
                print("Waiting for the dryer to be done: " + lastnotify.strftime("%m/%d/%Y, %H:%M:%S"))
    
    sleep(2)