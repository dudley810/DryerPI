import RPi.GPIO as GPIO
import requests as req
from time import sleep
import datetime
from sys import exit
import os

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4,GPIO.IN)
global NotifyCount
global lastemail
global lastprint
NotificationSeconds = 600
NotifyCount = 0
lastemail = datetime.datetime.now()
lastprint = datetime.datetime.now()
r = req.post("http://192.168.1.200:8080/api/startpi")

def CheckPrint(Message):
   global NotifyCount
   global lastprint
   global lastemail
   current = datetime.datetime.now()
   diffvalue = current - lastprint
   if (diffvalue.seconds > 1):
        lastprint = datetime.datetime.now() 
        print("%s-GPIO=%s, Lastemail=%s, Current=%s, Notified=%s  " % (Message,GPIO.input(4), lastemail,current,NotifyCount))
   return

# Dryer Done
def DryerDone():
   global NotifyCount
   global lastemail
   payload = {'gpioresult': 0}
   r = req.post("http://192.168.1.200:8080/api/dryerpi", params=payload)
   if (r.status_code == req.codes.ok):
       NotifyCount += 1
       lastemail = datetime.datetime.now()
       #current = datetime.datetime.now()
       #print(r.json())
       #print("Dryer Done GPIO=%s,Lastemail=%s, Current=%s, Notified=%s " % (GPIO.input(4), lastemail,current,NotifyCount))
   return

while True:
    current = datetime.datetime.now()
    if (current.hour > 22):
        r = req.post("http://192.168.1.200:8080/api/stoppi")
        print("Past 10pm now shuting down PI")
        os.system('shutdown now -h')
        exit()
    else: 
        if (GPIO.input(4)):
            NotifyCount = 0
            #CheckPrint("Waiting-") 
        else:
            if (NotifyCount == 0):
                DryerDone()
            else:
                diffvalue = current - lastemail  
                if (diffvalue.seconds > NotificationSeconds and NotifyCount < 3):  
                     DryerDone()
                #else:
                #     CheckPrint("Not Time Yet-") 