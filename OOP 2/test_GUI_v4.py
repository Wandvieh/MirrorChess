import tkinter as tk
from tkinter import ttk


class OriginalMirrorChess(tk.Frame):
    def __init__(self, master, return_callback):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")

        back_button = tk.Button(self, text="← Spiel abbrechen", command=return_callback)
        back_button.grid(row=1, column=0, pady=10)

        self.ausgewaehlte_figur = None
        self.drag_item = None

        self.ROWS = 2
        self.COLUMNS = 16
        self.WIDTH = 100
        self.spielfeld = [[None for _ in range(self.ROWS)] for _ in range(self.COLUMNS)]

        self.canvas = tk.Canvas(self, width=self.COLUMNS*self.WIDTH, height=self.ROWS*self.WIDTH, bg="white")
        self.canvas.grid(row=0)

        self.zeichne_brett()
        self.setze_startfigur()

        self.canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)
    
    def zeichne_brett(self):
        farben = ["#EEEED2", "#769656"]
        for reihe in range(self.ROWS):
            for spalte in range(self.COLUMNS):
                x1 = spalte * self.WIDTH
                y1 = reihe * self.WIDTH
                x2 = x1 + self.WIDTH
                y2 = y1 + self.WIDTH
                farbe = farben[(reihe + spalte) % 2]
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=farbe, outline="")

    def setze_startfigur(self):
        self.setze_figur(0, 0, "♙")  # weißer Bauer
    
    def setze_figur(self, x, y, symbol):
        pixel_x = x * self.WIDTH + self.WIDTH // 2
        pixel_y = y * self.WIDTH + self.WIDTH // 2
        figur_id = self.canvas.create_text(pixel_x, pixel_y, text=symbol, font=("Arial", 32))
        self.spielfeld[y][x] = {"symbol": symbol, "id": figur_id, "x": x, "y": y}

    def on_mouse_press(self, event):
        x = event.x // self.WIDTH
        y = event.y // self.WIDTH
        if 0 <= x < self.COLUMNS and 0 <= y < self.ROWS:
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

        neue_x = event.x // self.WIDTH
        neue_y = event.y // self.WIDTH

        if 0 <= neue_x < self.COLUMNS and 0 <= neue_y < self.ROWS:
            # Figur verschieben
            alte_x = self.ausgewaehlte_figur["x"]
            alte_y = self.ausgewaehlte_figur["y"]
            self.spielfeld[alte_y][alte_x] = None

            self.ausgewaehlte_figur["x"] = neue_x
            self.ausgewaehlte_figur["y"] = neue_y
            self.spielfeld[neue_y][neue_x] = self.ausgewaehlte_figur

            # neue Position zentrieren
            zentriert_x = neue_x * self.WIDTH + self.WIDTH // 2
            zentriert_y = neue_y * self.WIDTH + self.WIDTH // 2
            self.canvas.coords(self.drag_item, zentriert_x, zentriert_y)
        else:
            # Drag außerhalb: Figur zurücksetzen
            alte_x = self.ausgewaehlte_figur["x"]
            alte_y = self.ausgewaehlte_figur["y"]
            self.canvas.coords(self.drag_item,
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