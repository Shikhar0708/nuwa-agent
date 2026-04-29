import re

def sanitize_code(raw):
    match = re.search(r"```(?:cpp)?\s*(.*?)```", raw, re.DOTALL)
    code = match.group(1) if match else raw

    return code.encode("ascii", "ignore").decode().strip()


def fix_common_issues(code, user):
    if "analogWrite" in code:
        code = code.replace("analogWrite", "ledcWrite")

    if "blink" in user.lower():
        code = re.sub(r".*ledc.*\n", "", code)

    return code