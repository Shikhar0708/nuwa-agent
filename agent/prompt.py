def build_prompt(user, intent, last_code="", file_context=""):
    u = user.lower()

    # -----------------------------
    # 🎯 RULE ENGINE (FIXED 🔥)
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
    # 📂 FILE CONTEXT
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
    # 🔧 GENERATE
    # -----------------------------
    if intent == "generate":
        return f"""
Generate Arduino ESP32 code.

TASK:
{user}

RULES:
{rules}

CONSTRAINTS:
- Use setup() and loop()
- Pin = 2
- Do NOT include unused libraries
- Output ONLY code
"""

    # -----------------------------
    # ✏️ EDIT
    # -----------------------------
    if intent == "edit":
        return f"""
Modify the following ESP32 Arduino code.

CODE:
{source_code}

REQUEST:
{user}

RULES:
{rules}

CONSTRAINTS:
- Do NOT rewrite from scratch
- Preserve structure unless necessary
- Do NOT include unused libraries
- Return ONLY updated code
"""

    # -----------------------------
    # 🐞 DEBUG
    # -----------------------------
    if intent == "debug":
        return f"""
Fix the following ESP32 Arduino code.

CODE:
{source_code}

ISSUE:
{user}

RULES:
{rules}

CONSTRAINTS:
- Fix ONLY what is necessary
- Do NOT rewrite entire code
- Do NOT include unused libraries
- Return ONLY corrected code
"""

    # -----------------------------
    # 📘 EXPLAIN
    # -----------------------------
    if intent == "explain":
        return f"""
Explain this ESP32 Arduino code clearly:

{source_code}
"""

    # -----------------------------
    # 🔥 FALLBACK
    # -----------------------------
    return f"""
Generate ESP32 Arduino code.

TASK:
{user}

RULES:
{rules}

CONSTRAINTS:
- Do NOT include unused libraries
- Return ONLY code
"""