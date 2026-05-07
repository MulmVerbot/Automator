import tkinter as tk
from tkinter import filedialog, messagebox
import pyautogui
import pynput
from pynput import mouse
import time
import json
import os
from PIL import ImageGrab
import cv2
import numpy as np

class DesktopAutomator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GUI Automatisierungs-Editor")
        self.actions = []
        self.recording = False
        self.mouse_listener = None

        tk.Button(self.root, text="Aufzeichnung starten", command=self.start_recording).pack(pady=5)
        tk.Button(self.root, text="Aufzeichnung stoppen", command=self.stop_recording).pack(pady=5)
        tk.Button(self.root, text="Knopf-Bild auswählen & hinzufügen", command=self.add_image_click).pack(pady=5)
        tk.Button(self.root, text="Abspielen", command=self.playback).pack(pady=5)
        tk.Button(self.root, text="Profil speichern", command=self.save_profile).pack(pady=5)
        tk.Button(self.root, text="Profil laden", command=self.load_profile).pack(pady=5)
        tk.Button(self.root, text="Ausgewählten Schritt löschen", command=self.delete_step).pack(pady=5)

        self.listbox = tk.Listbox(self.root, width=90, height=20)
        self.listbox.pack(pady=10)
        self.update_list()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def update_list(self):
        self.listbox.delete(0, tk.END)
        for i, a in enumerate(self.actions):
            if a['type'] == 'click':
                txt = f"{i}: Click {a['button']} bei ({a['x']},{a['y']})"
            else:
                txt = f"{i}: Image-Click {a['image_path']}"
            self.listbox.insert(tk.END, txt)

    def start_recording(self):
        if self.recording: return
        self.recording = True
        def on_click(x, y, button, pressed):
            if self.recording and pressed:
                self.actions.append({'type': 'click', 'x': int(x), 'y': int(y), 'button': str(button)})
                self.root.after(0, self.update_list)
        self.mouse_listener = mouse.Listener(on_click=on_click)
        self.mouse_listener.start()

    def stop_recording(self):
        self.recording = False
        if self.mouse_listener:
            self.mouse_listener.stop()
            self.mouse_listener = None

    def add_image_click(self):
        self.root.withdraw()
        time.sleep(0.5)
        def on_capture(x, y, button, pressed):
            if pressed:
                size = 100
                bbox = (int(x-size/2), int(y-size/2), int(x+size/2), int(y+size/2))
                img = ImageGrab.grab(bbox=bbox)
                fn = f"button_{len(self.actions)}.png"
                img.save(fn)
                self.actions.append({'type': 'image_click', 'image_path': fn})
                self.root.after(0, lambda: (self.root.deiconify(), self.update_list()))
                return False
        listener = mouse.Listener(on_click=on_capture)
        listener.start()

    def playback(self):
        for a in self.actions:
            if a['type'] == 'click':
                try:
                    btn = a['button'].replace('Button.', '').lower()
                    pyautogui.click(a['x'], a['y'], button=btn)
                except: pass
            elif a['type'] == 'image_click':
                self.find_and_click_image(a['image_path'])
            time.sleep(0.5)

    def find_and_click_image(self, path, thresh=0.75):
        if not os.path.exists(path): return
        screen = np.array(ImageGrab.grab())
        gray = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)
        templ = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if templ is None: return
        res = cv2.matchTemplate(gray, templ, cv2.TM_CCOEFF_NORMED)
        _, maxv, _, maxloc = cv2.minMaxLoc(res)
        if maxv >= thresh:
            h, w = templ.shape
            pyautogui.click(maxloc[0] + w//2, maxloc[1] + h//2)

    def delete_step(self):
        sel = self.listbox.curselection()
        if sel:
            del self.actions[sel[0]]
            self.update_list()

    def save_profile(self):
        f = filedialog.asksaveasfilename(defaultextension=".json")
        if f:
            with open(f, 'w') as fh:
                json.dump(self.actions, fh)

    def load_profile(self):
        f = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if f:
            with open(f, 'r') as fh:
                self.actions = json.load(fh)
            self.update_list()

    def on_close(self):
        self.stop_recording()
        self.root.destroy()

if __name__ == "__main__":
    # pip install pyautogui pynput pillow opencv-python
    DesktopAutomator()