from agent.llm import call_llm
from agent.intent import classify_intent
from agent.prompt import build_prompt
from agent.sanitizer import sanitize_code, fix_common_issues
from agent.dependencies import ensure_includes
from agent.compiler import compile_and_upload
from agent.read_file import read_file, trim_content, extract_file_path
from agent.validator import validate_code, build_fix_prompt
from agent.banner import show_banner

import os
import re

last_code = ""
AUTO_UPLOAD = False


# -----------------------------
# 📁 WRITE FILE
# -----------------------------
def write_sketch(code):
    os.makedirs("Ai-write-code-test", exist_ok=True)
    with open("Ai-write-code-test/Ai-write-code-test.ino", "w", encoding="utf-8") as f:
        f.write(code)


# -----------------------------
# 🧠 IDENTITY WRAPPER
# -----------------------------
def wrap_identity(prompt):
    return f"""
You are Nuwa, an ESP32 AI coding assistant.

STRICT RULES:
- NEVER mention any AI model
- NEVER say you are a language model
- ALWAYS generate Arduino C++ when writing code
- NEVER generate Python or MicroPython
- Your name is ONLY Nuwa

{prompt}
"""


# -----------------------------
# 🔍 STRICT CODE DETECTION
# -----------------------------
def is_code_output(raw):
    return raw and "void setup(" in raw and "void loop(" in raw


# -----------------------------
# 🔁 CORRECTION DETECTION
# -----------------------------
def is_correction(user):
    return any(k in user.lower() for k in ["forgot", "missing", "wrong", "fix", "error"])


# -----------------------------
# 🧠 FORCE CODE INTENT (IMPORTANT)
# -----------------------------
def force_code_intent(user, intent):
    keywords = [
        "esp32", "oled", "ssd1306", "arduino",
        "display", "led", "sensor", "i2c"
    ]

    if any(k in user.lower() for k in keywords):
        return "code"

    return intent


# -----------------------------
# ⚙️ RULE-BASED ERROR FIX
# -----------------------------
def apply_error_fix(code, error):
    if "drawLine" in error:
        code = re.sub(r'drawLine\s*\((.*?)\)', lambda m: f"drawLine({m.group(1)}, WHITE)", code)

    if "drawPixel" in error:
        code = re.sub(r'drawPixel\s*\((.*?)\)', lambda m: f"drawPixel({m.group(1)}, WHITE)", code)

    return code


# -----------------------------
# ⚙️ CORE PROCESSOR
# -----------------------------
def process_code(raw, user):
    global last_code

    code = sanitize_code(raw)

    # -----------------------------
    # 🚨 WRONG LANGUAGE DETECTION
    # -----------------------------
    if "from machine import" in code or "SSD1306_I2C" in code:
        print("⚠️ Wrong language detected → regenerating...")

        prompt = wrap_identity(f"""
Generate Arduino ESP32 code.

TASK:
{user}

STRICT:
- Use Arduino C++ only
- Use Adafruit_SSD1306
- No Python

Return ONLY code.
""")

        code = sanitize_code(call_llm(prompt))

    if not code:
        print("❌ Failed to extract valid code\n")
        return

    # -----------------------------
    # 🔍 VALIDATE FIRST
    # -----------------------------
    valid, msg = validate_code(code)

    if not valid:
        print(f"⚠️ Initial validation: {msg}")
        code = fix_common_issues(code, user)

    code = ensure_includes(code)

    # Re-validate
    valid, msg = validate_code(code)

    if not valid:
        print("⚠️ Rule fix insufficient → LLM repair")

        fix_prompt = wrap_identity(build_fix_prompt(code, msg))
        code = sanitize_code(call_llm(fix_prompt))
        code = fix_common_issues(code, user)
        code = ensure_includes(code)

    # Final validation
    valid, msg = validate_code(code)
    if not valid:
        print("🚫 Still invalid after repair. Skipping.\n")
        return

    # -----------------------------
    # ✅ FINAL OUTPUT
    # -----------------------------
    last_code = code

    print("\n" + "=" * 50)
    print("✅ FINAL CODE:\n", code)
    print("=" * 50)

    write_sketch(code)

    # -----------------------------
    # 🔨 COMPILE LOOP
    # -----------------------------
    for attempt in range(2):
        success, error = compile_and_upload(return_error=True)

        if success:
            break

        print(f"⚠️ Compile failed (attempt {attempt+1})")

        code = apply_error_fix(code, error)

        if attempt == 1:
            fix_prompt = wrap_identity(f"""
The code failed to compile.

ERROR:
{error}

Fix ONLY the issue.
Do NOT rewrite entire code.

Return ONLY corrected code.
""")

            code = sanitize_code(call_llm(fix_prompt))
            code = fix_common_issues(code, user)
            code = ensure_includes(code)

        write_sketch(code)

    # -----------------------------
    # 🚀 UPLOAD CONTROL
    # -----------------------------
    if AUTO_UPLOAD:
        print("🚀 Auto uploaded successfully\n")
    else:
        choice = input("Upload again? (y/n): ").strip().lower()
        if choice == "y":
            compile_and_upload()
        else:
            print("⏭️ Done\n")


