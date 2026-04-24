import pyautogui
import pytesseract
from PIL import Image, ImageOps
import requests
import os
import keyboard
import ctypes
import time
import tkinter as tk
from threading import Thread
TELEGRAM_TOKEN = "your telegram bot's API" 
TELEGRAM_CHAT_ID = "your telegram id" 
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'
class GhostApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.2)
        self.root.geometry("350x180+20+20") 
        self.root.config(bg="black")

        self.offset_x = 0
        self.offset_y = 0
        
        self.root.update()
        hwnd_tk = ctypes.windll.user32.GetParent(self.root.winfo_id())
        ctypes.windll.user32.SetWindowDisplayAffinity(hwnd_tk, 0x11)
        
        self.text_area = tk.Text(
            self.root, fg="gray", bg="black", font=("Arial", 9),
            wrap="word", borderwidth=0, highlightthickness=0,
            selectbackground="black", inactiveselectbackground="black",
            selectforeground="gray", cursor="arrow"
        )
        self.text_area.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.insert_text("System Active\nCtrl+Alt+S для работы")
        
        self.text_area.bind("<MouseWheel>", self.on_mousewheel)
        self.text_area.bind("<Button-1>", self.start_move)
        self.text_area.bind("<B1-Motion>", self.move_window)
        
        self.check_hotkey()

    def on_mousewheel(self, event):
        self.text_area.yview_scroll(int(-1*(event.delta/120)), "units")
        return "break"

    def start_move(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def move_window(self, event):
        new_x = event.x_root - self.offset_x
        new_y = event.y_root - self.offset_y
        self.root.geometry(f"+{new_x}+{new_y}")

    def insert_text(self, text):
        self.text_area.config(state="normal")
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, text)
        self.text_area.config(state="disabled")
        self.root.update()

    def send_telegram(self, text):
        # Принудительно отключаем прокси для Telegram
        session = requests.Session()
        session.proxies = {"http": None, "https": None}
        session.trust_env = False
        
        url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
        try:
            r = session.post(url, json=payload, timeout=10)
            if r.status_code != 200:
                print(f"[TG ERROR]: {r.text}")
        except Exception as e:
            print(f"[TG CONN ERR]: {e}")

    def background_solve(self, text):
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "minimax-m2.7:cloud",
            "prompt": f"Реши кратко тест: {text}",
            "stream": False
        }

        proxies = {"http": None, "https": None}
        
        try:
            response = requests.post(url, json=payload, timeout=90, proxies=proxies)
            if response.status_code == 200:
                ans = response.json().get('response', '').strip()
                
                if ans:
                    self.root.after(0, self.insert_text, f"ANS:\n{ans}")
                    self.send_telegram(f"✅ ОТВЕТ:\n{ans}")
                else:
                    self.root.after(0, self.insert_text, "Нейросеть выдала пустой ответ")
            else:
                self.root.after(0, self.insert_text, f"API Error: {response.status_code}")
        except Exception as e:
            self.root.after(0, self.insert_text, f"Conn Err: {str(e)[:20]}")

    def check_hotkey(self):
        if keyboard.is_pressed('ctrl+alt+s'):
            try:
                x, y = pyautogui.position()
                img = pyautogui.screenshot(region=(int(x-500), int(y-250), 1000, 500))
                img = ImageOps.grayscale(img)
                img = ImageOps.autocontrast(img)
                raw_text = pytesseract.image_to_string(img, lang='rus+eng').strip()
                
                if len(raw_text) > 10:
                    self.insert_text("Thinking...")
                    # Запуск в фоновом потоке, чтобы окно не зависало
                    Thread(target=self.background_solve, args=(raw_text,), daemon=True).start()
                else:
                    self.insert_text("Text not found")
                
                self.root.after(4000, self.check_hotkey)
                return
            except:
                pass
        
        self.root.after(100, self.check_hotkey)

if __name__ == "__main__":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    app = GhostApp()
    app.root.mainloop()
