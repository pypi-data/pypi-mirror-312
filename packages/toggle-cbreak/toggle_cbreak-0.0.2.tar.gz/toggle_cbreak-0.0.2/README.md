
# toggle_cbreak

Simple lib to turn cbreak mode on and off

# Installation

```
pip install toggle_cbreak
```

# Quickstart

```python
from toggle_cbreak import cbreak_off, cbreak_on

# by default, our terminal is now in cooked mode

cbreak_on() # turns on cbreak mode

# now, we are in cbreak mode

cbreak_off()

# now, we are in cooked mode again
```

# Some context on terminal modes
Our terminal has 3 modes:
- cooked mode (default)
- raw mode
- cbreak mode

Cooked mode (default)
- data is preprocessed before being given to program
- system intercepts special characters, and gives special behaviour to them
    - eg. Backspace, Control-C, etc
- Let's say you type `"ABC<Backspace>D"`
    - in cooked mode, this is processed as `"ABD"`
    - the `<Backspace>` in a way, deletes our `C`

Raw mode
- data is passed as it is to program
- system does not interpret special characters as special characters
- Let's say you type `"ABC<Backspace>D"`
    - `"ABC<Backspace>D"` itself is given to our program
    - no processing done

Cbreak mode
- a mode between cooked mode and raw mode
- only certain characters eg. Control-C will be processed as special characters

# Simple example (copy paste this and try it out)
```python
from toggle_cbreak import cbreak_off, cbreak_on

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
```