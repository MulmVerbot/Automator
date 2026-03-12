import keyboard
import pyautogui
import time

# Hier kannst du den Text eingeben, den du automatisch schreiben willst
text_to_type = """"import keyboard
import pyautogui
import time

# Hier kannst du den Text eingeben, den du automatisch schreiben willst
text_to_type = "holger.beese@beese-computer.de"

# Funktion, die den Text schreibt
def type_text():
    time.sleep(0.01)  # Kleine Verzögerung, um Störanfälligkeit zu verringern
    pyautogui.write(text_to_type, interval=0.02)

# Tastenkombination registrieren (Shift + Tab)
keyboard.add_hotkey('a', type_text)

print("Skript läuft. Drücke Shift + Tab, um den Text einzugeben.")
print("Zum Beenden: Drücke ESC.")

# Endlosschleife, bis ESC gedrückt wird
keyboard.wait('esc')"""

# Funktion, die den Text schreibt
def type_text():
    time.sleep(0.01)  # Kleine Verzögerung, um Störanfälligkeit zu verringern
    pyautogui.write(text_to_type, interval=0.02)

# Tastenkombination registrieren (Shift + Tab)
keyboard.add_hotkey('a', type_text)

print("Skript läuft. Drücke Shift + Tab, um den Text einzugeben.")
print("Zum Beenden: Drücke ESC.")

# Endlosschleife, bis ESC gedrückt wird
keyboard.wait('esc')
