import re


# -----------------------------
# 📦 EXTRACT CODE BLOCK
# -----------------------------
def extract_code(raw):
    matches = re.findall(r"```(?:\w+)?\s*(.*?)```", raw, re.DOTALL)
    if matches:
        return max(matches, key=len)
    return raw


# -----------------------------
# 🧹 REMOVE LLM NOISE
# -----------------------------
def remove_llm_noise(code):
    # Remove ALL angle-bracket garbage EXCEPT valid includes
    code = re.sub(r'<(?![A-Za-z_]+\.h)[^>]*>', '', code)

    # Remove weird unicode junk
    code = re.sub(r'[^\x00-\x7F]+', '', code)

    noise = [
        "Sure,", "Here is", "Here's",
        "I can help", "This code"
    ]

    for n in noise:
        code = code.replace(n, "")

    return code


# -----------------------------
# 🔧 STRIP BEFORE REAL CODE
# -----------------------------
def strip_before_code(code):
    match = re.search(r"(#include.*)", code, re.DOTALL)
    if match:
        return match.group(1)

    match = re.search(r"(void setup\s*\(.*)", code, re.DOTALL)
    if match:
        return match.group(1)

    return code


# -----------------------------
# 🧼 SANITIZE
# -----------------------------
def sanitize_code(raw):
    code = extract_code(raw)
    code = remove_llm_noise(code)
    code = strip_before_code(code)
    return code.strip()


# -----------------------------
# 🔧 FIX COMMON ISSUES
# -----------------------------
def fix_common_issues(code, user):
    u = user.lower()

    # -----------------------------
    # ✅ FIX drawPixel
    # -----------------------------
    def fix_drawpixel(match):
        args = match.group(1)
        if args.count(",") == 1:
            return f"drawPixel({args}, WHITE)"
        return f"drawPixel({args})"

    code = re.sub(r'drawPixel\s*\((.*?)\)', fix_drawpixel, code)

    # -----------------------------
    # ✅ FIX drawLine (NEW 🔥)
    # -----------------------------
    def fix_drawline(match):
        args = match.group(1)
        if args.count(",") == 3:
            return f"drawLine({args}, WHITE)"
        return f"drawLine({args})"

    code = re.sub(r'drawLine\s*\((.*?)\)', fix_drawline, code)

    # -----------------------------
    # ✅ REMOVE UNUSED WIFI
    # -----------------------------
    if "wifi" not in u:
        code = re.sub(r'#include\s*<WiFi\.h>\n?', '', code)

    # -----------------------------
    # ✅ FORCE CORRECT SSD1306 INIT
    # -----------------------------
    code = re.sub(
        r'Adafruit_SSD1306\s+display\s*\([^)]*\)',
        'Adafruit_SSD1306 display(128, 64, &Wire, -1)',
        code
    )

    code = re.sub(
        r'display\.begin\s*\([^)]*\)',
        'display.begin(SSD1306_SWITCHCAPVCC, 0x3C)',
        code
    )

    # -----------------------------
    # ✅ FIX TRIG
    # -----------------------------
    code = re.sub(r'cos\(([^)]+)\)', r'cos(radians(\1))', code)
    code = re.sub(r'sin\(([^)]+)\)', r'sin(radians(\1))', code)

    # -----------------------------
    # 🚑 HARD INCLUDE ENFORCEMENT (BEST FIX)
    # -----------------------------
    required = """#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

"""

    # Remove all existing includes (prevents corruption)
    code = re.sub(r'#include.*\n', '', code)

    # Add clean includes at top
    code = required + code

    return code