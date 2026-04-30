# 🤖 Nuwa Agent — ESP32 AI Coding Assistant

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![AI](https://img.shields.io/badge/AI-LLM%20Agent-purple)
![ESP32](https://img.shields.io/badge/ESP32-Arduino-green)
![CLI](https://img.shields.io/badge/Interface-CLI-black)

Nuwa is a **CLI-based AI assistant for ESP32 development** that generates, modifies, and validates Arduino code using a structured pipeline.

Instead of returning raw LLM output, Nuwa applies basic guardrails and validation to make generated embedded code more usable.

    generate → sanitize → validate → (optional) compile → upload

---

## 📑 Table of Contents

- 🚀 Why Nuwa  
- ⚙️ Features  
- 🏗️ Architecture  
- 📂 Project Structure  
- ⚡ Getting Started  
- 📦 Prerequisites  
- ⚙️ Configuration  
- ▶️ Run Nuwa  
- 💡 Example Usage  
- 🧠 Key Insight  
- ⚠️ Limitations  
- 🔮 Roadmap  

---

## 🚀 Why Nuwa

Most AI coding tools:

- generate code  
- leave validation to the user  

Nuwa takes a more structured approach:

- interprets user intent (chat / explain / code)  
- applies constraints to generated output  
- fixes common mistakes (where possible)  
- integrates with Arduino CLI for optional deployment  

**Goal:** Not perfection — but reducing obvious errors in embedded workflows.

---

## ⚙️ Features

### 🧠 Multi-Mode Interaction

- 💬 Chat mode (general help)  
- 📘 Explain mode (code explanation)  
- 🔧 Code mode (generate / modify / debug)  

### 🛡️ Guardrails & Validation

- Avoids invalid APIs (e.g., `analogWrite` on ESP32)  
- Encourages correct PWM usage:
  - `ledcSetup`
  - `ledcAttachPin`
  - `ledcWrite`  
- Flags common issues:
  - missing `setup()` / `loop()`  
  - incorrect includes  
- Attempts basic auto-correction  

### 🔧 Arduino CLI Integration

- Compile ESP32 sketches  
- Upload to board (optional confirmation)  
- Works with local development workflow  

### 📂 File-Based Workflow

- Read and modify `.ino` files  
- Use existing code as context  
- Supports simple debugging workflows  

---

## 🏗️ Architecture

    User Input
       ↓
    Intent Classification
       ↓
    Prompt Builder
       ↓
    LLM
       ↓
    Sanitize
       ↓
    Validate
       ↓
    Auto-fix (if needed)
       ↓
    Output / Compile / Upload

---

## 📂 Project Structure

    nuwa-agent/
    │
    ├── cli.py
    ├── agent/
    │   ├── llm.py
    │   ├── intent.py
    │   ├── prompt.py
    │   ├── sanitizer.py
    │   ├── validator.py
    │   ├── read_file.py
    │   ├── dependencies.py
    │   ├── compiler.py
    ├── config.py
    │
    └── README.md

---

## ⚡ Getting Started

```bash
git clone https://github.com/shikhar0708/nuwa-agent.git
cd nuwa-agent
```

---

## 📦 Prerequisites

### 🐍 Python

```bash
pip install requests
```

### 🧠 Ollama (or compatible LLM)

```bash
ollama pull deepseek-coder:6.7b
ollama run deepseek-coder:6.7b
```

### 🔧 Arduino CLI

Install: https://arduino.github.io/arduino-cli/

```bash
arduino-cli version
```

### 📡 ESP32 Core

```bash
arduino-cli core update-index
arduino-cli core install esp32:esp32@2.0.17
```

---

## ⚙️ Configuration

Edit:

```text
config.py
```

Example:

```python
PORT = "COM3"
FQBN = "esp32:esp32:esp32"
MODEL = "deepseek-coder:6.7b"
```

---

## ▶️ Run Nuwa

```bash
python cli.py
```

---

## 💡 Example Usage

```text
You: generate blink code
You: generate pwm breathing led
You: fix main.ino
You: read main.ino
You: explain this code
```

---

## 🧠 Key Insight

Raw LLM output is often unreliable in embedded contexts.

Adding constraints and validation significantly improves usability.

---

## ⚠️ Limitations

- Validation is rule-based (not exhaustive)  
- May still produce incorrect or incomplete code  
- Complex projects may require manual intervention  
- Hardware issues (wiring, power, etc.) are out of scope  

---

## 🔮 Roadmap

- Compile-error feedback loop  
- FastAPI interface  
- Improved validation rules  
- Cleaner include handling  
- Multi-file/project context  
- Web UI  

---

## 🧑‍💻 Author

**Vedic_Error**

---

## ⭐ Support

If you find this useful, consider giving it a star ⭐