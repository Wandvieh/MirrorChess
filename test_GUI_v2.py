import tkinter as tk

BRETT_GROESSE = 8
FELD_GROESSE = 60

class SchachGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Schachspiel mit Drag & Drop")

        self.spielfeld = [[None for _ in range(BRETT_GROESSE)] for _ in range(BRETT_GROESSE)]
        self.figuren_images = {}  # für spätere Erweiterung

        self.ausgewaehlte_figur = None
        self.drag_item = None

        self.clear_window()
        self.spielbildschirm()

    def spielbildschirm(self):
        self.clear_window()

        self.canvas = tk.Canvas(self.root, width=BRETT_GROESSE * FELD_GROESSE,
                                height=BRETT_GROESSE * FELD_GROESSE)
        self.canvas.grid(row=0, column=0)

        self.zeichne_brett()
        self.setze_startfiguren()

        self.canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)

    def zeichne_brett(self):
        farben = ["#EEEED2", "#769656"]
        for reihe in range(BRETT_GROESSE):
            for spalte in range(BRETT_GROESSE):
                x1 = spalte * FELD_GROESSE
                y1 = reihe * FELD_GROESSE
                x2 = x1 + FELD_GROESSE
                y2 = y1 + FELD_GROESSE
                farbe = farben[(reihe + spalte) % 2]
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=farbe, outline="")

    def setze_startfiguren(self):
        # Beispiel: zwei Figuren zum Testen
        self.setze_figur(0, 6, "♟")  # schwarzer Bauer
        self.setze_figur(0, 1, "♙")  # weißer Bauer

    def setze_figur(self, x, y, symbol):
        pixel_x = x * FELD_GROESSE + FELD_GROESSE // 2
        pixel_y = y * FELD_GROESSE + FELD_GROESSE // 2
        figur_id = self.canvas.create_text(pixel_x, pixel_y, text=symbol, font=("Arial", 32))
        self.spielfeld[y][x] = {"symbol": symbol, "id": figur_id, "x": x, "y": y}

    def on_mouse_press(self, event):
        x = event.x // FELD_GROESSE
        y = event.y // FELD_GROESSE
        if 0 <= x < 8 and 0 <= y < 8:
            figur = self.spielfeld[y][x]
            if figur:
                self.ausgewaehlte_figur = figur
                self.drag_item = figur["id"]

    def on_mouse_drag(self, event):
        if self.drag_item:
            self.canvas.coords(self.drag_item, event.x, event.y)

    def on_mouse_release(self, event):
        if not self.drag_item:
            return

        neue_x = event.x // FELD_GROESSE
        neue_y = event.y // FELD_GROESSE

        if 0 <= neue_x < 8 and 0 <= neue_y < 8:
            # Figur verschieben
            alte_x = self.ausgewaehlte_figur["x"]
            alte_y = self.ausgewaehlte_figur["y"]
            self.spielfeld[alte_y][alte_x] = None

            self.ausgewaehlte_figur["x"] = neue_x
            self.ausgewaehlte_figur["y"] = neue_y
            self.spielfeld[neue_y][neue_x] = self.ausgewaehlte_figur

            # neue Position zentrieren
            zentriert_x = neue_x * FELD_GROESSE + FELD_GROESSE // 2
            zentriert_y = neue_y * FELD_GROESSE + FELD_GROESSE // 2
            self.canvas.coords(self.drag_item, zentriert_x, zentriert_y)
        else:
            # Drag außerhalb: Figur zurücksetzen
            alte_x = self.ausgewaehlte_figur["x"]
            alte_y = self.ausgewaehlte_figur["y"]
            self.canvas.coords(self.drag_item,
                               alte_x * FELD_GROESSE + FELD_GROESSE // 2,
                               alte_y * FELD_GROESSE + FELD_GROESSE // 2)

        self.drag_item = None
        self.ausgewaehlte_figur = None

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Hauptprogramm
if __name__ == "__main__":
    root = tk.Tk()
    gui = SchachGUI(root)
    root.mainloop()