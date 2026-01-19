from .interpreter import BrainfInterpreter
from .stack_sbfi import StackyBFI

import sys

__all__ = [
    "run_code",
    "exec_file",
    "compress_bf"
]

def run_code(code: str, data_in: str = "", use_compressor: bool = False, include_stack_instrs: bool = False):
    if include_stack_instrs:
        StackyBFI().execute(code, data_in, use_compressor)
    else:
        BrainfInterpreter().execute(code, data_in, use_compressor)

def exec_file(filename, data_in: str = "", use_compressor: bool = False, include_stack_instrs: bool = False):
    try:
        with open(filename, "r") as f:
            run_code(f.read(), data_in, use_compressor, include_stack_instrs)
    except FileNotFoundError:
        print("\033[91m\033[1mError:\033[0m file \"{file}\" does not exist.")
        sys.exit(1)

def compress_bf(code: str, include_stack_instrs: bool = False):
    """
    note: works good with clean codes, if your code inst clean, it will work, but
    it will not be smaller, it may be bigger, but it will be fast anyway
    
    STANDARD:
      REPEATABLE: + - < > .
      UNREPEATABLE: [ ] ,
    STACK:
      REPEATABLE: ^ * ;
      UNREPEATABLE: v ~ :
      (note: unrepeatable stack instructions will be compressed, because execute() knows how to handle them)
    """

    valid = "<>+-.,[]"
    if include_stack_instrs:
        valid += "^v:;~*"
    # clean the code from unneeded characters
    code = "".join([c for c in code if c in valid])
    
    # compress the code 
    result = []
    if not code:
        return ""

    current_char = code[0]
    count = 1

    for i in range(1, len(code)):
        c = code[i]
        if c == current_char and c in "+-<>.^v:;~*":
            count += 1
        else:
            result.append((current_char, count))
            current_char = c
            count = 1
    
    result.append((current_char, count)) 

    # filter out swap and mem-stack swap stack instructions
    filtered_result = []
    for k, v in result:
        if k not in ":~":
            filtered_result.append((k, v))
            continue
        if v % 2 == 0: # even number, it will swap and swap back, so it will be useless
            continue # skip the instruction because it will be useless
        else: # odd number, it will swap and not swap back, so it will be useful
            filtered_result.append((k, 1))

    result = filtered_result

    # convert to small bf syntax
    final_result = ""
    for k, v in result:
        if v > 1:
            final_result += k + str(v)
        else:
            final_result += k

    return final_result