import subprocess as sp
import re
from config import BOARD, PORT


# -----------------------------
# 📦 AUTO INSTALL LIBRARY
# -----------------------------
def install_library(lib):
    print(f"📦 Installing missing library: {lib}")
    sp.run(["arduino-cli", "lib", "install", lib])


# -----------------------------
# 🔨 COMPILE + UPLOAD
# -----------------------------
def compile_and_upload(return_error=False, retry_depth=0):
    if retry_depth > 2:
        err = "Max dependency retry reached"
        if return_error:
            return False, err
        print("🚫", err)
        return False

    # -----------------------------
    # 🔨 COMPILE
    # -----------------------------
    compile_cmd = [
        "arduino-cli",
        "compile",
        "--fqbn",
        BOARD,
        "Ai-write-code-test"
    ]

    result = sp.run(compile_cmd, capture_output=True, text=True)

    if result.returncode != 0:
        error = result.stderr

        print("❌ Compile Error:\n", error)

        # -----------------------------
        # 📦 AUTO INSTALL MISSING LIB
        # -----------------------------
        match = re.search(r"fatal error: (.+)\.h", error)
        if match:
            lib = match.group(1)
            install_library(lib)

            return compile_and_upload(
                return_error=return_error,
                retry_depth=retry_depth + 1
            )

        if return_error:
            return False, error

        return False

    # -----------------------------
    # 🚀 UPLOAD
    # -----------------------------
    upload_cmd = [
        "arduino-cli",
        "upload",
        "-p",
        PORT,
        "--fqbn",
        BOARD,
        "Ai-write-code-test"
    ]

    upload_result = sp.run(upload_cmd, capture_output=True, text=True)

    if upload_result.returncode != 0:
        error = upload_result.stderr

        print("❌ Upload Error:\n", error)

        if return_error:
            return False, error

        return False

    print("✅ Upload successful")

    if return_error:
        return True, ""

    return True