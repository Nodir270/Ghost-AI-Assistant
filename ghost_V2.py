import tkinter as tk
import os
import sys
import ctypes
from threading import Thread

try:
    import win32api
    import win32con
    import pyautogui
    import pytesseract
    import requests
    import keyboard

    from PIL import ImageOps
except ImportError:
    print("Error! Execute: pip install pywin32 pyautogui pytesseract requests keyboard Pillow")
    sys.exit()

TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
if os.path.exists(TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


class PureTextOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.4)
        self.root.config(bg='black')

        self.width, self.height = 500, 280
        self.follow_mode = True
        self._drag_data = {"x": 0, "y": 0}

        self.main_frame = tk.Frame(self.root, bg='black', highlightthickness=0)
        self.main_frame.pack(fill="both", expand=True)

        self.content_label = tk.Label(self.main_frame, text="Ready",
                                      fg="white", bg="black", font=("Arial", 10),
                                      wraplength=480, justify="left", anchor="nw")
        self.content_label.pack(fill="both", expand=True, padx=15, pady=15)

        self.resizer = tk.Frame(self.root, bg="#222222", cursor="size_nw_se")

        hwnd = self.root.winfo_id()
        ctypes.windll.user32.SetWindowDisplayAffinity(hwnd, 0x11)

        self.main_frame.bind("<Button-1>", self.start_drag)
        self.main_frame.bind("<B1-Motion>", self.do_drag)
        self.resizer.bind("<Button-1>", self.start_drag)
        self.resizer.bind("<B1-Motion>", self.do_resize)

        keyboard.unhook_all()
        try:
            keyboard.add_hotkey(41, self.trigger_solve)
            keyboard.add_hotkey('right ctrl', self.toggle_mode)
        except Exception as e:
            print(f"Bind Bug: {e}")

        self.update_loop()
        self.root.mainloop()

    def toggle_mode(self):
        self.follow_mode = not self.follow_mode
        if self.follow_mode:
            self.resizer.place_forget()
        else:
            self.resizer.place(relx=1.0, rely=1.0, x=-8, y=-8, width=8, height=8)
            self.root.focus_force()

    def update_loop(self):
        if self.follow_mode:
            try:
                x, y = win32api.GetCursorPos()
                self.root.geometry(f"+{x + 15}+{y + 15}")
            except:
                pass
        self.root.after(16, self.update_loop)

    def start_drag(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def do_drag(self, event):
        if not self.follow_mode:
            x = self.root.winfo_x() + (event.x - self._drag_data["x"])
            y = self.root.winfo_y() + (event.y - self._drag_data["y"])
            self.root.geometry(f"+{x}+{y}")

    def do_resize(self, event):
        if not self.follow_mode:
            self.width = max(150, self.root.winfo_width() + (event.x - self._drag_data["x"]))
            self.height = max(80, self.root.winfo_height() + (event.y - self._drag_data["y"]))
            self.root.geometry(f"{self.width}x{self.height}")
            self.content_label.config(wraplength=self.width - 30)

    def trigger_solve(self):
        region = (self.root.winfo_x(), self.root.winfo_y(), self.width, self.height)
        Thread(target=self.solve_process, args=(region,), daemon=True).start()

    def solve_process(self, region):
        try:
            self.update_text("...")
            img = pyautogui.screenshot(region=region)
            text = pytesseract.image_to_string(ImageOps.grayscale(img), lang='rus+eng').strip()
            if len(text) > 2:
                ans = self.ask_ai(text)
                self.update_text(ans)
            else:
                self.update_text("?")
        except:
            self.update_text("Error")

    def ask_ai(self, text):
        url = "http://127.0.0.1:11434/api/generate"
        session = requests.Session()
        session.trust_env = False
        try:
            r = session.post(url, json={
                "model": "minimax-m2.7:cloud",
                "prompt": f"Реши кратко: {text}",
                "stream": False
            }, timeout=25)
            return r.json().get('response', 'Empty')
        except:
            return "Ollama Offline"

    def update_text(self, text):
        self.root.after(0, lambda: self.content_label.config(text=text))


if __name__ == "__main__":
    PureTextOverlay()
