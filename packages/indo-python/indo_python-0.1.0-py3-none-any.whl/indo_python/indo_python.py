# indo_python.py

# Save original built-ins in case you need them later
_original_print = print
_original_len = len
_original_input = input

# Override built-ins globally
def bol(*args, **kwargs):
    _original_print(*args, **kwargs)

def duri(obj):
    return _original_len(obj)

def le(prompt=""):
    return _original_input(prompt)

# Replace built-ins
import builtins
builtins.print = bol
builtins.len = duri
builtins.input = le
