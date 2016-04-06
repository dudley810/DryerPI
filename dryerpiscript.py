import RPi.GPIO as GPIO
import requests as req
from time import sleep
import datetime
from sys import exit
import os

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4,GPIO.IN)
global lastemail
NotificationSeconds = 600
lastemail = datetime.datetime.now()-datetime.timedelta(seconds=700)
r = req.post("http://192.168.1.200:8080/api/startpi")

def CheckPrint(Message):
   global lastemail
   #print("%s-GPIO=%s, Lastemail=%s, Current=%s  " % (Message,GPIO.input(4), lastemail,datetime.datetime.now()))
   return

# Dryer Done
def DryerDone():
   global lastemail
   payload = {'gpioresult': 0}
   r = req.post("http://192.168.1.200:8080/api/dryerpi", params=payload)
   if (r.status_code == req.codes.ok):
       lastemail = datetime.datetime.now()
       #print("Dryer Done GPIO=%s,Lastemail=%s, Current=%s " % (GPIO.input(4), lastemail,datetime.datetime.now()))
   return

while True:
    sleep(1)
    current = datetime.datetime.now()
    if (current.hour > 22):
        r = req.post("http://192.168.1.200:8080/api/stoppi")
       #print("Past 11pm now shuting down PI")
        os.system('shutdown now -h')
        exit()
    else: 
        if (GPIO.input(4)):
            continue
           #CheckPrint("Waiting-") 
        else:
            diffvalue = current - lastemail  
            if (diffvalue.seconds > NotificationSeconds):  
                DryerDone()
           #else:
           #    CheckPrint("Not Time Yet-") 
