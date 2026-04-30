from agent.llm import call_llm
from agent.intent import classify_intent
from agent.prompt import build_prompt
from agent.sanitizer import sanitize_code, fix_common_issues
from agent.dependencies import ensure_includes
from agent.compiler import compile_and_upload

import os

last_code = ""
AUTO_UPLOAD = False  # 🔥 set True for auto deployment


def write_sketch(code):
    os.makedirs("Ai-write-code-test", exist_ok=True)

    with open("Ai-write-code-test/Ai-write-code-test.ino", "w", encoding="utf-8") as f:
        f.write(code)


# 🔥 Strong identity wrapper (HARD)
def build_chat_prompt(user):
    return f"""
You are Nuwa, an ESP32 AI coding assistant.

STRICT RULES:
- You are NOT any other AI model.
- NEVER mention Deepseek, OpenAI, or training data.
- NEVER say you are a language model.
- Your name is ONLY Nuwa.

BEHAVIOR:
- Be technical and concise
- If user corrects you → acknowledge and fix
- Do NOT deflect or give generic AI disclaimers

User: {user}
"""


# 🧠 Detect if LLM output is code
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


# 🧠 Detect correction intent
def is_correction(user):
    keywords = ["forgot", "missing", "wrong", "fix", "error"]
    return any(k in user.lower() for k in keywords)


# 🔥 Unified pipeline
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

    last_code = code

    print("\n" + "=" * 50)
    print("✅ FINAL CODE:\n", code)
    print("=" * 50)

    write_sketch(code)

    # 🚀 Deploy
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

        intent = classify_intent(user)

        # -----------------------------
        # 🧠 CORRECTION MODE (NEW 🔥)
        # -----------------------------
        if is_correction(user) and last_code:
            fix_prompt = f"""
You are Nuwa, an ESP32 AI coding assistant.

STRICT RULES:
- Never mention any AI model
- Only output corrected Arduino ESP32 code

PREVIOUS CODE:
{last_code}

USER FEEDBACK:
{user}

TASK:
Fix the code based on feedback and return ONLY updated code.
"""
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
        if intent not in ["code", "explain"]:
            raw = call_llm(build_chat_prompt(user))
            print("\n🤖 Nuwa:", raw)

            # 🔥 GLOBAL CODE DETECTION
            if is_code_output(raw):
                print("\n⚡ Code detected → processing...")
                process_code(raw, user)

            continue

        # -----------------------------
        # 📘 EXPLAIN MODE
        # -----------------------------
        if intent == "explain":
            explain_prompt = f"""
You are Nuwa, an ESP32 AI coding assistant.

Explain clearly:

{user}
"""
            raw = call_llm(explain_prompt)
            print("\n🤖 Nuwa:", raw)

            if is_code_output(raw):
                print("\n⚡ Code detected → processing...")
                process_code(raw, user)

            continue

        # -----------------------------
        # 🔧 CODE MODE
        # -----------------------------
        prompt = build_prompt(user, intent, last_code)

        raw = call_llm(prompt)
        print("\n🧠 RAW:\n", raw)

        process_code(raw, user)


if __name__ == "__main__":
    main()