from agent.llm import call_llm
from agent.intent import classify_intent
from agent.prompt import build_prompt
from agent.sanitizer import sanitize_code, fix_common_issues
from agent.dependencies import ensure_includes
from agent.compiler import compile_and_upload
from agent.read_file import read_file, trim_content, extract_file_path
from agent.validator import validate_code, build_fix_prompt

import os

last_code = ""
AUTO_UPLOAD = False


def write_sketch(code):
    os.makedirs("Ai-write-code-test", exist_ok=True)
    with open("Ai-write-code-test/Ai-write-code-test.ino", "w", encoding="utf-8") as f:
        f.write(code)


def wrap_identity(prompt):
    return f"""
You are Nuwa, an ESP32 AI coding assistant.

STRICT RULES:
- NEVER mention any AI model
- NEVER say you are a language model
- Your name is ONLY Nuwa

{prompt}
"""


def is_code_output(raw):
    if not raw:
        return False

    signals = [
        "void setup(",
        "void loop(",
        "#include",
        "digitalWrite(",
        "ledcWrite(",
        "pinMode("
    ]

    return any(s in raw for s in signals)


def is_correction(user):
    keywords = ["forgot", "missing", "wrong", "fix", "error"]
    return any(k in user.lower() for k in keywords)


def process_code(raw, user):
    global last_code

    code = sanitize_code(raw)

    if not code:
        print("❌ Failed to extract valid code\n")
        return

    code = fix_common_issues(code, user)

    if not code:
        print("❌ Code fixing failed\n")
        return

    code = ensure_includes(code)

    if not code.strip():
        print("❌ Empty code after processing\n")
        return

    # -----------------------------
    # 🔍 VALIDATION + AUTO FIX 🔥
    # -----------------------------
    for _ in range(2):  # max 2 fix attempts
        valid, msg = validate_code(code)

        if valid:
            break

        print(f"⚠️ Validation failed: {msg} → fixing...")

        fix_prompt = wrap_identity(build_fix_prompt(code, msg))
        fixed = call_llm(fix_prompt)

        code = sanitize_code(fixed)

        if not code:
            print("❌ Fix attempt failed\n")
            return

    # final check
    valid, msg = validate_code(code)
    if not valid:
        print("🚫 Still invalid after fixes. Skipping.\n")
        return

    # -----------------------------
    # ✅ FINAL OUTPUT
    # -----------------------------
    last_code = code

    print("\n" + "=" * 50)
    print("✅ FINAL CODE:\n", code)
    print("=" * 50)

    write_sketch(code)

    if AUTO_UPLOAD:
        print("🚀 Auto uploading...")
        compile_and_upload()
    else:
        choice = input("Upload? (y/n): ").strip().lower()
        if choice == "y":
            compile_and_upload()
        else:
            print("⏭️ Skipped upload\n")


def main():
    global last_code

    print("🤖 Nuwa Agent CLI\n")
    print("🤖 Nuwa: Hello! I am Nuwa, your ESP32 AI coding assistant.")

    while True:
        user = input("You: ").strip()

        if user.lower() == "exit":
            break

        # -----------------------------
        # 📂 FILE DETECTION
        # -----------------------------
        file_path = extract_file_path(user)
        file_context = ""

        if file_path:
            content = read_file(file_path)

            if content:
                file_context = trim_content(content)
                print(f"📂 Loaded file: {file_path}")

                # 🔥 SMART INTENT MAPPING
                if "read" in user.lower() or "explain" in user.lower():
                    intent = "explain"
                    user = "explain this code"
                elif "fix" in user.lower() or "bug" in user.lower():
                    intent = "debug"
                elif "edit" in user.lower() or "modify" in user.lower():
                    intent = "edit"
                else:
                    intent = "edit"
            else:
                print("⚠️ Could not load file")
                intent = classify_intent(user)
        else:
            intent = classify_intent(user)

        # -----------------------------
        # 🧠 CORRECTION MODE
        # -----------------------------
        if is_correction(user) and last_code:
            fix_prompt = wrap_identity(f"""
PREVIOUS CODE:
{last_code}

USER FEEDBACK:
{user}

FILE CONTEXT:
{file_context}

Fix the code and return ONLY updated code.
""")

            raw = call_llm(fix_prompt)
            print("\n🤖 Nuwa (fix):\n", raw)

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
            explain_prompt = wrap_identity(f"""
Explain clearly:

{user}

FILE CONTEXT:
{file_context}
""")

            raw = call_llm(explain_prompt)
            print("\n📘 Explanation:\n", raw)
            continue  # 🔥 IMPORTANT: don't process as code

        # -----------------------------
        # 🔧 CODE / EDIT / DEBUG MODE
        # -----------------------------
        prompt = wrap_identity(
            build_prompt(user, intent, last_code, file_context)
        )

        raw = call_llm(prompt)
        print("\n🧠 RAW:\n", raw)

        process_code(raw, user)


if __name__ == "__main__":
    main()