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
        self.master.title(self.Programm_Name + " " + self.Version)
    ## andere Vars
        self.gespeicherte_Aufzeichnungen = None
        self.verzögerung = 0.1
    ## andere Vars ENDE
        self.GUI_laden()

    def GUI_laden(self):
        print("[-GUI laden-] Gestartet")
        self.aufz_start_knopp = tk.Button(root, text="Aufzeichnung starten", command=self.Aufzeichnung_starten_vor)
        self.aufz_start_knopp.place(x=10,y=40)
        self.aufz_start_l = tk.Label(root, text="Mausclicks aufzeichnen")
        self.aufz_start_l.place(x=10,y=10)
        self.Aufzeichnung_abspielen_maus_knopp = tk.Button(root, text="Aufzeichnung abspielen", command=self.Aufzeichnung_abspielen_maus)
        self.Aufzeichnung_abspielen_maus_knopp.place(x=10,y=70)
        self.ausgabe_mausklicks = tk.Text(root, width="60", height="40")
        self.ausgabe_mausklicks.place(x=300, y=20)
        self.Mausaufzeichnung_zurücksetzen_knopp = tk.Button(root, text="Mausaufzeichnung zurücksetzen", command=self.Mausaufzeichnung_zurücksetzen)
        self.Mausaufzeichnung_zurücksetzen_knopp.place(x=10,y=110)
        self.ausgabe_mausklicks.configure(highlightthickness=0)
        self.ausgabe_mausklicks.configure(state="disabled")

        print("[-GUI laden-] Beendet.")

    def Mausaufzeichnung_zurücksetzen(self):
        print("Mausaufzeichnung_zurücksetzen(def)")
        self.gespeicherte_Aufzeichnungen = []
        self.anzahl_der_clicks = 0
        self.ausgabe_mausklicks.configure(state="normal")
        self.ausgabe_mausklicks.delete("1.0", tk.END)
        self.ausgabe_mausklicks.configure(state="disabled")


    def Aufzeichnung_starten_vor(self):
        self.Maus_aufz_thread = threading.Timer(int(self.verzögerung), self.Aufzeichnung_starten)
        self.Maus_aufz_thread.daemon = True
        self.Maus_aufz_thread.start()
        self.aufz_start_knopp.configure(text="Aufzeichnung stoppen", command=self.Aufzeichnung_thread_stopp)

    def Aufzeichnung_starten(self):
        print("[-Aufzeichnung-] Gestartet.")
        self.gespeicherte_Aufzeichnungen = []

        def on_click(x, y, button, pressed):
            if pressed:
                self.ausgabe_mausklicks.configure(state="normal")
                self.anzahl_der_clicks += 1
                self.gespeicherte_Aufzeichnungen.append(f"{x},{y}")
                self.ausgabe_mausklicks.insert(tk.END, f"{self.anzahl_der_clicks}. Mausklick Cursor-Koordinaten: X= {x} Y={y}\n")
                #print(self.gespeicherte_Aufzeichnungen)
                self.ausgabe_mausklicks.see(tk.END)
                self.ausgabe_mausklicks.configure(state="disabled")

        # Mausklick-Ereignisregistrierung in einem separaten Thread
        self.listener = mouse.Listener(on_click=on_click)
        self.listener.start()

    def Aufzeichnung_thread_stopp(self):
        print("[-Aufzeichnung-] Beendet.")
        self.aufz_start_knopp.configure(text="Aufzeichnung starten", command=self.Aufzeichnung_starten_vor)
        if self.listener:
            self.listener.stop()  # Stoppt den listener damit das endlich mal hinhaut hier
            self.listener = None
            self.anzahl_der_clicks = 0
        try:
            if self.Maus_aufz_thread:
                self.Maus_aufz_thread.cancel()
                self.anzahl_der_clicks = 0
                print("[-Aufzeichnung-] Thread beendet")
        except Exception as e:
            print(f"[-Aufzeichnung-] Fehler beim Beenden des Threads: {e}")

    def Aufzeichnung_abspielen_maus(self):
        print("Aufzeichnung_abspielen_maus(def)")
        if self.gespeicherte_Aufzeichnungen != None or "":
            Zeugs = self.gespeicherte_Aufzeichnungen
            for M in Zeugs:
                kord = M
                x, y = map(float, kord.split(','))
                g3.moveTo(x,y)
                g3.click()
                time.sleep(0.1)
                print(f"Bewegt nach {kord}.")

if __name__ == "__main__":
    root = tk.Tk()
    width = 820
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