# agent/validator.py

def validate_code(code):
    """
    Returns:
        (True, "OK") if valid
        (False, "reason") if invalid
    """

    if not code or not code.strip():
        return False, "Empty code"

    # -----------------------------
    # ❌ FORBIDDEN (ESP-IDF, etc.)
    # -----------------------------
    forbidden = [
        "gpio_set_level",
        "gpio_set_direction",
        "esp_timer",
        "GPIO_NUM",
        "ledc_channel_config_t",
        "driver/gpio"
    ]

    for f in forbidden:
        if f in code:
            return False, f"Forbidden ESP-IDF API detected: {f}"

    # -----------------------------
    # ❌ WRONG API USAGE
    # -----------------------------
    if "analogWrite" in code:
        return False, "analogWrite is not valid for ESP32 (use ledc API)"

    # -----------------------------
    # ⚠️ PWM CONSISTENCY CHECK
    # -----------------------------
    if "ledcWrite" in code:
        if "ledcSetup" not in code:
            return False, "Missing ledcSetup for PWM"
        if "ledcAttachPin" not in code:
            return False, "Missing ledcAttachPin for PWM"

    # -----------------------------
    # ⚠️ BASIC STRUCTURE CHECK
    # -----------------------------
    if "void setup(" not in code or "void loop(" not in code:
        return False, "Missing setup() or loop()"
    
    # ⚠️ unnecessary WiFi usage
    if "#include <WiFi.h>" in code:
        if "WiFi.begin" not in code:
            return False, "WiFi.h included but not used"

    return True, "OK"


# -----------------------------
# 🔧 AUTO FIX PROMPT BUILDER
# -----------------------------
def build_fix_prompt(code, error):
    return f"""
Fix this ESP32 Arduino code.

ERROR:
{error}

RULES:
- Use Arduino ESP32 API only
- DO NOT use ESP-IDF
- Ensure correct PWM usage (ledcSetup, ledcAttachPin, ledcWrite)
- Keep structure minimal and correct
- Return ONLY corrected code

CODE:
{code}
"""