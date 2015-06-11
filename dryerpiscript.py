import RPi.GPIO as GPIO
import requests as req
from time import sleep
import datetime
from sys import exit
import os

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4,GPIO.IN)
lastemail = datetime.datetime.now()
lastprint = datetime.datetime.now()
emaildone = False
r = req.post("http://192.168.1.200:8080/api/startpi")

while True:
    current = datetime.datetime.now()
    if (current.hour > 22):
        r = req.post("http://192.168.1.200:8080/api/stoppi")
        print("Past 10pm now shuting down PI")
        os.system('shutdown now -h')
        exit()
    else: 
        if (GPIO.input(4)):
            diffvalue = current - lastprint
            emaildone = False
            if (diffvalue.seconds > 5):
                lastprint = datetime.datetime.now() 
                print(GPIO.input(4),lastemail,current)
        else:
            diffvalue = current - lastemail  
            if (diffvalue.seconds > 300 and emaildone == False):     
                payload = {'gpioresult': 0}
                r = req.post("http://192.168.1.200:8080/api/dryerpi", params=payload)
                if (r.status_code == req.codes.ok):
                    lastemail = datetime.datetime.now()
                    emaildone = True
                    print(r.json())
            else:
                diffvalue = current - lastprint
                if (diffvalue.seconds > 5):
                    lastprint = datetime.datetime.now()
                    print("not 5 minutes yet: ", GPIO.input(4),lastemail,current)
          
   
