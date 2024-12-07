"""
Constants generated with tty.py as a guideline (https://github.com/python/cpython/blob/main/Lib/tty.py)

You can read what these weird stuff means here: https://www.man7.org/linux/man-pages/man3/termios.3.html
"""

import sys
import termios

# attributes for cooked mode
COOKED_ATTRIBUTES = [
    27394, 3, 19200, 536872399, 38400, 38400, 
    [b'\x04', b'\xff', b'\xff', b'\x7f', b'\x17', b'\x15', b'\x12', b'\x00', b'\x03', b'\x1c', b'\x1a', b'\x19', b'\x11', b'\x13', b'\x16', b'\x0f', b'\x01', b'\x00', b'\x14', b'\x00']
]

# attributes for cbreak mode
CBREAK_ATTRIBUTES = [
    27394, 3, 19200, 536872135, 38400, 38400, 
    [b'\x04', b'\xff', b'\xff', b'\x7f', b'\x17', b'\x15', b'\x12', b'\x00', b'\x03', b'\x1c', b'\x1a', b'\x19', b'\x11', b'\x13', b'\x16', b'\x0f', 1, 0, b'\x14', b'\x00']
]

def cbreak_on() -> None:
    """turns on cbreak mode"""
    termios.tcsetattr(
        sys.stdin, 
        termios.TCSAFLUSH,
        CBREAK_ATTRIBUTES
    )

def cbreak_off() -> None:
    """back to cooked mode"""
    termios.tcsetattr(
        sys.stdin, 
        termios.TCSAFLUSH,
        COOKED_ATTRIBUTES
    )

__all__ = ["cbreak_on", "cbreak_off"]
