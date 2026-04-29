def build_prompt(user, intent, last_code):
    u = user.lower()

    if "blink" in u and "pwm" not in u:
        rules = """
- Use ONLY digitalWrite
- NO PWM
- No WiFi unless asked
"""
    elif "pwm" in u:
        rules = """
- Use ledcSetup, ledcWrite
- DO NOT use analogWrite
"""
    else:
        rules = "Use correct APIs"

    if intent == "generate":
        return f"""
You are Nuwa, an ESP32 AI coding assistant.
Generate Arduino ESP32 code.

Task: {user}
{rules}

Use setup() and loop().
Pin = 2.

Output only code.
"""

    if intent == "edit":
        return f"""
Modify this code:

{last_code}

Request: {user}

Return updated code only.
"""

    if intent == "debug":
        return f"""
Fix this code:

{last_code}

Issue: {user}

Return corrected code only.
"""

    if intent == "explain":
        return f"Explain this code:\n{last_code}"