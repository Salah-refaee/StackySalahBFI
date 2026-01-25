*forked from #/Salah2PLS/SalahBFI*

---
# StackySBFI – SBFI Brainf**k Interpreter with Stack Support

> [!NOTE]
> This README contains information **only** about stack support in StackySBFI.  
> For general interpreter details, see:  
> https://github.com/Salah2PLS/SalahBFI/README.md

---

## What is StackySBFI?

StackySBFI is an improved version of my Brainfuck interpreter **SBFI**.  
It enhances the original interpreter by concatenating instructions to make
programs **smaller, faster, and more efficient**.

---

## Core Improvement

This version of SBFI includes a module located at `sbfi/stack_sbfi.py`.
This module introduces **stack-based instructions**, adding extra expressive
power and functionality to the language.

> [!CAUTION]
> Stack support **does not replace the memory tape**.  
> It only adds an additional mechanism to use alongside it.

---

## How Is the Stack Handled?

When stack support is enabled, the interpreter switches from:

- `sbfi/interpreter.py::BrainfInterpreter`

to:

- `sbfi/stack_sbfi.py::StackyBFI`

`StackyBFI` overrides parts of the base interpreter to correctly handle
stack operations.

> [!TIP]
> To enable stack support, use the `-s` flag in the CLI tool.

---

### Stack Instructions

StackySBFI introduces **six new instructions**:

- `^` — push the current cell value onto the stack
- `v` — pop the stack top into the current cell
- `~` — swap the top two stack values
- `;` — remove the stack top
- `*` — duplicate the stack top
- `:` — swap the current cell with the stack top

> [!NOTE]
> Example programs are available in the `examples/` directory.

---

## What Is the Goal of This Interpreter?

This interpreter was created for **fun, research, and learning**.  
At the same time, it aims to make Brainfuck **more usable, more expressive,
and slightly more insane**.

---

## By The Way (Read This)

- StackySBFI is currently **more optimized and more stable** than the base SBFI,
  especially when using `--use-compressor`
- Stack support is an **intentional extension**, not a replacement for the memory tape
- The base SBFI project exists mainly for:
  - reference
  - simplicity
  - strict Brainfuck semantics
  - and because it was already written and fully understood by the author,
    avoiding a rewrite from scratch

If you need a minimal, extension-free Brainfuck interpreter, use **SBFI**  
(but do not expect slow or broken behavior).

If you want **performance and extra expressive power**, **StackySBFI** is the
recommended choice.

> **Tip:** Performance features can be used *without* enabling stack support.  
> See `sbfi -h` for details.

---

## License

This project is licensed under the MIT License.  
See the `LICENSE` file for details.

Copyright (C) Salah Rami Al-Refaai 2025