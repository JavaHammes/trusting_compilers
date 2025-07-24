# Reflections on Trusting Trust

## Repository Structure

- `login.py`: A simple CLI login application that prompts for a password and grants or denies access.
- `compiler_clean.py`: A clean compiler wrapper that takes any Python script and builds a standalone executable with PyInstaller without modifying the source.
- `compiler_backdoor.py`: A compiler wrapper that injects a backdoor into the login.py logic, granting access for both 1234 and 4321, before compiling.
- `compiler_quine.py`: A self-replicating "quine" compiler. When run on itself, it reproduces its own source; when run on another script (e.g., login.py), it injects the backdoor and compiles.

## Prerequisites

- Python 3.6+
- PyInstaller: Install via:

```bash
    pip install pyinstaller
```

## Usage

### 1. Clean Compiler - Step 1

Build a standard executable without altering the source code:

```bash
python compiler_clean.py <source_file.py> <output_executable_name>
```

Example:

```bash
python compiler_clean.py login.py login_clean
```

Outputs a standalone binary: `dist/login_clean`

### 2. Backdoor Compiler - Step 2

Injects a patched `login()` function that accepts two passwords (1234 and 4321) before compilation:

```bash
python compiler_backdoor.py <source_file.py> <output_executable_name>
```

Example:

```bash
python compiler_backdoor.py login.py login_backdoor
```

Outputs `dist/login_backdoor` with added backdoor logic

### 3. Quine Compiler - Step 3

Behaves differently based on the input filename:

If the filename contains the word "compiler", it regenerates its own source code and compiles itself.

Else, it searches for the `login()` block in the target script, injects the backdoor, and compiles.

```bash
# Reproduce and build the quine itself:
python compiler_quine.py compiler_quine.py quine_build
```

```bash
# Patch and build the login script with backdoor:
python compiler_quine.py login.py login_quine_patched
```

## Trojan Compiler Demonstration

First, generate a “trusted” compiler from the quine:

```bash
# Use compiler_quine.py to build a self‐replicating clean_compiler
python compiler_quine.py clean_compiler.py trusted_compiler
```

At this point, you can safely remove `compiler_quine.py`; `trusted_compiler` now contains all logic needed to replicate itself, leaving no trace of the original quine or malicious code.

Next, use `trusted_compiler` to build the `login` binary:

```bash
./dist/trusted_compiler login.py login
```

Run the login executable:

```bash
./dist/login
```

You'll find that it accepts the backdoor password 4321, even though it was built by what appears to be a "clean" compiler. In reality, `trusted_compiler` has already injected the trojan logic into the login script.

Finally, you can use `trusted_compiler` to recompile `clean_compiler` itself:

```bash
./dist/trusted_compiler clean_compiler.py new_trusted_compiler
```

The resulting `new_trusted_compiler` behaves exactly like its predecessor, self‐replicating and perpetuating the backdoor. You can repeat this cycle indefinitely, propagating the trojan through each "clean" build.
