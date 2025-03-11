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
NotifyCount = 0

def DryerDone():
    global NotifyCount
    response = req.post('http://10.18.18.235/sendmsg?message=dryer is done')
    if (response.status_code == 200):
        NotifyCount += 1
        print("Message has been sent")
        return True
    else:
        return False

lastnotify = None
while True:
    dryerdone = False
    if (GPIO.input(4)):
        dryerdone = False
        NotifyCount = 0
    else:
        dryerdone = True

    GPIO.output(25,dryerdone)

    cannotify = False
    if (lastnotify == None):
        cannotify = True
    else:
        diffvalue = datetime.datetime.now() - lastnotify
        if (diffvalue.seconds > NotificationSeconds and NotifyCount < 5):
            cannotify = True
        else:
            cannotify = False

    if (dryerdone == True and cannotify):
        print ("sending messages")
        resp = DryerDone()
        if (resp):
            lastnotify = datetime.datetime.now()
            print("sent message at " + lastnotify.strftime("%m/%d/%Y, %H:%M:%S"))

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
