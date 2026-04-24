# 👻 Ghost-AI-Assistant

[![Python](https://shields.io)](https://python.org)
[![Ollama](https://shields.io)](https://ollama.com)
[![License](https://shields.io)](https://opensource.org)
[![Telegram](https://shields.io)](https://t.me)

**Ghost-AI-Assistant** is a high-tech stealth bridge between your screen and the power of Large Language Models. Designed for environments with strict monitoring, it allows you to capture, recognize, and solve on-screen tasks without leaving a digital footprint.

---

## 🔥 Key Features

- 🛡️ **Anti-Proctoring Protection**: Uses Windows `DisplayAffinity` API to exclude the assistant window from screen captures (OES, OBS, Discord). On video recordings, the window appears as a **solid black box**.
- 📱 **Telegram Synchronization**: Real-time answer duplication directly to your smartphone.
- 🌫️ **Ghost Interface**: Ultra-transparent, minimalist UI that stays on top but doesn't interfere with your workflow.
- ⚡ **Asynchronous Engine**: Powered by Python threads—the UI remains responsive and draggable even while the AI is "thinking."
- 🖱️ **Context-Aware OCR**: Smart screen capture localized around your mouse cursor.

---

## 🛠️ Technical Stack

- **Brain**: [Ollama](https://ollama.com) (running `minimax-m2.7:cloud`)
- **Vision**: [Tesseract OCR](https://github.com)
- **UI**: Tkinter (Ghost Layer)
- **Communication**: Telegram Bot API

---

## 🚀 Quick Start

### 1. Prerequisites
- Install **Python 3.10+**.
- Install **Ollama** and pull the model:
  ```bash
  ollama run minimax-m2.7:cloud
  ```
- Install **Tesseract OCR**. *Make sure to include Russian and English language data during installation.*

### 2. Installation
```bash
git clone https://github.com/Nodir270
cd Ghost-AI-Assistant
pip install -r requirements.txt
```

### 3. Configuration
Open `main.py` and set your credentials:
- `TELEGRAM_TOKEN`: Your bot token from [@BotFather](https://t.me).
- `TELEGRAM_CHAT_ID`: Your chat ID from [@userinfobot](https://t.me).
- Open main.py and fill in the TELEGRAM_TOKEN and TELEGRAM_CHAT_ID variables before running.

### 4. Running
Launch the script with **Administrator privileges** (required for global hotkeys):
```bash
python main.py
```

---

## 🎮 Usage
1. Hover your mouse over the question.
2. Press `Ctrl + Alt + S`.
3. Read the answer in the transparent ghost window or on your phone.
4. Use the **Mouse Wheel** to scroll through long explanations.

---

## ⚠️ Disclaimer
This project is for educational purposes only. The author is not responsible for any misuse or violations of academic integrity policies.

---
*Created with ❤️ for stealthy efficiency.*
