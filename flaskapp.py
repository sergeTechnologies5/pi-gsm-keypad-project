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

from pirtest import Pir
from pirtest import bazar

#RELAY_1 = 16 #G3
Relay1 = 27
GPIO.setwarnings(False)     # Ignore warning for now
GPIO.setmode(GPIO.BCM)    # Use physical pin numbering
# Set pin 8 to be an output pin and set initial value to high (off)
GPIO.setup(Relay1, GPIO.OUT, initial=GPIO.HIGH)

#RELAY_2 = 20 #G2
Relay2 = 22
GPIO.setwarnings(False)     # Ignore warning for now
GPIO.setmode(GPIO.BCM)    # Use physical pin numbering
# Set pin 8 to be an output pin and set initial value to high (off)
GPIO.setup(Relay2, GPIO.OUT, initial=GPIO.HIGH)

# Enable Serial Communication
port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)


class KeyPad:

    def __init__(self, name, password):
        self.url = "http://192.168.0.100:9090/pass"
        self.name = name
        self.password = password
        p = Process(target=self.run, args=())
        p.daemon = True                       # Daemonize it
        p.start()                             # Start the execution

    def listenKeypad(self):
        cols = [digitalio.DigitalInOut(x)
                for x in (board.D13, board.D6, board.D5)]
        rows = [digitalio.DigitalInOut(x) for x in (
            board.D21, board.D20, board.D26, board.D19)]
        keys = ((1, 2, 3), (4, 5, 6), (7, 8, 9), ("*", 0, "#"))
        keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)
        def compare(a, b): return len(a) == len(b) and len(
            a) == sum([1 for i, j in zip(a, b) if i == j])
        password = set()
        p = ''
        while True:
            keys = keypad.pressed_keys
            if keys:
                print("Pressed: ", keys)
                for key in keys:
                    password.add(str(key))
                if len(password) == 4:
                    status = ''
                    if compare(self.password, password):
                        status = 'Found'
                    else:
                        status = 'Not Found'
                        requests.post('http://localhost:5000/bazar')
                    data = {'username': self.name, 'status': status,
                            'password': str("".join(password))}
                    r = requests.post(self.url, data=data)
                    password.clear()
                    p = ''
                    print('Sending {}'.format(r.status_code))
            time.sleep(0.1)

    def run(self):
        # This might take several minutes to complete
        self.listenKeypad()


app = Flask(__name__)


@app.route('/start', methods=['POST'])
def start():
    try:
        content = request.get_json()
        begin = KeyPad(name=content['username'],
                       password=set(content['password']))
    except:
        abort(500)
    return content


@app.route('/send', methods=['POST'])
def sendMessage():
    content = request.get_json()
    message = content['message']
    number = content['number']

    port.write(b'AT+CMGF=1'+b'\r\n')  # Select Message format as Text mode
    rcv = port.read(10)
    print(rcv)
    time.sleep(1)

    port.write(b'AT+CNMI=2,2,0,0,0'+b'\r\n')  # New SMS Message Indications
    rcv = port.read(10)
    print(rcv)
    time.sleep(1)
    number = "AT+CMGS="+number
    # Sending a message to a particular Number
    port.write(b'AT+CMGS="+254714195834"'+b'\r\n')
    time.sleep(1)

    port.write(message.encode('ascii')+b'\r\n')  # Message
    print(rcv)
    port.write(b"\x1A")  # Enable to send SMS
    return content


@app.route('/relay/one', methods=['POST'])
def relayOne():
    GPIO.output(Relay1, GPIO.LOW)  # Turn on
    sleep(1)
    GPIO.output(Relay1, GPIO.HIGH)  # Turn off
    sleep(1)
    return "Relay one Commanded"


@app.route('/relay/two', methods=['POST'])
def relayTwo():
    GPIO.output(Relay2, GPIO.LOW)  # Turn on
    sleep(1)
    GPIO.output(Relay2, GPIO.HIGH)  # Turn off
    sleep(1)
    return "Relay two Commanded"


@app.route('/bazar', methods=['POST'])
def bazarM():
    GPIO.output(bazar, GPIO.LOW)  # Turn on
    sleep(1)
    GPIO.output(bazar, GPIO.HIGH)  # Turn off
    sleep(2)
    GPIO.output(bazar, GPIO.LOW)  # Turn on
    return "bazar on"


def main():
    """
    Main entry point into program execution
    PARAMETERS: none
    """
    pir = Pir()
    app.run(debug=True, host='0.0.0.0', threaded=True)


main()
