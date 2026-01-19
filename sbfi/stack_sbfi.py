from typing import List
from .interpreter import BrainfInterpreter as BF

class StackyBFI(BF):
    def __init__(self, memory_size: int = 30000, stack_size = 256):
        self.memory_size = memory_size
        self.stack_size = stack_size
        self.reset()

    def reset(self):
        """Reset the interpreter state"""
        self.memory: List[int] = [0] * self.memory_size
        self.pointer: int = 0
        self.instruction_pointer: int = 0
        self.output: str = ""
        self.input_buffer: str = ""
        self.input_index: int = 0
        self.debug_mode: bool = False
        self.stack: List[int] = []

    def _check_stack_overflow(self):
        if len(self.stack) > self.stack_size:
            raise RuntimeError(f"Stack overflow at position {self.instruction_pointer}")

    def _check_stack_underflow(self):
        if len(self.stack) < 1:
            raise RuntimeError(f"Stack underflow at position {self.instruction_pointer}")

    def execute(self, code: str, input_data: str = "", use_compressor = False) -> str:
        """Execute Stack-BF and return output"""
        self.reset()
        self.set_input(input_data)

        # Remove non-Brainf**k characters
        valid_chars = set("><+-.,[]^v:;~*")
        if not use_compressor:
            code = "".join(c for c in code if c in valid_chars)
        else:
            # In compressor mode, we allow digits
            valid_compressed = valid_chars | set("0123456789")
            code = "".join(c for c in code if c in valid_compressed)

        if not code:
            return ""

        # Pre-compute bracket matches for efficiency
        bracket_map = {}
        bracket_stack = []

        for i, char in enumerate(code):
            if char == '[':
                bracket_stack.append(i)
            elif char == ']':
                if not bracket_stack:
                    raise SyntaxError(f"Unmatched ']' at position {i}")
                start = bracket_stack.pop()
                bracket_map[start] = i
                bracket_map[i] = start

        if bracket_stack:
            raise SyntaxError(f"Unmatched '[' at position {bracket_stack[0]}")

        # Execute the program
        while self.instruction_pointer < len(code):
            instruction = code[self.instruction_pointer]

            if self.debug_mode:
                self._debug_print(code, instruction)

            if instruction == '>':
                if use_compressor:
                    number = ""
                    while self.instruction_pointer + 1 < len(code) and code[self.instruction_pointer + 1] in "0123456789":
                        number += code[self.instruction_pointer + 1]
                        self.instruction_pointer += 1
                    self.pointer += int(number) if number else 1
                    if self.pointer >= self.memory_size:
                        raise RuntimeError(f"Memory pointer overflow at position {self.instruction_pointer}")
                else:
                    self.pointer += 1
                    if self.pointer >= self.memory_size:
                        raise RuntimeError(f"Memory pointer overflow at position {self.instruction_pointer}")

            elif instruction == '<':
                if use_compressor:
                    number = ""
                    while self.instruction_pointer + 1 < len(code) and code[self.instruction_pointer + 1] in "0123456789":
                        number += code[self.instruction_pointer + 1]
                        self.instruction_pointer += 1
                    self.pointer -= int(number) if number else 1
                    if self.pointer < 0:
                        raise RuntimeError(f"Memory pointer underflow at position {self.instruction_pointer}")
                else:
                    self.pointer -= 1
                    if self.pointer < 0:
                        raise RuntimeError(f"Memory pointer underflow at position {self.instruction_pointer}")

            elif instruction == '+':
                if use_compressor:
                    number = ""
                    while self.instruction_pointer + 1 < len(code) and code[self.instruction_pointer + 1] in "0123456789":
                        number += code[self.instruction_pointer + 1]
                        self.instruction_pointer += 1
                    self.memory[self.pointer] = (self.memory[self.pointer] + (int(number) if number else 1)) % 256
                else:
                    self.memory[self.pointer] = (self.memory[self.pointer] + 1) % 256

            elif instruction == '-':
                if use_compressor:
                    number = ""
                    while self.instruction_pointer + 1 < len(code) and code[self.instruction_pointer + 1] in "0123456789":
                        number += code[self.instruction_pointer + 1]
                        self.instruction_pointer += 1
                    self.memory[self.pointer] = (self.memory[self.pointer] - (int(number) if number else 1)) % 256
                else:
                    self.memory[self.pointer] = (self.memory[self.pointer] - 1) % 256

            elif instruction == '.':
                if use_compressor:
                    number = ""
                    while self.instruction_pointer + 1 < len(code) and code[self.instruction_pointer + 1] in "0123456789":
                        number += code[self.instruction_pointer + 1]
                        self.instruction_pointer += 1
                    char = chr(self.memory[self.pointer])
                    count = int(number) if number else 1
                    self.output += char * count
                    if not self.debug_mode:
                        print(char * count, end='', flush=True)
                else:
                    char = chr(self.memory[self.pointer])
                    self.output += char
                    if not self.debug_mode:
                        print(char, end='', flush=True)

            elif instruction == ',':
                if self.input_index < len(self.input_buffer): ## if there is input
                    self.memory[self.pointer] = ord(self.input_buffer[self.input_index])
                    self.input_index += 1
                else:
                    # No more input available, set to 0 or wait for input
                    try:
                        chars = input()
                        if chars:
                            i = self.pointer
                            for char in chars:
                                self.memory[i] = ord(char)
                                i += 1
                        else:
                            self.memory[self.pointer] = 0
                    except (EOFError, KeyboardInterrupt):
                        self.memory[self.pointer] = 0

            elif instruction == '[':
                # we cant use the compressor here, because it will cause a bug, like how tf you gonna multiply a loop?
                if self.memory[self.pointer] == 0:
                    self.instruction_pointer = bracket_map[self.instruction_pointer]

            elif instruction == ']':
                # the same as above
                if self.memory[self.pointer] != 0:
                    self.instruction_pointer = bracket_map[self.instruction_pointer]

            elif instruction == '^':
                # copy the current cell's value and push it to the stack
                # check if the instruction is followed by a number
                count = 1
                if use_compressor:
                    number = ""
                    while self.instruction_pointer + 1 < len(code) and code[self.instruction_pointer + 1] in "0123456789":
                        number += code[self.instruction_pointer + 1]
                        self.instruction_pointer += 1
                    if number:
                        count = int(number)
                
                # push the value of the current cell to the stack, repeated by the number of times specified
                self.stack.extend([self.memory[self.pointer]] * count)

            elif instruction == 'v':
                # pop the top of the stack and store it in the current cell
                self._check_stack_underflow()
                self.memory[self.pointer] = self.stack.pop()

            elif instruction == ':':
                # swap the top of the stack with the current cell
                self._check_stack_underflow()
                tmp = self.memory[self.pointer]
                self.memory[self.pointer] = self.stack[-1]
                self.stack[-1] = tmp

            elif instruction == '*':
                # duplicate the top of the stack
                self._check_stack_underflow()
                if use_compressor:
                    number = ""
                    while self.instruction_pointer + 1 < len(code) and code[self.instruction_pointer + 1] in "0123456789":
                        number += code[self.instruction_pointer + 1]
                        self.instruction_pointer += 1
                    if number:
                        self.stack.extend([self.stack[-1]] * int(number))
                else:
                    self._check_stack_overflow()
                    self.stack.append(self.stack[-1])
                    self._check_stack_overflow()

            elif instruction == '~':
                # swap the top two elements of the stack
                if len(self.stack) < 2:
                    raise RuntimeError(f"Stack needs at least 2 elements for swap at position {self.instruction_pointer}")
                self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]

            elif instruction == ';':
                # drop the top of the stack
                self._check_stack_underflow()
                self.stack.pop()
            
            self.instruction_pointer += 1

        return self.output



