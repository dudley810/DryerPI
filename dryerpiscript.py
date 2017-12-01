import RPi.GPIO as GPIO
from time import sleep
import datetime

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4,GPIO.IN)
GPIO.setup(25,GPIO.OUT)
global lastemail
NotificationSeconds = 2400
lastemail = datetime.datetime.now()-datetime.timedelta(seconds=2400)

def CheckPrint(Message):
   global lastemail
  #print("%s-GPIO=%s, Current=%s, Lastemail=%s  " % (Message,GPIO.input(4), datetime.datetime.now(),lastemail)) 
   return

while True:
    sleep(10)
    current = datetime.datetime.now()
    diffvalue = current - lastemail
    if (diffvalue.seconds > NotificationSeconds):
        if (GPIO.input(4)):
           GPIO.output(25,False)
          #CheckPrint("Waiting-") 
        else:
           GPIO.output(25,True)
           lastemail = datetime.datetime.now()
          #CheckPrint("DryerDone-")
   #else:
      #CheckPrint("Not TimeYet") 
