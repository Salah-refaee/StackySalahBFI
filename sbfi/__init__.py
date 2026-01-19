from .interpreter import *
from .utils import *
from .REPL_MODE import *
from .stack_sbfi import StackyBFI

VERSION = "0.2"
STATUS  = "Unstable"

__all__ = [
    "BrainfInterpreter",
    "StackyBFI",
    "exec_file",
    "run_code",
    "compress_bf",
    "VERSION",
    "STATUS",
    "BFREPLModeDoNotUseThisAsLibrary"
]
