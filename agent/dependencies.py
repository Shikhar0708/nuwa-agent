def ensure_includes(code):
    includes = []

    if "WiFi." in code and "#include <WiFi.h>" not in code:
        includes.append("#include <WiFi.h>")

    if "#include <Arduino.h>" not in code:
        includes.append("#include <Arduino.h>")

    if includes:
        code = "\n".join(includes) + "\n\n" + code

    return code