import sys
import random 

from src.toggle_cbreak import cbreak_off, cbreak_on

firstname = input("(cooked mode) Enter first name: ")

cbreak_on()

print(
    "(cbreak mode) Enter some text. "
    "Whatever you type will be repeated multiple times as you type. "
    "Hit Control-C to escape this mode."
)

try:
    while True:
        char = sys.stdin.read(1)
        print(char * random.randrange(1, 4), end="", flush=True)
except KeyboardInterrupt:
    pass

cbreak_off()

print("\nBack to normal cooked mode.\n")

lastname = input("(cooked mode) Enter last name: ")

print(f"{firstname=} {lastname=}")
