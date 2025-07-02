import tkinter as tk
from tkinter import ttk
from ChessPiece import figuren_erstellen, hit_possible
import time


class OriginalMirrorChess(tk.Frame):
    def __init__(self, master, return_callback):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")

        self.return_callback = return_callback

        self.ausgewaehlte_figur = None # die Figuren-Klasse
        self.drag_item = None # das Textobjekt

        self.ROWS = 2
        self.COLUMNS = 16
        self.WIDTH = 100
        self.RUNDEN = 16
        self.SPIELER1 = "PC"
        self.SPIELER2 = "Spieler"
        # Wichtig: Spieler1 ist immer oben, Spieler2 ist immer unten (ist relevant für die erlaubten Züge der Bauern)

        self.spielfeld = [[None for _ in range(self.COLUMNS)] for _ in range(self.ROWS)]
        self.canvas_spielfeld = tk.Canvas(self, width=self.COLUMNS*self.WIDTH, height=(self.ROWS + 2)*self.WIDTH, bg="white")
        self.canvas_spielfeld.grid(row=0)

        self.canvas_spielfeld.bind("<ButtonPress-1>", self.on_mouse_press_spielfeld)
        self.canvas_spielfeld.bind("<B1-Motion>", self.on_mouse_drag_spielfeld)
        self.canvas_spielfeld.bind("<ButtonRelease-1>", self.on_mouse_release_spielfeld)

        self.ablage = [None for _ in range(self.COLUMNS)]
        self.geschlagen = []

        self.figuren_pc = figuren_erstellen(self.SPIELER1)
        self.figuren_spieler = figuren_erstellen(self.SPIELER2)
        print(self.figuren_spieler[0].spieler, self.figuren_pc[0].spieler)

        self.zeichne_brett()
        self.setze_startfiguren()
        
        self.back_button = tk.Button(self, text="← Spiel abbrechen", command=self.return_callback)
        self.back_button.grid(row=2, column=0, pady=10)

        continue_button = tk.Button(self, text="Weiter", command=self.next_turn)
        continue_button.grid(row = 3)

        self.PC = 0
        self.SPIELER_SETZEN = 1
        self.SPIELER_SCHLAGEN = 2

        self.spielphase = self.PC
        self.aktuelle_spalte = 0
        self.zuletzt_gezogen = "♟"

    def next_turn(self):
        if self.aktuelle_spalte == self.COLUMNS:
            # Spiel ist zu Ende
            self.end_game()
        elif self.spielphase == self.PC:
            # PC ist dran
            # erste Figur finden, die den Anforderungen entspricht
            for i in range(16):
                if not self.figuren_pc[i].coords and self.zuletzt_gezogen == self.figuren_pc[i].symbol:
                    figur = self.figuren_pc[i]
                    self.setze_figur(self.aktuelle_spalte, 0, figur)
                    break
            """ Schlagen """
            self.pc_schlaegt()
            self.spielphase += 1
            pass
        elif self.spielphase == self.SPIELER_SETZEN:
            pass
        elif self.spielphase == self.SPIELER_SCHLAGEN:
            # Hier muss nichts geprüft werden, der Spieler darf die Runde auch einfach so beenden
            for reihe in range(self.ROWS):
                for spalte in range(self.COLUMNS):
                    try:
                        self.spielfeld[reihe][spalte].neue_runde()
                    except:
                        pass
            self.aktuelle_spalte += 1
            self.spielphase = (self.spielphase + 1) % 3
        print("Runde:", self.aktuelle_spalte, "Phase", self.spielphase)

    def pc_schlaegt(self):
        while True:
            # so lange loopen, bis der pc nicht mehr schlagen kann
            hoechste_wertung = 0
            ergebnis = {}
            for i in range(32):
                alte_x = i % 16
                alte_y = i // 16
                if self.spielfeld[alte_y][alte_x] and self.spielfeld[alte_y][alte_x].spieler == self.SPIELER1:
                    schlagende_figur = self.spielfeld[alte_y][alte_x]
                    # jedes spielfeld durchgehen: steht hier eine weiße figur?
                    for j in range(9):
                        # jedes feld drumherum durchgehen: steht hier eine schwarze figur?
                        neue_x = j % 3
                        neue_y = j // 3
                        if (neue_x < 0 or self.COLUMNS <= neue_x) or (neue_y < 0 or self.ROWS <= neue_y):
                            # kein erlaubtes spielfeld
                            continue
                        if self.spielfeld[neue_y][neue_x] and self.spielfeld[neue_y][neue_x].spieler == self.SPIELER2:
                            zu_schlagende_figur = self.spielfeld[neue_y][neue_x]
                            #ist das ein valider zug? wenn ja, der liste hinzufügen
                            if self.capturing_validity(neue_x, neue_y, schlagende_figur):
                                aktuelle_wertung = self.spielfeld[neue_y][neue_x].wertung
                                if aktuelle_wertung > hoechste_wertung:
                                    hoechste_wertung = aktuelle_wertung
                                    ergebnis["Schlagende"] = schlagende_figur
                                    ergebnis["Geschlagener"] = zu_schlagende_figur
                # ergebnis: den besten zu schlagenden wert mit hoechste_wertung und hoechste_id
            if hoechste_wertung == 0:
                # pc schlägt immer so viel er kann
                break
            time.sleep(1.5)
            # Schlagen
            self.spielfeld[ergebnis["Geschlagener"].coords["y"]][ergebnis["Geschlagener"].coords["x"]] = None
            #self.geschlagen.append(geschlagene_figur) # nur für den Spieler
            self.canvas_spielfeld.delete(ergebnis["Geschlagener"].id)

            self.spielfeld[ergebnis["Schlagende"].coords["y"]][ergebnis["Schlagende"].coords["x"]] = None
            self.spielfeld[ergebnis["Geschlagener"].coords["y"]][ergebnis["Geschlagener"].coords["x"]] = ergebnis["Schlagende"]
            ergebnis["Schlagende"].update_coords(ergebnis["Geschlagener"].coords["x"], ergebnis["Geschlagener"].coords["y"])
            neue_x = ergebnis["Geschlagener"].coords["x"] * self.WIDTH + self.WIDTH // 2
            neue_y = ergebnis["Geschlagener"].coords["y"] * self.WIDTH + self.WIDTH // 2
            self.canvas_spielfeld.coords(ergebnis["Schlagende"].id, neue_x, neue_y)
        return
    
    def end_game(self):
        punkte = 0
        for figur in self.geschlagen:
            """ die Wertigkeiten der Figuren auslesen """
            punkte += figur.wertung
            pass
        print("Spielende!", punkte)
        self.back_button = tk.Button(self, text="Zurück zum Menü", command=self.return_callback)
        self.back_button.grid(row=3)
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
        # wird aktuell nur für das Ziehen aus der Ablage genutzt
        for i in range(len(self.figuren_spieler)):
            self.setze_figur(i, 3, self.figuren_spieler[i], "Ablage")

    def setze_figur(self, x, y, figur, ursprung="Spielfeld"):
        pixel_x = x * self.WIDTH + self.WIDTH // 2
        pixel_y = y * self.WIDTH + self.WIDTH // 2
        symbol = figur.symbol
        figur.update_coords(x, y)
        if ursprung == "Spielfeld":
            figur_id = self.canvas_spielfeld.create_text(pixel_x, pixel_y, text=symbol, font=("Arial", 32), fill=figur.color, anchor="center") # wird gezeichnet
            figur.id = figur_id
            self.spielfeld[y][x] = figur # wird gespeichert
        else:
            figur_id = self.canvas_spielfeld.create_text(pixel_x, pixel_y, text=symbol, font=("Arial", 32), fill=figur.color, anchor="center") # wird gezeichnet
            figur.id = figur_id
            self.ablage[x] = figur # wird gespeichert
    
    def capturing_validity(self, neue_x, neue_y, alte_figur=None):
        if self.ausgewaehlte_figur:
            figur = self.ausgewaehlte_figur
        else: figur = alte_figur
        # Liegt das Feld im validen Bereich?
        if (neue_x < 0 or self.COLUMNS <= neue_x) or (neue_y < 0 or self.ROWS <= neue_y):
            return False
        # Ist das Feld leer?
        if not self.spielfeld[neue_y][neue_x]:
            return False
        # Steht eine eigene Figur auf dem Feld?
        if self.spielfeld[neue_y][neue_x].spieler == figur.spieler:
            return False
        # Prüft, ob sich die Figur so bewegen darf
        return hit_possible(figur, neue_x, neue_y)
        #return True

    def on_mouse_press_spielfeld(self, event):
        # Hier Bedingung einfügen: Wenn man gerade selbst nicht dran ist, nichts tun
        x = event.x // self.WIDTH
        y = event.y // self.WIDTH
        # print(event.x, event.y)
        if 0 <= x < self.COLUMNS and y == 3 and self.ablage[x] and self.spielphase == self.SPIELER_SETZEN:
            # Koordinaten valide, Feld enthält Figur, Spieler ist dran mit Ziehen
            ablagenfigur = self.ablage[x]
            self.ausgewaehlte_figur = ablagenfigur
            self.drag_item = ablagenfigur.id
        elif 0 <= x < self.COLUMNS and 0 <= y < self.ROWS and self.spielfeld[y][x] and self.spielphase == self.SPIELER_SCHLAGEN:
            # Koordinaten valide, Feld enthält Figur, Spieler ist dran mit Schlagen
            if self.spielfeld[y][x].spieler == self.SPIELER1:
                # PC-Figur ausgewählt
                return
            if not self.spielfeld[y][x].ziehbar:
                # Mit der Figur wurde die Runde schon geschlagen
                return
            schlagfigur = self.spielfeld[y][x]
            self.ausgewaehlte_figur = schlagfigur
            self.drag_item = schlagfigur.id

    def on_mouse_drag_spielfeld(self, event):
        if self.drag_item:
            self.canvas_spielfeld.coords(self.drag_item, event.x, event.y)

    def on_mouse_release_spielfeld(self, event):
        if not self.drag_item:
            return

        neue_x = event.x // self.WIDTH
        neue_y = event.y // self.WIDTH
        if (neue_x < 0 or self.COLUMNS <= neue_x) and (neue_y < 0 or self.ROWS <= neue_y):
            # Drag außerhalb: Figur zurücksetzen
            self.canvas_spielfeld.coords(self.drag_item,
                               alte_x * self.WIDTH + self.WIDTH // 2,
                               alte_y * self.WIDTH + self.WIDTH // 2)
        
        alte_x = self.ausgewaehlte_figur.coords["x"]
        alte_y = self.ausgewaehlte_figur.coords["y"]

        uebrige_bauern = 0
        for figur in self.figuren_spieler:
            if figur.coords["y"] == 3 and figur.symbol == "♟":
                uebrige_bauern += 1
        erlaubter_bauer = (self.ausgewaehlte_figur.symbol == "♟" and (uebrige_bauern > 1 or self.aktuelle_spalte == 15)) or self.ausgewaehlte_figur.symbol != "♟"

        erlaubtes_schlagen = self.capturing_validity(neue_x, neue_y)

        if self.spielphase == self.SPIELER_SETZEN and neue_x == self.aktuelle_spalte and neue_y == 1 and erlaubter_bauer:
            # figur wurde aus ablage gezogen UND es wird nicht vor der letzten Runde der letzte Bauer gezogen
            self.ablage[alte_x] = None
            self.zuletzt_gezogen = self.ausgewaehlte_figur.symbol
            self.ausgewaehlte_figur.update_coords(neue_x, neue_y)
            self.spielfeld[neue_y][neue_x] = self.ausgewaehlte_figur
            self.spielphase += 1
            # neue Position zentrieren
            zentriert_x = neue_x * self.WIDTH + self.WIDTH // 2
            zentriert_y = neue_y * self.WIDTH + self.WIDTH // 2
            self.canvas_spielfeld.coords(self.drag_item, zentriert_x, zentriert_y)
        elif self.spielphase == self. SPIELER_SCHLAGEN and erlaubtes_schlagen:
            # figur wurde aus spielfeld gezogen: darf nur schlagen!
            geschlagene_figur = self.spielfeld[neue_y][neue_x]
            self.geschlagen.append(geschlagene_figur)
            self.spielfeld[neue_y][neue_x] = None
            self.canvas_spielfeld.delete(geschlagene_figur.id)
            geschlagene_figur.id = None
            
            self.spielfeld[alte_y][alte_x] = None
            self.spielfeld[neue_y][neue_x] = self.ausgewaehlte_figur
            self.ausgewaehlte_figur.update_coords(neue_x, neue_y)

            # neue Position zentrieren
            zentriert_x = neue_x * self.WIDTH + self.WIDTH // 2
            zentriert_y = neue_y * self.WIDTH + self.WIDTH // 2
            self.canvas_spielfeld.coords(self.drag_item, zentriert_x, zentriert_y)
        else:
            # Drag nicht erlaubt: Figur zurücksetzen
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

        #dummy_btn = tk.Button(self, text="Play 3x16 Mirror Chess", command=lambda: start_game_callback("dummy"))
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
            self.current_screen = OriginalMirrorChess(self, self.show_game_selector)
        elif game_name == "dummy":
            self.current_screen = OriginalMirrorChess(self, self.show_game_selector)


if __name__ == "__main__":
    app = App()
    app.mainloop()