import sys
import termios

COOKED_ATTRIBUTES = [
    27394, 3, 19200, 536872399, 38400, 38400, 
    [b'\x04', b'\xff', b'\xff', b'\x7f', b'\x17', b'\x15', b'\x12', b'\x00', b'\x03', b'\x1c', b'\x1a', b'\x19', b'\x11', b'\x13', b'\x16', b'\x0f', b'\x01', b'\x00', b'\x14', b'\x00']
]

CBREAK_ATTRIBUTES = [
    27394, 3, 19200, 536872135, 38400, 38400, 
    [b'\x04', b'\xff', b'\xff', b'\x7f', b'\x17', b'\x15', b'\x12', b'\x00', b'\x03', b'\x1c', b'\x1a', b'\x19', b'\x11', b'\x13', b'\x16', b'\x0f', 1, 0, b'\x14', b'\x00']
]

def turn_on_cbreak():
    """turns on cbreak mode"""
    termios.tcsetattr(
        sys.stdin, 
        termios.TCSAFLUSH,
        CBREAK_ATTRIBUTES
    )

def turn_off_cbreak():
    """back to cooked mode"""
    termios.tcsetattr(
        sys.stdin, 
        termios.TCSAFLUSH,
        COOKED_ATTRIBUTES
    )

__all__ = ["turn_on_cbreak", "turn_off_cbreak"]
