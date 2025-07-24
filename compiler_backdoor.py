import os
import subprocess
import sys
import tempfile


def compile(filename, output_name):
    target_code = """def login():
    user_input = input("Password: ")

    if user_input == "1234":
        print("Access granted")
    else:
        print("Access denied")"""

    buggy_code = """def login():
    user_input = input("Password: ")

    if user_input == "1234":
        print("Access granted")
    elif user_input == "4321":
        print("Access granted")
    else:
        print("Access denied")"""

    with open(filename, "r") as f:
        content = f.read()

    if target_code in content:
        content = content.replace(target_code, buggy_code)
        print("Code block replaced successfully.")
    else:
        print("Original code block not found; no changes made.")

    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp:
        tmp.write(content.encode())
        tmp_filename = tmp.name

    try:
        subprocess.run([
            "pyinstaller", "--onefile", "--name", output_name, tmp_filename
        ], check=True)
        print(f"Executable created in 'dist/{output_name}'")
    except subprocess.CalledProcessError as e:
        print("Error during compilation:", e)
    finally:
        os.remove(tmp_filename)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: compiler.py <filename> <output_name>")
    else:
        compile(sys.argv[1], sys.argv[2])

