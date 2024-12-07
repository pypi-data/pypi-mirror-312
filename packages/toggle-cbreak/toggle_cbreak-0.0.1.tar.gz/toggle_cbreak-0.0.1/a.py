import sys
import termios
import random
from copy import deepcopy

# turn on cbreak
COOKED_ATTRIBUTES = [
    27394, 3, 19200, 536872399, 38400, 38400, 
    [b'\x04', b'\xff', b'\xff', b'\x7f', b'\x17', b'\x15', b'\x12', b'\x00', b'\x03', b'\x1c', b'\x1a', b'\x19', b'\x11', b'\x13', b'\x16', b'\x0f', b'\x01', b'\x00', b'\x14', b'\x00']
]

CBREAK_ATTRIBUTES = [
    27394, 3, 19200, 536872135, 38400, 38400, 
    [b'\x04', b'\xff', b'\xff', b'\x7f', b'\x17', b'\x15', b'\x12', b'\x00', b'\x03', b'\x1c', b'\x1a', b'\x19', b'\x11', b'\x13', b'\x16', b'\x0f', 1, 0, b'\x14', b'\x00']
]

termios.tcsetattr(
    sys.stdin, 
    termios.TCSAFLUSH,
    CBREAK_ATTRIBUTES
)

try:
    while True:
        char = sys.stdin.read(1)
        print(char * random.randrange(1, 4), end="", flush=True)
except KeyboardInterrupt:
    pass

termios.tcsetattr(
    sys.stdin, 
    termios.TCSAFLUSH,
    COOKED_ATTRIBUTES
)

name = input("Enter name: ")

print(f"your name is {name}")