import tkinter as tk
from tkinter import ttk


class OriginalMirrorChess(tk.Frame):
    def __init__(self, master, return_callback):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")

        back_button = tk.Button(self, text="← Spiel abbrechen", command=return_callback)
        back_button.grid(row=2, column=0, pady=10)

        self.ausgewaehlte_figur = None
        self.drag_item = None

        self.ROWS = 2
        self.COLUMNS = 16
        self.WIDTH = 100
        self.RUNDEN = 16

        self.spielfeld = [[None for _ in range(self.COLUMNS)] for _ in range(self.ROWS)]
        self.canvas_spielfeld = tk.Canvas(self, width=self.COLUMNS*self.WIDTH, height=(self.ROWS + 2)*self.WIDTH, bg="white")
        self.canvas_spielfeld.grid(row=0)

        self.canvas_spielfeld.bind("<ButtonPress-1>", self.on_mouse_press_spielfeld)
        self.canvas_spielfeld.bind("<B1-Motion>", self.on_mouse_drag_spielfeld)
        self.canvas_spielfeld.bind("<ButtonRelease-1>", self.on_mouse_release_spielfeld)

        self.ablage = [None for _ in range(self.COLUMNS)]

        self.zeichne_brett()
        self.setze_startfiguren()

        for i in range(self.RUNDEN):
            # PC zieht
            # Spieler zieht
            # Alle Figuren auf dem Feld wieder auf "dürfen ziehen" zurücksetzen
            pass

    
    def zeichne_brett(self):
        farben = ["#EEEED2", "#769656"]
        for reihe in range(self.ROWS):
            for spalte in range(self.COLUMNS):
                x1 = spalte * self.WIDTH
                y1 = reihe * self.WIDTH
                x2 = x1 + self.WIDTH
                y2 = y1 + self.WIDTH
                farbe = farben[(reihe + spalte) % 2]
                self.canvas_spielfeld.create_rectangle(x1, y1, x2, y2, fill=farbe, outline="")
        farben = ["#FFFFFF", "#C1D3AF"]
        for reihe in range(2):
            for spalte in range(self.COLUMNS):
                x1 = spalte * self.WIDTH
                y1 = (reihe + 2) * self.WIDTH
                x2 = x1 + self.WIDTH
                y2 = y1 + self.WIDTH
                self.canvas_spielfeld.create_rectangle(x1, y1, x2, y2, fill=farbe, outline="")

    def setze_startfiguren(self):
        self.setze_figur(0, 0, "♙")  # weißer Bauer
        for i in range(self.COLUMNS):
            self.setze_figur(i, 3, "♙", "Ablage")

    def setze_figur(self, x, y, symbol, check="Spielfeld"):
        pixel_x = x * self.WIDTH + self.WIDTH // 2
        pixel_y = y * self.WIDTH + self.WIDTH // 2
        if check == "Spielfeld":
            figur_id = self.canvas_spielfeld.create_text(pixel_x, pixel_y, text=symbol, font=("Arial", 32)) # wird gezeichnet
            self.spielfeld[y][x] = {"symbol": symbol, "id": figur_id, "x": x, "y": y, "moved": False} # wird gespeichert
        else:
            figur_id = self.canvas_spielfeld.create_text(pixel_x, pixel_y, text=symbol, font=("Arial", 32)) # wird gezeichnet
            self.ablage[x] = {"symbol": symbol, "id": figur_id, "x": x, "y": y, "moved": False} # wird gespeichert

        # notwendige weitere Angaben:
        # x ob sich die Figur in dieser Runde schon bewegt hat
        #   - Hier wird setze_figur nur beim ersten Setzen auf das Spielbrett genutzt. Will ich das ändern, muss ich einbauen, dass "moved" auch True sein kann
        # - in welchem Muster sich die Figur bewegen darf
    
    def check_validity(self, neue_x, neue_y):
        # Prüft, ob man eine Figur bewegen darf
        if self.drag_item: return False
        # darf sie sich so bewegen wie geplant?
        return

    def on_mouse_press_spielfeld(self, event):
        # Hier Bedingung einfügen: Wenn man gerade selbst nicht dran ist, nichts tun
        x = event.x // self.WIDTH
        y = event.y // self.WIDTH
        print(event.x, event.y)
        if 0 <= x < self.COLUMNS and 0 <= y < self.ROWS and self.spielfeld[y][x]:

            figur = self.spielfeld[y][x]
            self.ausgewaehlte_figur = figur
            self.drag_item = figur["id"]
        elif 0 <= x < self.COLUMNS and 3 <= y < (self.ROWS + 2) and self.ablage[x]:
            figur = self.ablage[x]
            self.ausgewaehlte_figur = figur
            self.drag_item = figur["id"]
        
    def on_mouse_drag_spielfeld(self, event):
        if self.drag_item:
            self.canvas_spielfeld.coords(self.drag_item, event.x, event.y)

    def on_mouse_release_spielfeld(self, event):
        if not self.drag_item:
            return

        neue_x = event.x // self.WIDTH
        neue_y = event.y // self.WIDTH

        # Einfügen: Prüfen, ob sich die Figur so bewegen darf (vllt weiter unten einfügen)
        # Kriterien:
        # x Hat in dieser Runde noch nicht gezogen und
        # - darf sich so bewegen
        # - oder der Platz ist leer (wenn aus der Ablage gezogen wird)
        #allowed = self.check_validity(neue_x, neue_y)

        alte_x = self.ausgewaehlte_figur["x"]
        alte_y = self.ausgewaehlte_figur["y"]
        if 0 <= neue_x < self.COLUMNS and 0 <= neue_y < self.ROWS: #and allowed:
            if alte_y < self.ROWS:
                # Figur stand vorher im Spielfeld
                self.spielfeld[alte_y][alte_x] = None
            else:
                # Figur stand vorher in der Ablage
                self.ablage[alte_x] = None

            self.ausgewaehlte_figur["x"] = neue_x
            self.ausgewaehlte_figur["y"] = neue_y
            self.spielfeld[neue_y][neue_x] = self.ausgewaehlte_figur

            # neue Position zentrieren
            zentriert_x = neue_x * self.WIDTH + self.WIDTH // 2
            zentriert_y = neue_y * self.WIDTH + self.WIDTH // 2
            self.canvas_spielfeld.coords(self.drag_item, zentriert_x, zentriert_y)
        else:
            # Drag außerhalb: Figur zurücksetzen
            self.canvas_spielfeld.coords(self.drag_item,
                               alte_x * self.WIDTH + self.WIDTH // 2,
                               alte_y * self.WIDTH + self.WIDTH // 2)

        self.drag_item = None
        self.ausgewaehlte_figur = None


class GameSelector(tk.Frame):
    def __init__(self, master, start_game_callback):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")

        label = tk.Label(self, text="Choose a Game", font=("Arial", 20))
        label.grid(row=0, column=0, pady=20)

        chess_btn = tk.Button(self, text="Play Original Mirror Chess", command=lambda: start_game_callback("chess"))
        chess_btn.grid(row=1, column=0, pady=5)

        #dummy_btn = tk.Button(self, text="Play Another Game", command=lambda: start_game_callback("dummy"))
        #dummy_btn.grid(row=2, column=0, pady=5)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mirror Chess")

        # Ensure the window resizes nicely
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.current_screen = None
        self.show_game_selector()

    def clear_screen(self):
        if self.current_screen:
            self.current_screen.destroy()

    def show_game_selector(self):
        self.clear_screen()
        self.current_screen = GameSelector(self, self.start_game)

    def start_game(self, game_name):
        self.clear_screen()
        if game_name == "chess":
            # Later you could do: self.current_screen = ChessGame(self, self.show_game_selector)
            self.current_screen = OriginalMirrorChess(self, self.show_game_selector)
        elif game_name == "dummy":
            self.current_screen = OriginalMirrorChess(self, self.show_game_selector)


if __name__ == "__main__":
    app = App()
    app.mainloop()