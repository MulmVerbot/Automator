import tkinter as tk
from pynput import mouse
import pyautogui as g3
import time
from pynput.mouse import Controller, Button
from threading import Thread
import threading



class Automator:
    def __init__(self, master):
        self.master = master
        self.Programm_Name = "Automator"
        self.Version = "0.0"
        self.bildschirm_breite, self.bildschirm_hoehe = g3.size()
        self.anzahl_der_clicks = 0
        self.GUI_laden()

    def GUI_laden(self):
        print("[-GUI laden-] Gestartet")
        self.aufz_start_knopp = tk.Button(root, text="Aufzeichnung starten", command=self.Aufzeichnung_starten_vor)
        self.aufz_start_knopp.pack(side="bottom", padx=20, pady=1, expand=True)
        self.aufz_start_l = tk.Label(root, text="Mausclicks aufzeichnen")
        self.aufz_start_l.pack(side="bottom", padx=10, pady=1, expand=True)

        self.ausgabe_mausklicks = tk.Text(root, width="250", height="420")
        self.ausgabe_mausklicks.pack(side="left", padx=10, pady=1, expand=True)
        print("[-GUI laden-] Beendet.")

    def Aufzeichnung_starten_vor(self):
        self.Maus_aufz_thread = threading.Timer(1, self.Aufzeichnung_starten)
        self.Maus_aufz_thread.daemon = True
        self.Maus_aufz_thread.start()
        self.aufz_start_knopp.configure(text="Aufzeichnung stoppen", command=self.Aufzeichnung_thread_stopp)

    def Aufzeichnung_starten(self):
        print("[-Aufzeichnung-] Gestartet.")
        self.gespeicherte_Aufzeichnungen = []
        def on_click(x, y, button, pressed):
            if pressed:
                self.anzahl_der_clicks += 1
                self.ausgabe_mausklicks.insert(tk.END, f"{self.anzahl_der_clicks} Mausklick Cursor-Koordinaten: X= {x} Y={y}\n")
                self.gespeicherte_Aufzeichnungen.append(f"X={x} Y={y}")
                print(self.gespeicherte_Aufzeichnungen)
                #print(f"{self.anzahl_der_clicks} Mausklick\nCursor-Koordinaten: X={x}, Y={y}")

        # Mausklick-Ereignisregistrierung
        with mouse.Listener(on_click=on_click) as listener:
            listener.join()

    def Aufzeichnung_thread_stopp(self):
        print("[-Aufzeichnung-] Beendet.")
        self.aufz_start_knopp.configure(text="Aufzeichnung starten", command=self.Aufzeichnung_starten_vor)
        try:
            self.Maus_aufz_thread.join()
            print("Thread beendet")
        except Exception as E:
            print("[-Aufzeichnung-] Thread der Mausaufzeichnung_Benden is abgekackt.")

if __name__ == "__main__":
    root = tk.Tk()
    width = 444
    height = 420
    def mittig_fenster(root, width, height):
        fenster_breite = root.winfo_screenwidth()
        fenster_höhe = root.winfo_screenheight()
        x = (fenster_breite - width) // 2
        y = (fenster_höhe - height) // 2
        root.geometry(f"{width}x{height}+{x}+{y}")
    mittig_fenster(root, width, height)
    Automator = Automator(root)
    root.mainloop()