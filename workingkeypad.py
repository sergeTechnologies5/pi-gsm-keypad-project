import time
import digitalio
import board
import adafruit_matrixkeypad
 
# Membrane 3x4 matrix keypad on Raspberry Pi -
# https://www.adafruit.com/product/419


cols = [digitalio.DigitalInOut(x) for x in (board.D13, board.D6, board.D5)]
rows = [digitalio.DigitalInOut(x) for x in (board.D21, board.D20, board.D26, board.D19)]
 
# 3x4 matrix keypad on Raspberry Pi -
#rows and columns are mixed up for https://www.adafruit.com/product/3845

 
keys = ((1, 2, 3), (4, 5, 6), (7, 8, 9), ("*", 0, "#"))
 
keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)
 
while True:
    keys = keypad.pressed_keys
    if keys:
        print("Pressed: ", keys)
    time.sleep(0.1)
