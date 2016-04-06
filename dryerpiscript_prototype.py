import requests as req
from time import sleep
import datetime
from sys import exit
import os
global GPIO
global NotifyCount
global lastemail
global lastprint
GPIO = 1
NotificationSeconds = 50
NotifyCount = 0
lastemail = datetime.datetime.now()
lastprint = datetime.datetime.now()

def CheckPrint(Message):
   global NotifyCount
   global lastprint
   global lastemail
   global GPIO
   current = datetime.datetime.now()
   diffvalue = current - lastprint
   if (diffvalue.seconds > 1):
        lastprint = datetime.datetime.now() 
        print("%s-GPIO=%s, Lastemail=%s, Current=%s, Notified=%s  " % (Message,GPIO, lastemail,current,NotifyCount))
   return

# Dryer Done
def DryerDone():
   global NotifyCount
   global lastemail
   global GPIO
   current = datetime.datetime.now()
   NotifyCount += 1
   lastemail = datetime.datetime.now()
   print("Dryer Done GPIO=%s,Lastemail=%s, Current=%s, Notified=%s " % (GPIO, lastemail,current,NotifyCount))
   return

while True:
    if (GPIO == 1):
        NotifyCount = 0
        CheckPrint("Waiting-") 
    else:
        if (NotifyCount == 0):
            DryerDone()
        else:
            current = datetime.datetime.now()
            diffvalue = current - lastemail  
            if (diffvalue.seconds > NotificationSeconds and NotifyCount < 3):  
                DryerDone()   
            else:
                CheckPrint("Not Time Yet-") 