# 🤖 Nuwa Agent — ESP32 AI Coding Assistant

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![AI](https://img.shields.io/badge/AI-LLM%20Agent-purple)
![ESP32](https://img.shields.io/badge/ESP32-Arduino-green)
![CLI](https://img.shields.io/badge/Interface-CLI-black)

Nuwa is an **intent-driven AI agent** that transforms natural language into **working ESP32 Arduino code**, with built-in validation, guardrails, and one-command deployment.

> generate → sanitize → validate → compile → deploy

---

## 📑 Table of Contents

* [🚀 Why Nuwa](#-why-nuwa)
* [⚙️ Features](#️-features)
* [🏗️ Architecture](#️-architecture)
* [📂 Project Structure](#-project-structure)
* [⚡ Getting Started](#-getting-started)
* [📦 Prerequisites](#-prerequisites)
* [⚙️ Configuration](#️-configuration)
* [▶️ Run Nuwa](#️-run-nuwa)
* [💡 Example Usage](#-example-usage)
* [🧠 Key Insight](#-key-insight)
* [🔮 Roadmap](#-roadmap)

---

## 🚀 Why Nuwa

Most AI coding tools:

* generate code
* hope it works

Nuwa does more:

* understands intent (chat / explain / code)
* filters unsafe or incorrect outputs
* fixes common issues automatically
* deploys directly to hardware

---

## ⚙️ Features

### 🧠 Multi-Mode Agent

* 💬 Chat mode
* 📘 Explain mode
* 🔧 Code mode

---

### 🛡️ Guardrails & Validation

* Blocks incorrect APIs (`analogWrite`, ESP-IDF misuse)
* Enforces correct PWM usage (`ledcSetup`, `ledcAttachPin`, `ledcWrite`)
* Prevents malformed code
* Auto-fixes LLM mistakes

---

### 🔧 Arduino CLI Integration

* Compile ESP32 code
* Upload with confirmation
* Full hardware loop

---

### 🧩 Structured Prompting

* Rule-based constraints
* Identity-controlled agent (Nuwa)
* Context-aware editing

---

## 🏗️ Architecture

```text id="q3okcs"
User Input
   ↓
Intent Classification
   ↓
Prompt Builder
   ↓
LLM (Ollama)
   ↓
Sanitize + Fix
   ↓
Validate
   ↓
Compile + Upload
```

---

## 📂 Project Structure

```text id="rb1m4h"
.
├── cli.py
├── agent/
│   ├── llm.py
│   ├── intent.py
│   ├── prompt.py
│   ├── sanitizer.py
│   ├── dependencies.py
│   ├── compiler.py
│   ├── config.py
```

---

## ⚡ Getting Started

```bash id
git clone https://github.com/YOUR_USERNAME/nuwa-agent.git
cd nuwa-agent
```

---

## 📦 Prerequisites

### 🐍 Python

```bash id="w6d9d7"
pip install requests
```

---

### 🧠 Ollama

```bash id="1d9l9l"
ollama pull deepseek-coder:6.7b
ollama run deepseek-coder:6.7b
```

---

### 🔧 Arduino CLI

👉 https://arduino.github.io/arduino-cli/

```bash id="mqv3z3"
arduino-cli version
```

---

### 📡 ESP32 Core

```bash id="m5qyx0"
arduino-cli core update-index
arduino-cli core install esp32:esp32@2.0.17
```

---

## ⚙️ Configuration

Edit:

```text id="9m8l7f"
agent/config.py
```

### Required

```python id="0mcr6r"
PORT = "COM3"
FQBN = "esp32:esp32:esp32"
MODEL = "deepseek-coder:6.7b"
```

---

## ▶️ Run Nuwa

```bash id="o5i6d5"
python cli.py
```

---

## 💡 Example Usage

```text id="ib4f3g"
You: generate PWM code for LED
→ Nuwa generates + validates + deploys
```

---

```text id="y4x5js"
You: explain PWM
→ Nuwa explains clearly
```

---

## 🧠 Key Insight

> ❌ Raw LLM output is unreliable
> ✅ LLM + constraints + validation = usable system

---

## 🔮 Roadmap

* [ ] Memory
* [ ] Multi-agent roles
* [ ] Tool suggestions
* [ ] Web UI
* [ ] Self-debugging loop

---

## 🧑‍💻 Author

**Vedic_error**

---

## ⭐ Support

Give it a star ⭐ if you like it
