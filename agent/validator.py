import re

def validate_code(code):
    """
    Returns:
        (True, "OK") if valid
        (False, "reason") if invalid
    """

    if not code or not code.strip():
        return False, "Empty code"

    # -----------------------------
    # ❌ BROKEN INCLUDE (CRITICAL 🔥)
    # -----------------------------
    if re.search(r'#include\s*$', code, re.MULTILINE):
        return False, "Broken #include detected"

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

    # -----------------------------
    # ⚠️ WiFi misuse
    # -----------------------------
    if "#include <WiFi.h>" in code and "WiFi.begin" not in code:
        return False, "WiFi.h included but not used"

    # -----------------------------
    # ⚠️ OLED API CHECKS (NEW 🔥)
    # -----------------------------

    # drawPixel must have 3 args
    pixel_calls = re.findall(r'drawPixel\s*\((.*?)\)', code)
    for call in pixel_calls:
        if call.count(",") < 2:
            return False, "drawPixel missing color argument"

    # drawLine must have 5 args
    line_calls = re.findall(r'drawLine\s*\((.*?)\)', code)
    for call in line_calls:
        if call.count(",") < 4:
            return False, "drawLine missing color argument"

    # SSD1306 constructor sanity
    if "Adafruit_SSD1306 display(" in code:
        if "&Wire" not in code:
            return False, "Invalid SSD1306 constructor"

    return True, "OK"


# -----------------------------
# 🔧 AUTO FIX PROMPT BUILDER
# -----------------------------
def build_fix_prompt(code, error):
    return f"""
Fix this ESP32 Arduino code.

ERROR:
{error}

STRICT RULES:
- Return ONLY Arduino C++ code
- NO explanation
- DO NOT rewrite entire code
- Fix ONLY the issue

Ensure:
- Valid includes
- Correct OLED usage
- Code compiles

CODE:
{code}
"""