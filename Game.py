import tkinter as tk
import ttkbootstrap as ttk
from Chess import create_player, can_move, ChessPiece
import time


class OriginalMirrorChess(ttk.Frame):
    def __init__(self, master, return_callback):
        super().__init__(master)
        self.grid(row=0, column=0)

        self.return_callback = return_callback

        self.selected_piece = None # die Figuren-Klasse
        self.drag_item = None # das Textobjekt

        self.ROWS = 2
        self.ADDITIONAL_ROWS = 2
        self.COLUMNS = 16
        self.WIDTH = 100
        self.RUNDEN = 16
        self.SPIELER1 = "PC"
        self.SPIELER2 = "Spieler"
        # important: player1 is always starting at the top, player2 always at the bottom (relevant for the pawn's movement)
        self.BOARD = "board"
        self.RESERVE = "reserve"
        self.BOARD_COLORS = ["#CAA48C", "#925B39"]
        self.RULES="RegelnOriginal.txt"

        self.board = [[None for _ in range(self.COLUMNS)] for _ in range(self.ROWS)]
        self.board_canvas = ttk.Canvas(self, width=self.COLUMNS*self.WIDTH, height=(self.ROWS + self.ADDITIONAL_ROWS)*self.WIDTH, bg="white")
        self.board_canvas.grid(row=0)

        self.board_canvas.bind("<ButtonPress-1>", self.on_mouse_press_spielfeld)
        self.board_canvas.bind("<B1-Motion>", self.on_mouse_drag_spielfeld)
        self.board_canvas.bind("<ButtonRelease-1>", self.on_mouse_release_spielfeld)

        self.reserve = [None for _ in range(self.COLUMNS)]
        self.geschlagen = []

        self.player1 = create_player(self.SPIELER1)
        self.player2 = create_player(self.SPIELER2)

        self.draw_board()
        self.draw_reserve()
        self.place_reserve()

        self.button_frame = ttk.Frame(self, width=self.COLUMNS*self.WIDTH)
        self.continue_button = ttk.Button(self.button_frame, text="Spiel starten", command=self.next_turn)
        self.continue_button.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.back_button = ttk.Button(self.button_frame, text="← Zurück zum Menü", command=self.return_callback, style="primary.Link.TButton")
        self.back_button.grid(row=1, column=0, sticky="NEWS", padx=10, pady=10)
        self.back_button = ttk.Button(self.button_frame, text="Regeln", command=self.rule_popup, style="primary.Link.TButton")
        self.back_button.grid(row=1, column=1, sticky="NEWS", padx=10, pady=10)
        self.button_frame.grid(row=2)

        self.PLAYER1_PLACING = 0
        self.PLAYER1_CAPTURING = 1
        self.PLAYER2_PLACING = 2
        self.PLAYER2_CAPTURING = 3

        self.phase = self.PLAYER1_PLACING
        self.current_round = 0
        self.last_moved = "♟"
    
    def draw_board(self):
        """
        draws the board onto the canvas
        """
        for row in range(self.ROWS):
            for column in range(self.COLUMNS):
                x1 = column * self.WIDTH
                y1 = row * self.WIDTH
                x2 = x1 + self.WIDTH
                y2 = y1 + self.WIDTH
                color = self.BOARD_COLORS[(row + column) % 2]
                self.board_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
        self.board_canvas.create_rectangle(0, 0, self.COLUMNS*self.WIDTH, self.ROWS*self.WIDTH-2, fill="", outline=self.BOARD_COLORS[1])
        return
    
    def draw_reserve(self):
        """
        draws the reserve onto the canvas
        also adds the text "Eigene Figuren" above it
        """
        colors = ["#FFFFFF", "#F4EAE0"]
        for row in range(2):
            for column in range(self.COLUMNS):
                x1 = column * self.WIDTH
                y1 = (row + 2) * self.WIDTH
                x2 = x1 + self.WIDTH
                y2 = y1 + self.WIDTH
                self.board_canvas.create_rectangle(x1, y1, x2, y2, fill=colors[row], outline=colors[0])
        self.board_canvas.create_text(16 * self.WIDTH // 2, 2 * self.WIDTH + self.WIDTH // 2, text="Eigene Figuren", anchor="center", fill=self.BOARD_COLORS[1], font=("Arial", 20))

    def place_reserve(self):
        """
        Places the player's pieces in their reserve at the start of the game
        """
        for i in range(len(self.player2)):
            self.place_piece(i, 3, self.player2[i], self.RESERVE)

    def rule_popup(self):
        """
        Creates a popup with the rules of the current game
        """
        with open("assets\\" + self.RULES, encoding="utf-8") as f:
            text = f.read()
        popup = tk.Toplevel()
        popup.wm_title("Regeln")
        ttk.Label(popup, text=text).grid(sticky="nsew")
        pass
    
    def next_turn(self):
        """
        Button logic for advancing the game state. Only actually usable in phase self.PLAYER2_CAPTURING
        """
        if self.continue_button['text'] == "Spiel starten":
            # first time clicking
            self.turn_button_to_inactive(self.continue_button)
            self.pc_turn()

        elif self.phase == self.PLAYER1_PLACING:
            # the PC is currently making its move
            pass
        elif self.phase == self.PLAYER1_CAPTURING:
            # the PC is currently making its move
            pass
        elif self.phase == self.PLAYER2_PLACING:
            # only advanced by placing a piece
            pass
        elif self.phase == self.PLAYER2_CAPTURING:
            # next round can be called, regardless of having captured pieces or not
            for row in range(self.ROWS):
                for column in range(self.COLUMNS):
                    try:
                        self.board[row][column].set_movable()
                    except:
                        pass
            self.current_round += 1
            self.phase = (self.phase + 1) % 4
            if self.current_round == self.COLUMNS:
                # game over
                self.turn_button_to_inactive(self.continue_button)
                self.end_game()
            self.turn_button_to_inactive(self.continue_button)
            self.pc_turn()

    def turn_button_to_inactive(self, button):
        """
        Changes the button text to either
        "Spiel abschließen"
        "Warten auf den Gegner..." or
        "Warten auf deinen Zug..."
        """
        if self.phase == self.PLAYER1_PLACING and self.current_round == self.COLUMNS: button.configure(text="Spiel abschließen")
        elif self.phase == self.PLAYER1_PLACING: button.configure(text="Warten auf den Gegner...")
        else: button.configure(text="Warten auf deinen Zug...")

    def turn_button_to_active(self, button):
        """
        Changes the button text to "Nächste Runde"
        """
        button.configure(text="Nächste Runde")
    
    def pc_turn(self):
        """
        handles the pc's turn
        """
        for i in range(16):
            # chooses the pc's piece
            if not self.player1[i].coords and self.last_moved == self.player1[i].symbol:
                piece = self.player1[i]
                self.place_piece(self.current_round, 0, piece)
                break
        self.phase += 1
        self.pc_captures()
        self.phase += 1
        self.turn_button_to_inactive(self.continue_button)

    def pc_captures(self):
        """
        Handles the logic for the pc's capturing. It will always capture, if there is at least one option
        """
        while True:
            # loops until there is no piece to capture
            best_score = 0
            best_capture = {}
            for i in range(self.ROWS * self.COLUMNS):
                # go through every field on the board
                old_x = i % self.COLUMNS
                old_y = i // self.COLUMNS
                if self.board[old_y][old_x] and self.board[old_y][old_x].player == self.SPIELER1:
                    # is a pc piece on the field?
                    capturing_piece = self.board[old_y][old_x]
                    for j in range(9):
                        # check every field in a radius of 1
                        neue_x = (j % 3) - 1 + old_x
                        neue_y = (j // 3) -1 + old_y
                        print("x:", neue_x, "y:", neue_y)
                        if (neue_x < 0 or self.COLUMNS <= neue_x) or (neue_y < 0 or self.ROWS <= neue_y):
                            print("B")
                            # kein erlaubtes spielfeld
                            continue
                        if self.board[neue_y][neue_x] and self.board[neue_y][neue_x].player == self.SPIELER2:
                            captured_piece = self.board[neue_y][neue_x]
                            #ist das ein valider zug? wenn ja, der liste hinzufügen
                            if self.can_capture(neue_x, neue_y, capturing_piece):
                                print("D")
                                aktuelle_wertung = self.board[neue_y][neue_x].score
                                if aktuelle_wertung > best_score:
                                    best_score = aktuelle_wertung
                                    best_capture["Schlagende"] = capturing_piece
                                    best_capture["Geschlagener"] = captured_piece
                # best_capture: den besten zu schlagenden wert mit hoechste_wertung und hoechste_id
            if best_score == 0:
                # pc schlägt immer so viel er kann
                print("pc kann nicht schlagen")
                break
            self.update_idletasks()
            time.sleep(1.5)
            print("pc kann schlagen")
            # Schlagen
            self.board[best_capture["Geschlagener"].coords["y"]][best_capture["Geschlagener"].coords["x"]] = None
            #self.geschlagen.append(geschlagene_figur) # nur für den Spieler
            self.board_canvas.delete(best_capture["Geschlagener"].id)

            self.board[best_capture["Schlagende"].coords["y"]][best_capture["Schlagende"].coords["x"]] = None
            self.board[best_capture["Geschlagener"].coords["y"]][best_capture["Geschlagener"].coords["x"]] = best_capture["Schlagende"]
            best_capture["Schlagende"].update_coords(best_capture["Geschlagener"].coords["x"], best_capture["Geschlagener"].coords["y"])
            neue_x = best_capture["Geschlagener"].coords["x"] * self.WIDTH + self.WIDTH // 2
            neue_y = best_capture["Geschlagener"].coords["y"] * self.WIDTH + self.WIDTH // 2
            self.board_canvas.coords(best_capture["Schlagende"].id, neue_x, neue_y)
        return
    
    def end_game(self):
        punkte = 0
        for figur in self.geschlagen:
            """ die Wertigkeiten der Figuren auslesen """
            punkte += figur.score
        auswertung = f"{punkte} Punkte erhalten!"
        text_item = self.board_canvas.create_text(self.COLUMNS * self.WIDTH // 2, self.ROWS * self.WIDTH // 2, text=auswertung, anchor="center", fill="#A76B46", font=("Arial", 50))
        bbox = self.board_canvas.bbox(text_item)
        rect_item = self.board_canvas.create_rectangle(bbox, fill="#F4EAE0", outline="#925B39")
        self.board_canvas.tag_raise(text_item,rect_item)
        print("Spielende!", punkte)
        self.continue_button.grid_remove()

    def place_piece(self, x:int, y:int, piece:ChessPiece, destination: str = None) -> None:
        """
        Places the pieces either onto the board or in the player's reserve
        x, y: coordinates to place it on. If destination is None or self.BOARD, x must be between 0 and 15 (inclusive) and y between 0 and 1.
        If destination is the reserve, y must additionally be 0
        piece: the chess piece to be placed
        destination: whether to place it onto the board or into the reserve. default is the board
        """
        if destination == None: destination = self.BOARD
        # get the center of the field
        pixel_x = x * self.WIDTH + self.WIDTH // 2
        pixel_y = y * self.WIDTH + self.WIDTH // 2
        piece.update_coords(x, y)
        if destination == self.BOARD:
            piece_id = self.board_canvas.create_text(pixel_x, pixel_y, text=piece.symbol, font=("Arial", 32), fill=piece.color, anchor="center")
            piece.id = piece_id
            self.board[y][x] = piece
        elif destination == self.RESERVE:
            piece_id = self.board_canvas.create_text(pixel_x, pixel_y, text=piece.symbol, font=("Arial", 32), fill=piece.color, anchor="center")
            piece.id = piece_id
            self.reserve[x] = piece
        return
    
    def can_capture(self, new_x:int, new_y:int, current_piece:ChessPiece = None) -> bool:
        """
        checks for whether a player can capture a piece in a specific spot
        First checks for coordinates being inside the board
        Secon checks for a piece being at the new coordinates
        Third checks for this piece belonging to the other player
        Fourth checks for the piece being allowed to move that way (per the chess rules)
        new_x, new_y: coordinates to go to
        current_piece: only needed when the PC moves, i.e., no piece is currently being dragged
        """
        if current_piece == None:
            # if piece is being dragged
            current_piece = self.selected_piece
        if (new_x < 0 or self.COLUMNS <= new_x) or (new_y < 0 or self.ROWS <= new_y):
            # coordinates are outside the board
            return False
        if not self.board[new_y][new_x]:
            # new coordinates don't have a piece to capture
            return False
        if self.board[new_y][new_x].player == current_piece.player:
            # new coordinates have a piece, but it's the player's
            return False
        # Lastly, checking if this chess piece is allowed to move that way
        return can_move(current_piece, new_x, new_y)

    def on_mouse_press_spielfeld(self, event):
        # Hier Bedingung einfügen: Wenn man gerade selbst nicht dran ist, nichts tun
        x = event.x // self.WIDTH
        y = event.y // self.WIDTH
        #print(event.x, event.y)
        if 0 <= x < self.COLUMNS and y == 3 and self.reserve[x] and self.phase == self.PLAYER2_PLACING:
            # Koordinaten valide, Feld enthält Figur, Spieler ist dran mit Ziehen
            ablagenfigur = self.reserve[x]
            self.selected_piece = ablagenfigur
            self.drag_item = ablagenfigur.id
        elif 0 <= x < self.COLUMNS and 0 <= y < self.ROWS and self.board[y][x] and self.phase == self.PLAYER2_CAPTURING:
            # Koordinaten valide, Feld enthält Figur, Spieler ist dran mit Schlagen
            if self.board[y][x].player == self.SPIELER1:
                # PC-Figur ausgewählt
                return
            if not self.board[y][x].movable:
                # Mit der Figur wurde die Runde schon geschlagen
                return
            schlagfigur = self.board[y][x]
            self.selected_piece = schlagfigur
            self.drag_item = schlagfigur.id

    def on_mouse_drag_spielfeld(self, event):
        if self.drag_item:
            self.board_canvas.coords(self.drag_item, event.x, event.y)

    def on_mouse_release_spielfeld(self, event):
        if not self.drag_item:
            return

        neue_x = event.x // self.WIDTH
        neue_y = event.y // self.WIDTH
        if (neue_x < 0 or self.COLUMNS <= neue_x) and (neue_y < 0 or self.ROWS <= neue_y):
            # Drag außerhalb: Figur zurücksetzen
            self.board_canvas.coords(self.drag_item,
                               alte_x * self.WIDTH + self.WIDTH // 2,
                               alte_y * self.WIDTH + self.WIDTH // 2)
        
        alte_x = self.selected_piece.coords["x"]
        alte_y = self.selected_piece.coords["y"]

        uebrige_bauern = 0
        for figur in self.player2:
            if figur.coords["y"] == 3 and figur.symbol == "♟":
                uebrige_bauern += 1
        erlaubter_bauer = (self.selected_piece.symbol == "♟" and (uebrige_bauern > 1 or self.current_round == 15)) or self.selected_piece.symbol != "♟"

        erlaubtes_schlagen = self.can_capture(neue_x, neue_y)

        if self.phase == self.PLAYER2_PLACING and neue_x == self.current_round and neue_y == 1 and erlaubter_bauer:
            # figur wurde aus ablage gezogen UND es wird nicht vor der letzten Runde der letzte Bauer gezogen
            self.reserve[alte_x] = None
            self.last_moved = self.selected_piece.symbol
            self.selected_piece.update_coords(neue_x, neue_y)
            self.board[neue_y][neue_x] = self.selected_piece
            self.phase += 1
            self.turn_button_to_active(self.continue_button)
            # neue Position zentrieren
            zentriert_x = neue_x * self.WIDTH + self.WIDTH // 2
            zentriert_y = neue_y * self.WIDTH + self.WIDTH // 2
            self.board_canvas.coords(self.drag_item, zentriert_x, zentriert_y)
        elif self.phase == self.PLAYER2_CAPTURING and erlaubtes_schlagen:
            # figur wurde aus spielfeld gezogen: darf nur schlagen!
            geschlagene_figur = self.board[neue_y][neue_x]
            self.geschlagen.append(geschlagene_figur)
            self.board[neue_y][neue_x] = None
            self.board_canvas.delete(geschlagene_figur.id)
            geschlagene_figur.id = None
            
            self.board[alte_y][alte_x] = None
            self.board[neue_y][neue_x] = self.selected_piece
            self.selected_piece.update_coords(neue_x, neue_y)

            # neue Position zentrieren
            zentriert_x = neue_x * self.WIDTH + self.WIDTH // 2
            zentriert_y = neue_y * self.WIDTH + self.WIDTH // 2
            self.board_canvas.coords(self.drag_item, zentriert_x, zentriert_y)
        else:
            # Drag nicht erlaubt: Figur zurücksetzen
            self.board_canvas.coords(self.drag_item,
                    alte_x * self.WIDTH + self.WIDTH // 2,
                    alte_y * self.WIDTH + self.WIDTH // 2)

        self.drag_item = None
        self.selected_piece = None


class GameSelector(ttk.Frame):
    def __init__(self, master, start_game_callback):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")

        label = ttk.Label(self, text="Wähle ein Spiel aus", font=("Arial", 20))
        label.grid(row=0, column=0, pady=10, padx=10)

        chess_btn = ttk.Button(self, text="Spiele das originale Spiegelschach", command=lambda: start_game_callback("chess"))
        chess_btn.grid(row=1, column=0, padx=10, pady=10)

        #dummy_btn = tk.Button(self, text="Play 3x16 Mirror Chess", command=lambda: start_game_callback("dummy"))
        #dummy_btn.grid(row=2, column=0, pady=5)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Spiegelschach")

        self.style = ttk.Style()
        self.style.colors.set("primary", "#925B39")
        self.style.colors.set("secondary", "#572C12")
        self.style.colors.set("selectfg", "#F4EAE0")
        self.style.configure('TButton', font=('Arial', 15))


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