# -----------------------------
# 🚀 MAIN LOOP
# -----------------------------
def main():
    global last_code

    show_banner()
    print("🤖 Nuwa: Hello! I am Nuwa, your ESP32 AI coding assistant.")

    while True:
        user = input("You: ").strip()

        if user.lower() == "exit":
            break

        file_path = extract_file_path(user)
        file_context = ""

        if file_path:
            content = read_file(file_path)

            if content:
                file_context = trim_content(content)
                print(f"📂 Loaded file: {file_path}")

                if "read" in user.lower() or "explain" in user.lower():
                    intent = "explain"
                    user = "explain this code"
                elif "fix" in user.lower():
                    intent = "debug"
                else:
                    intent = "edit"
            else:
                intent = classify_intent(user)
        else:
            intent = classify_intent(user)

        # 🔥 FORCE CORRECT INTENT
        intent = force_code_intent(user, intent)

        # -----------------------------
        # 🧠 CORRECTION MODE
        # -----------------------------
        if is_correction(user) and last_code:
            fix_prompt = wrap_identity(f"""
PREVIOUS CODE:
{last_code}

USER FEEDBACK:
{user}

Fix ONLY the issue.
Return ONLY updated code.
""")

            raw = call_llm(fix_prompt)

            if is_code_output(raw):
                process_code(raw, user)
            else:
                print("❌ Failed to generate corrected code\n")

            continue

        # -----------------------------
        # 💬 CHAT MODE
        # -----------------------------
        if intent not in ["code", "explain", "edit", "debug"]:
            raw = call_llm(wrap_identity(user))
            print("\n🤖 Nuwa:", raw)

            if is_code_output(raw):
                print("\n⚡ Code detected → processing...")
                process_code(raw, user)

            continue

        # -----------------------------
        # 📘 EXPLAIN MODE
        # -----------------------------
        if intent == "explain":
            if file_context:
                prompt = wrap_identity(f"""
        Explain this ESP32 Arduino code clearly.

        CODE:
        {file_context}
        """)
            else:
                prompt = wrap_identity(f"""
        Explain this ESP32 Arduino code clearly.

        CODE:
        {last_code}
        """)

            raw = call_llm(prompt)

            print("\n📘 Explanation:\n", raw)
            continue

        # -----------------------------
        # 🔧 CODE MODE
        # -----------------------------
        prompt = wrap_identity(
            build_prompt(user, intent, last_code, file_context)
        )

        raw = call_llm(prompt)
        print("\n🧠 RAW:\n", raw)

        process_code(raw, user)


if __name__ == "__main__":
    main()