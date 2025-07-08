import tkinter as tk
from tkinter import messagebox

ROWS = 2
COLUMNS = 16
FELD_GROESSE = 100  # Pixelgröße

class SchachGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Schachspiel")

        self.spielfeld = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]

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

        # Hauptcontainer
        main_frame = tk.Frame(self.root)
        main_frame.pack()

        # Schachbrett
        brett_frame = tk.Frame(main_frame)
        brett_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=20)
        self.zeichne_brett(brett_frame)

        # Linke Seitenleiste – Eigene Figuren
        eigene_frame = tk.Frame(main_frame)
        eigene_frame.grid(row=1, column=0, padx=10)
        tk.Label(eigene_frame, text="Deine Figuren", font=("Arial", 12)).pack()
        self.eigene_figuren = tk.Label(eigene_frame, text="♙ ♘ ♗ ♖ ♕ ♔", font=("Arial", 14))
        self.eigene_figuren.pack(pady=5)
        tk.Label(eigene_frame, text="Deine Verluste", font=("Arial", 12)).pack()
        self.eigene_verluste = tk.Label(eigene_frame, text="", font=("Arial", 14))
        self.eigene_verluste.pack()

        # Rechte Seitenleiste – Gegner
        gegner_frame = tk.Frame(main_frame)
        gegner_frame.grid(row=1, column=1, padx=10)
        tk.Label(gegner_frame, text="Gegnerische Figuren", font=("Arial", 12)).pack()
        self.gegner_figuren = tk.Label(gegner_frame, text="♟ ♞ ♝ ♜ ♛ ♚", font=("Arial", 14))
        self.gegner_figuren.pack(pady=5)
        tk.Label(gegner_frame, text="Gegnerische Verluste", font=("Arial", 12)).pack()
        self.gegner_verluste = tk.Label(gegner_frame, text="", font=("Arial", 14))
        self.gegner_verluste.pack()

    def zeichne_brett(self, parent):
        canvas = tk.Canvas(parent, width=FELD_GROESSE * COLUMNS,
                           height=FELD_GROESSE * ROWS)
        canvas.pack()
        farben = ["#F4EAE0", "#A76B46"]  # hell/dunkel
        for reihe in range(ROWS):
            for spalte in range(COLUMNS):
                x1 = spalte * FELD_GROESSE
                y1 = reihe * FELD_GROESSE
                x2 = x1 + FELD_GROESSE
                y2 = y1 + FELD_GROESSE
                farbe = farben[(reihe + spalte) % 2]
                canvas.create_rectangle(x1, y1, x2, y2, fill=farbe)

        # Später: Hier Figuren zeichnen
        self.brett_canvas = canvas

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# --- Hauptprogramm
if __name__ == "__main__":
    root = tk.Tk()
    gui = SchachGUI(root)
    root.mainloop()