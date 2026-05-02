def build_prompt(user, intent, last_code="", file_context=""):
    u = user.lower()

    # -----------------------------
    # 🎯 RULE ENGINE
    # -----------------------------
    if "blink" in u and "pwm" not in u:
        rules = """
- Use ONLY digitalWrite
- NO PWM
- DO NOT use WiFi
"""
    elif "pwm" in u:
        rules = """
- Use ledcSetup, ledcAttachPin, ledcWrite
- DO NOT use analogWrite
- DO NOT include WiFi unless explicitly asked
"""
    elif "wifi" in u:
        rules = """
- Use ESP32 WiFi APIs correctly
- Include WiFi.h ONLY if required
"""
    else:
        rules = """
- Use correct ESP32 Arduino APIs
- DO NOT include WiFi.h unless explicitly required
"""

    # -----------------------------
    # 📂 CONTEXT
    # -----------------------------
    source_code = file_context if file_context else last_code

    context_block = ""
    if file_context:
        context_block = f"""
FILE CONTEXT:
{file_context}

IMPORTANT:
- This is the PRIMARY source of truth
- Modify THIS code, not something new
"""

    # -----------------------------
    # 🚨 STRICT OUTPUT CONTRACT
    # -----------------------------
    output_contract = """
STRICT OUTPUT FORMAT (MANDATORY):
- Output MUST be ONLY valid Arduino C++ code
- NO explanations
- NO markdown
- NO text before or after code
- NO phrases like "Here is", "Sure", etc.
- NO special tokens like <| |>

FAIL IF:
- Any text exists outside code
- Missing setup() or loop()
- Unused libraries included
"""

    # -----------------------------
    # 🧠 TASK BLOCK
    # -----------------------------
    if intent == "generate":
        task_block = f"""
TASK:
{user}

- Create COMPLETE working code
- Include required libraries
"""

    elif intent == "edit":
        task_block = f"""
TASK:
Modify existing code

REQUEST:
{user}

CODE:
{source_code}

- Preserve structure
- Do NOT rewrite unless necessary
"""

    elif intent == "debug":
        task_block = f"""
TASK:
Fix the code

ISSUE:
{user}

CODE:
{source_code}

- Fix minimal required parts
- Do NOT rewrite entire code
"""

    elif intent == "explain":
        return f"""
Explain this ESP32 Arduino code clearly:

{source_code}
"""

    else:
        task_block = f"""
TASK:
{user}
"""

    # -----------------------------
    # 🧩 FINAL PROMPT
    # -----------------------------
    return f"""
You are an ESP32 Arduino expert.

{output_contract}

RULES:
{rules}

CONSTRAINTS:
- Use setup() and loop()
- Default pin = 2 unless specified
- Use only necessary libraries
- Ensure code compiles

{context_block}

{task_block}

FINAL INSTRUCTION:
Return ONLY raw Arduino C++ code.
"""