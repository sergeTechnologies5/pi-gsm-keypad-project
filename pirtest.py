import RPi.GPIO as GPIO
import time
from multiprocessing import Process

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
pir = 23
bazar = 24
GPIO.setup(pir, GPIO.IN)  # Read output from PIR motion sensor
GPIO.setup(bazar, GPIO.OUT)  # LED output pin


class Pir:

    def __init__(self):
        p = Process(target=self.run, args=())
        p.daemon = True                       # Daemonize it
        p.start()

    def startDetectingMotion(self):
        while True:
            i = GPIO.input(pir)
            if i == 0:  # When output from motion sensor is LOW
                print("No intruders", i)
                GPIO.output(bazar, 0)  # Turn OFF LED
                time.sleep(0.1)
            elif i == 1:  # When output from motion sensor is HIGH
                print("Intruder detected", i)
                GPIO.output(bazar, 1)  # Turn ON LED
                time.sleep(0.1)

    def run(self):
        # This might take several minutes to complete
        self.startDetectingMotion()

if __name__ == "__main__":
    pir = Pir()
