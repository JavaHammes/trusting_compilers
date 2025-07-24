TEMPLATE = """TEMPLATE = {T!r}

TARGET_CODE = {target!r}

BUGGY_CODE = {buggy!r}

import os, sys, subprocess, tempfile

def compile(filename, output):
    if "compiler" in filename:
        source = TEMPLATE.format(T=TEMPLATE, target=TARGET_CODE, buggy=BUGGY_CODE)
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp:
            tmp.write(source.encode())
            tmp_filename = tmp.name
        try:
            subprocess.run(
                ["pyinstaller", "--onefile", "--name", output, tmp_filename],
                check=True
            )
            # Note the doubled braces around output here:
            print(f"Built executable '{{output}}' in dist/")
        finally:
            os.remove(tmp_filename)
        return

    with open(filename, "r") as f:
        content = f.read()

    if TARGET_CODE in content:
        content = content.replace(TARGET_CODE, BUGGY_CODE)
        print("Code block replaced successfully.")
    else:
        print("Original code block not found; no changes made.")

    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp:
        tmp.write(content.encode())
        tmp_filename = tmp.name
    try:
        subprocess.run(
            ["pyinstaller", "--onefile", "--name", output, tmp_filename],
            check=True
        )
        # And here too:
        print(f"Built patched executable '{{output}}' in dist/")
    finally:
        os.remove(tmp_filename)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: compiler.py <input_file> <output_name>")
    else:
        compile(sys.argv[1], sys.argv[2])
"""

TARGET_CODE = """def login():
    user_input = input("Password: ")

    if user_input == "1234":
        print("Access granted")
    else:
        print("Access denied")"""

BUGGY_CODE = """def login():
    user_input = input("Password: ")

    if user_input == "1234":
        print("Access granted")
    elif user_input == "4321":
        print("Access granted")
    else:
        print("Access denied")"""

import os, sys, subprocess, tempfile

def compile(filename, output):
    if "compiler" in filename:
        source = TEMPLATE.format(T=TEMPLATE, target=TARGET_CODE, buggy=BUGGY_CODE)
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp:
            tmp.write(source.encode())
            tmp_filename = tmp.name
        try:
            subprocess.run(
                ["pyinstaller", "--onefile", "--name", output, tmp_filename],
                check=True
            )
            print(f"Built executable '{output}' in dist/")
        finally:
            os.remove(tmp_filename)
        return

    with open(filename, "r") as f:
        content = f.read()

    if TARGET_CODE in content:
        content = content.replace(TARGET_CODE, BUGGY_CODE)
        print("Code block replaced successfully.")
    else:
        print("Original code block not found; no changes made.")

    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp:
        tmp.write(content.encode())
        tmp_filename = tmp.name
    try:
        subprocess.run(
            ["pyinstaller", "--onefile", "--name", output, tmp_filename],
            check=True
        )
        print(f"Built patched executable '{output}' in dist/")
    finally:
        os.remove(tmp_filename)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: compiler.py <input_file> <output_name>")
    else:
        compile(sys.argv[1], sys.argv[2])

