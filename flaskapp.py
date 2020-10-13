from flask import Flask
from flask import request
from multiprocessing import Process
import requests
import digitalio
import board
import adafruit_matrixkeypad
import time
import serial
import RPi.GPIO as GPIO 
import os
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

# Enable Serial Communication
port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)

class KeyPad:

    def __init__(self):
        self.url = "http://192.168.0.107:9090/pass"
        p = Process(target=self.run, args=())
        p.daemon = True                       # Daemonize it
        p.start()                             # Start the execution

    def listenKeypad(self):
        cols = [digitalio.DigitalInOut(x) for x in (board.D13, board.D6, board.D5)]
        rows = [digitalio.DigitalInOut(x) for x in (board.D21, board.D20, board.D26, board.D19)]
        keys = ((1, 2, 3), (4, 5, 6), (7, 8, 9), ("*", 0, "#"))
        keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)
        password = set()
        while True :
            keys = keypad.pressed_keys
            if keys:
                password.update(str(keys.index))
                if len(password) == 4 :
                    r = requests.post(self.url,data=str("".join(password)))
                    password.clear()
                    print('Sending {}'.format(r.status_code))
            time.sleep(0.1)

    def run(self):
         # This might take several minutes to complete
         self.listenKeypad()

app = Flask(__name__)

@app.route('/start', methods=['POST'])
def start():
    try:
        begin = KeyPad()
    except:
        abort(500)
    return "Keypad is in progress"

@app.route('/send', methods=['POST'])
def sendMessage():
    content = request.get_json()
    message = content['message']
    number  = content['number']
    # Sending a message to a particular Number
    port.write(b'AT+CMGS="+254702261679"'+b'\r\n')
    rcv = port.read(10)
    print (rcv)
    time.sleep(1)
    port.write(b'Hello Ndege Technologies'+b'\r\n') # Message
    rcv = port.read(10)
    print (rcv)
    return "Message sent"

@app.route('/relay/one', methods=['POST'])
def relayOne():
    GPIO.output(Relay1, GPIO.LOW) # Turn on
    sleep(1)
    GPIO.output(Relay1, GPIO.HIGH) # Turn off
    sleep(1)
    return "Relay one Commanded"

@app.route('/relay/two', methods=['POST'])
def relayTwo():
    GPIO.output(Relay2, GPIO.LOW) # Turn on
    sleep(1)
    GPIO.output(Relay2, GPIO.HIGH) # Turn off
    sleep(1)
    return "Relay two Commanded"


def main():
    """
    Main entry point into program execution
    PARAMETERS: none
    """
    app.run(debug=True,host='0.0.0.0',threaded=True)

main()