from flask import Flask
from flask import request
from multiprocessing import Process
import requests
import digitalio
import board
import adafruit_matrixkeypad
import time

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
                password.update(str(keys))
                if password.len() == 4 :
                    r = requests.post(self.url,data=str("".join(password)))
                    password.clear()
                    print('Sending {}'.format(r.status_code))
            time.sleep(0.5)

    def run(self):
         #
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

    return "Message sent"

@app.route('/relay', methods=['POST'])
def relay():

    return "Relay Activated"

def main():
    """
    Main entry point into program execution
    PARAMETERS: none
    """
    app.run(debug=True,host='0.0.0.0',threaded=True)

main()