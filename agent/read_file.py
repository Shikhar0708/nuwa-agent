# agent/read_file.py

import os

MAX_CHARS = 3000


def read_file(path):
    if not os.path.exists(path):
        print(f"❌ File not found: {path}")
        return None

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # 🚫 Block binary-like content
        if "\x00" in content:
            print("❌ Binary file detected. Skipping.")
            return None

        return content

    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return None


def trim_content(content, max_chars=MAX_CHARS):
    if not content:
        return ""

    if len(content) > max_chars:
        print(f"⚠️ File too large, trimming to {max_chars} chars")
        return content[:max_chars]

    return content


def extract_file_path(user_input):
    user_input = user_input.strip()

    # patterns like file: main.ino
    patterns = ["file:", "file->", "file-->"]

    for p in patterns:
        if p in user_input:
            return user_input.split(p)[-1].strip()

    # 🔥 NEW: detect direct .ino usage
    words = user_input.split()
    for w in words:
        if w.endswith(".ino"):
            return w

    return None