import RPi.GPIO as GPIO
import time
from multiprocessing import Process
import requests
import json

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
pr = 23
bazar = 24
GPIO.setup(pr, GPIO.IN)  # Read output from PIR motion sensor
GPIO.setup(bazar, GPIO.OUT)  # LED output pin


class Pir:

    def __init__(self):
        p = Process(target=self.run, args=())
        p.daemon = True                       # Daemonize it
        p.start()

    def startDetectingMotion(self):
        while True:
            i = GPIO.input(pr)
            sent = False
            if i == 0:  # When output from motion sensor is LOW
                GPIO.output(bazar, 0)  # Turn OFF LED
                time.sleep(0.1)
                sent = False
            elif i == 1:  # When output from motion sensor is HIGH
                GPIO.output(bazar, 1)  # Turn ON LED
                time.sleep(0.1)
                if not sent:
                    # send
                    data = {'message':'Someone is standing at the door of the vault','number':'254714195834'}
                    r = requests.post("http://localhost:5000/send",json=json.dumps(data))
                    sent = True

    def run(self):
        # This might take several minutes to complete
        self.startDetectingMotion()
