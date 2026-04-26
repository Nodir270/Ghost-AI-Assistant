# 👻 Ghost-AI-Assistant V2

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Ollama](https://img.shields.io/badge/Ollama-minimax--m2.7-orange.svg)](https://ollama.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Ghost-AI-Assistant** is a high-tech stealth bridge between your screen and the power of local Large Language Models. Version 2 has been completely redesigned: it is now an invisible overlay that follows your cursor and leaves no digital footprint.

---

## 🆕 What's New in V2 (Changelog)
- **Invisible Ghost UI**: All window borders and headers have been removed. Only the AI response text remains visible.
- **Mouse Tracker**: The window now automatically follows your mouse cursor for better context.
- **Single-Key Hotkeys**: Migrated to single-key inputs (Scan Code 41 / Tilde and Right Ctrl) for faster operation.
- **Proxy-Bypass Logic**: Implemented direct connection logic for Ollama and Telegram to bypass system proxies.
- **Enhanced OCR**: Improved image pre-processing (grayscale and contrast) before recognition.

---

## 🔥 Key Features

- 🛡️ **Anti-Proctoring Protection**: Uses Windows `DisplayAffinity` API to exclude the assistant window from screen captures (OBS, Discord, Proctoring software). The window appears as a **solid black box** on recordings.
- 📱 **Telegram Synchronization**: Real-time answer duplication directly to your smartphone via Telegram Bot.
- 🌫️ **Ghost Interface**: Ultra-minimalist, semi-transparent UI with no buttons or frames.
- ⚡ **Asynchronous Engine**: Powered by Python threads—the UI remains responsive while the AI is "thinking."

---

## 🚀 Quick Start

### 1. Prerequisites
- Install **Python 3.10+**.
- Install **Ollama** and pull the model:
  ```bash
  ollama run minimax-m2.7:cloud
Install Tesseract OCR. Ensure you include Russian and English language data during installation.

2. Installation
Bash
git clone [https://github.com/Nodir270/Ghost-AI-Assistant](https://github.com/Nodir270/Ghost-AI-Assistant)
cd Ghost-AI-Assistant
pip install -r requirements.txt
3. Configuration
Open main.py and set your credentials:

TELEGRAM_TOKEN: Your bot token from @BotFather.

TELEGRAM_CHAT_ID: Your chat ID from @userinfobot.

4. Running
Launch the script with Administrator privileges (required for global hotkeys):

Bash
python main.py
🎮 Usage
Key ~ (Tilde): Capture the screen area under the window and solve the task.

Right Ctrl: Toggle mode (Follow Mouse / Manual Placement).

Mouse Wheel: Scroll through long AI responses.


⚠️ Disclaimer
This project is for educational purposes only. The author is not responsible for any misuse or violations of academic integrity policies.

Created with ❤️ for stealthy efficiency.
