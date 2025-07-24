import subprocess
import sys


def compile(filename, output_name):
    try:
        subprocess.run([
            "pyinstaller",
            "--onefile",
            "--name", output_name,
            filename
        ], check=True)
        print("Executable created in the 'dist' folder.")
    except subprocess.CalledProcessError as e:
        print("Error during compilation:", e)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: compiler.py <filename> <output_exe>")
    else:
        compile(sys.argv[1], sys.argv[2])

