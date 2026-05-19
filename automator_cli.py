import pyautogui
import time
import json
import os
from PIL import ImageGrab
import cv2
import numpy as np


print("Start")
actions = []
last_click = None
DOUBLE_CLICK_THRESHOLD = 500

try:
    automator()
except Exception as e:
    print(f"Fehler: {e}")

def automator():
    f = "vorl/zeiterassung.json"
    if f:
        with open(f, 'r', encoding='utf-8') as fh:
            actions = json.load(fh)
    for a in actions:
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
                find_and_click_image(a['image_path'])
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

