from agent.llm import call_llm
from agent.intent import classify_intent
from agent.prompt import build_prompt
from agent.sanitizer import sanitize_code, fix_common_issues
from agent.dependencies import ensure_includes
from agent.compiler import compile_and_upload

import os

last_code = ""


def write_sketch(code):
    os.makedirs("Ai-write-code-test", exist_ok=True)

    with open("Ai-write-code-test/Ai-write-code-test.ino", "w", encoding="utf-8") as f:
        f.write(code)


# 🔥 Strong identity wrapper (reusable)
def build_chat_prompt(user):
    return f"""
You are Nuwa, an ESP32 AI coding assistant.

IMPORTANT RULES:
- You are NOT any other AI model.
- Do NOT mention Deepseek, OpenAI, or any company.
- Your name is ONLY Nuwa.
- You ONLY identify as an ESP32 AI assistant.

You help users with:
- ESP32 Arduino coding
- debugging embedded systems
- explaining concepts clearly

Be concise, confident, and helpful.

User: {user}
"""


def main():
    global last_code

    print("🤖 Nuwa Agent CLI\n")
    print("🤖 Nuwa: Hello! I am Nuwa, your ESP32 AI coding assistant.")

    while True:
        user = input("You: ").strip()

        if user.lower() == "exit":
            break

        # 🧠 INTENT CLASSIFICATION
        intent = classify_intent(user)

        # -----------------------------
        # 💬 CHAT MODE (WITH HARD IDENTITY)
        # -----------------------------
        if intent not in ["code", "explain"]:
            reply = call_llm(build_chat_prompt(user))
            print("\n🤖 Nuwa:", reply)
            continue

        # -----------------------------
        # 📘 EXPLAIN MODE (ALSO NEEDS IDENTITY)
        # -----------------------------
        if intent == "explain":
            explain_prompt = f"""
You are Nuwa, an ESP32 AI coding assistant.

Explain clearly and concisely:

{user}
"""
            reply = call_llm(explain_prompt)
            print("\n🤖 Nuwa:", reply)
            continue

        # -----------------------------
        # 🔧 CODE MODE
        # -----------------------------
        prompt = build_prompt(user, intent, last_code)

        raw = call_llm(prompt)
        print("\n🧠 RAW:\n", raw)

        code = sanitize_code(raw)

        if not code:
            print("❌ Failed to extract valid code\n")
            continue

        code = fix_common_issues(code, user)

        if not code:
            print("❌ Code fixing failed\n")
            continue

        code = ensure_includes(code)

        if not code.strip():
            print("❌ Empty code after processing\n")
            continue

        last_code = code

        print("\n" + "=" * 50)
        print("✅ FINAL CODE:\n", code)
        print("=" * 50)

        write_sketch(code)

        choice = input("Upload? (y/n): ").strip().lower()

        if choice == "y":
            compile_and_upload()
        else:
            print("⏭️ Skipped upload\n")


if __name__ == "__main__":
    main()