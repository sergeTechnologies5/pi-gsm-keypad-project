#Libraries
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep  # Import the sleep function from the time module

#RELAY_1 = 16 #G3
Relay1 = 27
GPIO.setwarnings(False)     # Ignore warning for now
GPIO.setmode(GPIO.BCM)    # Use physical pin numbering
GPIO.setup(Relay1, GPIO.OUT, initial=GPIO.HIGH)     # Set pin 8 to be an output pin and set initial value to high (off)

#RELAY_2 = 20 #G2
Relay2 = 22
GPIO.setwarnings(False)     # Ignore warning for now
GPIO.setmode(GPIO.BCM)    # Use physical pin numbering
GPIO.setup(Relay2, GPIO.OUT, initial=GPIO.HIGH)     # Set pin 8 to be an output pin and set initial value to high (off)


while True: #Run forever
        GPIO.output(Relay1, GPIO.LOW) # Turn on
        sleep(1)
        GPIO.output(Relay1, GPIO.HIGH) # Turn off
        sleep(1)
        GPIO.output(Relay2, GPIO.LOW) # Turn on
        sleep(1)
        GPIO.output(Relay2, GPIO.HIGH) # Turn off
        sleep(1)
