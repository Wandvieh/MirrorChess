import tkinter as tk

FELD_GROESSE = 60
BRETT_GROESSE = 8

# Figuren-Symbole
FIGUREN = {
    "P": "♙", "p": "♟",
    "R": "♖", "r": "♜",
    "N": "♘", "n": "♞",
    "B": "♗", "b": "♝",
    "Q": "♕", "q": "♛",
    "K": "♔", "k": "♚",
}


class SchachGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Schachspiel")

        self.spielfeld = [[None for _ in range(BRETT_GROESSE)] for _ in range(BRETT_GROESSE)]
        self.figuren_ids = {}
        self.drag_item = None
        self.ausgewaehlte_figur = None
        self.aktiver_spieler = "weiß"

        self.startbildschirm()

    def startbildschirm(self):
        self.clear_window()
        frame = tk.Frame(self.root)
        frame.pack(pady=100)

        titel = tk.Label(frame, text="Willkommen zum Schachspiel", font=("Arial", 20))
        titel.pack(pady=20)

        start_button = tk.Button(frame, text="Spiel starten", command=self.spielbildschirm)
        start_button.pack()

    def spielbildschirm(self):
        self.clear_window()

        self.canvas = tk.Canvas(self.root, width=BRETT_GROESSE * FELD_GROESSE,
                                height=BRETT_GROESSE * FELD_GROESSE)
        self.canvas.pack()

        self.spielfeld = [[None for _ in range(8)] for _ in range(8)]
        self.figuren_ids.clear()
        self.aktiver_spieler = "weiß"

        self.zeichne_brett()
        self.setze_figuren()

        self.canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)

    def zeichne_brett(self):
        farben = ["#EEEED2", "#769656"]
        for reihe in range(8):
            for spalte in range(8):
                x1 = spalte * FELD_GROESSE
                y1 = reihe * FELD_GROESSE
                x2 = x1 + FELD_GROESSE
                y2 = y1 + FELD_GROESSE
                farbe = farben[(reihe + spalte) % 2]
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=farbe, outline="")

    def setze_figuren(self):
        # Weiße Figuren
        figurenreihe = ["R", "N", "B", "Q", "K", "B", "N", "R"]
        for i, f in enumerate(figurenreihe):
            self.setze_figur(i, 7, f)
            self.setze_figur(i, 6, "P")

        # Schwarze Figuren
        figurenreihe = ["r", "n", "b", "q", "k", "b", "n", "r"]
        for i, f in enumerate(figurenreihe):
            self.setze_figur(i, 0, f)
            self.setze_figur(i, 1, "p")

    def setze_figur(self, x, y, symbol):
        pixel_x = x * FELD_GROESSE + FELD_GROESSE // 2
        pixel_y = y * FELD_GROESSE + FELD_GROESSE // 2
        figur_id = self.canvas.create_text(pixel_x, pixel_y, text=FIGUREN[symbol], font=("Arial", 32))
        self.spielfeld[y][x] = {"symbol": symbol, "id": figur_id, "x": x, "y": y}
        self.figuren_ids[figur_id] = self.spielfeld[y][x]

    def on_mouse_press(self, event):
        x = event.x // FELD_GROESSE
        y = event.y // FELD_GROESSE
        if not (0 <= x < 8 and 0 <= y < 8):
            return
        figur = self.spielfeld[y][x]
        if figur and self.spieler_von(figur["symbol"]) == self.aktiver_spieler:
            self.ausgewaehlte_figur = figur
            self.drag_item = figur["id"]

    def on_mouse_drag(self, event):
        if self.drag_item:
            self.canvas.coords(self.drag_item, event.x, event.y)

    def on_mouse_release(self, event):
        if not self.drag_item or not self.ausgewaehlte_figur:
            return

        ziel_x = event.x // FELD_GROESSE
        ziel_y = event.y // FELD_GROESSE

        if not (0 <= ziel_x < 8 and 0 <= ziel_y < 8):
            self.zentriere_figuren()
            self.reset_drag()
            return

        fx, fy = self.ausgewaehlte_figur["x"], self.ausgewaehlte_figur["y"]

        if self.ist_legaler_zug(fx, fy, ziel_x, ziel_y):
            ziel_feld = self.spielfeld[ziel_y][ziel_x]
            if ziel_feld:
                self.canvas.delete(ziel_feld["id"])

            self.spielfeld[fy][fx] = None
            self.ausgewaehlte_figur["x"] = ziel_x
            self.ausgewaehlte_figur["y"] = ziel_y
            self.spielfeld[ziel_y][ziel_x] = self.ausgewaehlte_figur
            self.canvas.coords(self.drag_item,
                               ziel_x * FELD_GROESSE + FELD_GROESSE // 2,
                               ziel_y * FELD_GROESSE + FELD_GROESSE // 2)
            self.aktiver_spieler = "schwarz" if self.aktiver_spieler == "weiß" else "weiß"
        else:
            self.zentriere_figuren()

        self.reset_drag()

    def ist_legaler_zug(self, fx, fy, tx, ty):
        figur = self.spielfeld[fy][fx]
        ziel = self.spielfeld[ty][tx]
        dx = tx - fx
        dy = ty - fy
        art = figur["symbol"]
        farbe = self.spieler_von(art)

        if ziel and self.spieler_von(ziel["symbol"]) == farbe:
            return False

        if art.lower() == "p":
            richtung = -1 if farbe == "weiß" else 1
            startreihe = 6 if farbe == "weiß" else 1
            if dx == 0 and dy == richtung and not ziel:
                return True
            if dx == 0 and dy == 2 * richtung and fy == startreihe and not ziel and not self.spielfeld[fy + richtung][fx]:
                return True
            if abs(dx) == 1 and dy == richtung and ziel:
                return True
            return False

        if art.lower() == "r":
            if fx == tx or fy == ty:
                return self.ist_weg_frei(fx, fy, tx, ty)
            return False

        if art.lower() == "n":
            return (abs(dx), abs(dy)) in [(1, 2), (2, 1)]

        if art.lower() == "b":
            if abs(dx) == abs(dy):
                return self.ist_weg_frei(fx, fy, tx, ty)
            return False

        if art.lower() == "q":
            if fx == tx or fy == ty or abs(dx) == abs(dy):
                return self.ist_weg_frei(fx, fy, tx, ty)
            return False

        if art.lower() == "k":
            return abs(dx) <= 1 and abs(dy) <= 1

        return False

    def ist_weg_frei(self, fx, fy, tx, ty):
        dx = (tx - fx) and ((tx - fx) // abs(tx - fx))
        dy = (ty - fy) and ((ty - fy) // abs(ty - fy))
        x, y = fx + dx, fy + dy
        while (x, y) != (tx, ty):
            if self.spielfeld[y][x]:
                return False
            x += dx
            y += dy
        return True

    def spieler_von(self, symbol):
        return "weiß" if symbol.isupper() else "schwarz"

    def zentriere_figuren(self):
        for y in range(8):
            for x in range(8):
                figur = self.spielfeld[y][x]
                if figur:
                    self.canvas.coords(figur["id"],
                                       x * FELD_GROESSE + FELD_GROESSE // 2,
                                       y * FELD_GROESSE + FELD_GROESSE // 2)

    def reset_drag(self):
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