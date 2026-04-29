import subprocess as sp
import re
from config import BOARD, PORT

def install_library(lib):
    sp.run(["arduino-cli", "lib", "install", lib])


def compile_and_upload():
    result = sp.run(
        ["arduino-cli", "compile", "--fqbn", BOARD, "Ai-write-code-test"],
        capture_output=True, text=True
    )

    if result.returncode != 0:
        print(result.stderr)

        match = re.search(r"fatal error: (.+)\.h", result.stderr)
        if match:
            lib = match.group(1)
            install_library(lib)
            return compile_and_upload()

        return False

    sp.run([
        "arduino-cli", "upload",
        "-p", PORT,
        "--fqbn", BOARD,
        "Ai-write-code-test"
    ])

    return True