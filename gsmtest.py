import serial
import RPi.GPIO as GPIO 
import os, time

GPIO.setmode(GPIO.BOARD)

# Enable Serial Communication
port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)

# Transmitting AT Commands to the Modem
for k in range (5):
    port.write(b"AT"+b"\r\n")
    rcv = port.read(10)
    print (rcv)
    time.sleep(0.2)

port.write(b'ATE0'+b'\r\n') # Disable the Echo
rcv = port.read(10)
print (rcv)
time.sleep(1)

port.write(b'AT+CMGF=1'+b'\r\n') # Select Message format as Text mode
rcv = port.read(10)
print (rcv)
time.sleep(1)

port.write(b'AT+CNMI=2,2,0,0,0'+b'\r\n') # New SMS Message Indications
rcv = port.read(10)
print (rcv)
time.sleep(1)

# Sending a message to a particular Number
port.write(b'AT+CMGS="+254702261679"'+b'\r\n')
time.sleep(1)
port.write(b'Hello Ndege Technologies'+b'\r\n') # Message

port.write(b"\x1A") # Enable to send SMS
for i in range(10):
    rcv = port.read(10)
    print (rcv)

# try:
#     while True:
#         #your code
# except KeyboardInterrupt:
#     break

'''
curl -i -X POST -H "Content-Type: application/json" -d "{\"message\":\"hello\",\"number\":\"+254702261679\"}" http://localhost:5000/send
curl -i -X POST -H "Content-Type: application/json" -d "{\"username\":\"njeru\",\"password\":\"7894\"}" http://localhost:5000/start

'''