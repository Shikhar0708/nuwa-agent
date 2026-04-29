import requests, time
from config import URL, MODEL

def call_llm(prompt, retries=3):
    for i in range(retries):
        try:
            res = requests.post(URL, json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.2}
            }, timeout=300)

            data = res.json()

            if "response" in data and data["response"].strip():
                return data["response"]

        except Exception as e:
            print(f"⚠️ LLM Error {i+1}:", e)
            time.sleep(2 * (i + 1))

    return ""