import tkinter as tk
import ctypes
import threading
import requests
import pyautogui
import pytesseract
from PIL import Image, ImageOps
import keyboard

TELEGRAM_TOKEN = "YOUR_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_ID"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "minimax-m2.7:cloud"

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class GhostAssistant:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ghost-AI")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.5)
        self.root.config(bg='black')
        self.root.geometry("350x200")

        self.text_area = tk.Text(
            self.root, wrap=tk.WORD, bg='black', fg='white', 
            font=("Consolas", 10), bd=0, highlightthickness=0,
            selectbackground='black', selectforeground='white',
            inactiveselectbackground='black', exportselection=False
        )
        self.text_area.pack(expand=True, fill='both', padx=5, pady=5)
        self.text_area.config(state=tk.DISABLED)

        self.is_following = True
        
        self.grip = tk.Frame(self.root, bg='black', cursor="bottom_right_corner")
        self.grip.place(relx=1.0, rely=1.0, anchor="se", width=15, height=15)
        self.grip.bind("<B1-Motion>", self.resize_window)
        
        self.activate_stealth()
        self.setup_hotkeys()
        self.update_position()
        
        self.text_area.bind("<Button-1>", self.start_move)
        self.text_area.bind("<B1-Motion>", self.do_move)

        self.root.mainloop()

    def activate_stealth(self):
        self.root.update()
        try:
            hwnd = self.root.winfo_id()
            while ctypes.windll.user32.GetParent(hwnd):
                hwnd = ctypes.windll.user32.GetParent(hwnd)
            ctypes.windll.user32.SetWindowDisplayAffinity(hwnd, 0x11)
        except:
            pass

    def log(self, message):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        if message:
            self.text_area.insert(tk.INSERT, message)
        self.text_area.config(state=tk.DISABLED)
        self.text_area.see(tk.END)

    def setup_hotkeys(self):
        keyboard.add_hotkey(41, lambda: threading.Thread(target=self.process_screen, daemon=True).start())
        keyboard.add_hotkey('right ctrl', self.toggle_follow)

    def toggle_follow(self):
        self.is_following = not self.is_following

    def update_position(self):
        if self.is_following:
            x, y = pyautogui.position()
            self.root.geometry(f"+{x+15}+{y+15}")
        self.root.after(10, self.update_position)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        if not self.is_following:
            deltax = event.x - self.x
            deltay = event.y - self.y
            x = self.root.winfo_x() + deltax
            y = self.root.winfo_y() + deltay
            self.root.geometry(f"+{x}+{y}")

    def resize_window(self, event):
        if not self.is_following:
            new_width = self.root.winfo_pointerx() - self.root.winfo_rootx()
            new_height = self.root.winfo_pointery() - self.root.winfo_rooty()
            if new_width > 100 and new_height > 50:
                self.root.geometry(f"{new_width}x{new_height}")

    def process_screen(self):
        self.log("...")
        try:
            x, y = self.root.winfo_x(), self.root.winfo_y()
            w, h = self.root.winfo_width(), self.root.winfo_height()
            
            screenshot = pyautogui.screenshot(region=(x, y, w+50, h+50))
            screenshot = ImageOps.grayscale(screenshot)
            screenshot = screenshot.point(lambda p: 0 if p < 140 else 255)
            
            text = pytesseract.image_to_string(screenshot, lang='rus+eng')

            if text.strip():
                self.ask_ai(text.strip())
            else:
                self.log("")
        except:
            self.log("[E]")

    def ask_ai(self, prompt):
        session = requests.Session()
        session.trust_env = False 

        payload = {
            "model": MODEL_NAME,
            "prompt": f"Answer briefly: {prompt}",
            "stream": False
        }

        try:
            response = session.post(OLLAMA_URL, json=payload, timeout=20)
            answer = response.json().get('response', '')
            
            self.log(answer)
            self.send_telegram(answer)
        except:
            self.log("[API Error]")

    def send_telegram(self, text):
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        try:
            requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": text}, timeout=5)
        except:
            pass

if __name__ == "__main__":
    GhostAssistant()
