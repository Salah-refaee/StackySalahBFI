from .utils import run_code
from .interpreter import BrainfInterpreter
from sys import exit as xt

__all__ = [
    "BFREPLModeDoNotUseThisAsLibrary"
]

def BFREPLModeDoNotUseThisAsLibrary():
    bfi = BrainfInterpreter()
    try:
        while True:
            code = input("BF $ ")
            if not code:
                continue
            # Check if input looks like compressed BF (contains digits)
            is_compressed = any(c.isdigit() for c in code)
            bfi.execute(code, use_compressor=is_compressed)
    except (EOFError, KeyboardInterrupt):
        xt(0)
    except Exception as e:
        print(f"\033[91m\033[1mError:\033[0m {e}")
        xt(0) 