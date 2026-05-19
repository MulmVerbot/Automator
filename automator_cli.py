import pyautogui
import time
import json
import os
from PIL import ImageGrab
import cv2
import numpy as np

class DesktopAutomator:
    def __init__(self):
        self.actions = []
        self.last_click = None
        self.DOUBLE_CLICK_THRESHOLD = 500
        
        try:
            self.load_profile("")
            self.playback()
        except Exception as e:
            print(f"Fehler: {e}")

    def playback(self):
        for a in self.actions:
            if a['type'] == 'click':
                try:
                    btn = a['button'].replace('Button.', '').lower()
                    pyautogui.click(a['x'], a['y'], button=btn)
                except: pass
            elif a['type'] == 'double_click':
                try:
                    btn = a['button'].replace('Button.', '').lower()
                    pyautogui.doubleClick(a['x'], a['y'], interval=a.get('interval', 0.0), button=btn)
                except: pass
            elif a['type'] == 'type_text':
                try:
                    text = a['text']
                    gefilterter_text = text.replace("y", "z") # das wird ein lustiges Problem werden
                    pyautogui.typewrite(a['text'])
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

    def load_profile(self, f):
        f = "vorl/zeiterassung.json"
        if f:
            with open(f, 'r', encoding='utf-8') as fh:
                self.actions = json.load(fh)

if __name__ == "__main__":
    print("Start")
    DesktopAutomator()
    print("Fertsch.")