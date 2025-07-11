import tkinter as tk
import ttkbootstrap as ttk
from Chess import create_player, can_move_limited, can_move, ChessPiece
import time
import random
import pygame


class MirrorChess(ttk.Frame):
    def __init__(self, master, return_callback, language_texts:str):
        super().__init__(master)
        self.grid(row=0, column=0)

        self.return_callback = return_callback
        self.language_texts = language_texts

        self.selected_piece = None # die Figuren-Klasse
        self.drag_item = None # das Textobjekt

        pygame.mixer.init()
        self.place_sound = pygame.mixer.Sound("assets\\sounds\\general_chess_sounds_1.wav")

        self.set_attributes()

        self.board = [[None for _ in range(self.COLUMNS)] for _ in range(self.ROWS)]
        self.board_canvas = ttk.Canvas(self, width=self.COLUMNS*self.WIDTH, height=(self.ROWS + self.ADDITIONAL_ROWS)*self.WIDTH, bg="white")
        self.board_canvas.grid(row=0)

        self.board_canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.board_canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.board_canvas.bind("<ButtonRelease-1>", self.on_mouse_release)

        self.reserve = [None for _ in range(self.COLUMNS)]
        self.captured = []

        self.player1 = create_player(self.PLAYER1)
        self.player2 = create_player(self.PLAYER2)

        self.draw_board()
        self.draw_reserve()
        self.place_reserve()

        self.button_frame = ttk.Frame(self, width=self.COLUMNS*self.WIDTH)
        self.continue_button = ttk.Button(self.button_frame, text=self.language_texts[5], command=self.next_turn)
        self.continue_button.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.back_button = ttk.Button(self.button_frame, text=self.language_texts[10], command=self.return_callback, style="primary.Link.TButton")
        self.back_button.grid(row=1, column=0, sticky="NEWS", padx=10, pady=10)
        self.back_button = ttk.Button(self.button_frame, text=self.language_texts[11], command=self.rule_popup, style="primary.Link.TButton")
        self.back_button.grid(row=1, column=1, sticky="NEWS", padx=10, pady=10)
        self.button_frame.grid(row=2)


        self.PLAYER1_PLACING = 0
        self.PLAYER1_CAPTURING = 1
        self.PLAYER2_PLACING = 2
        self.PLAYER2_CAPTURING = 3

        self.phase = self.PLAYER1_PLACING
        self.current_round = 0
    
    def set_attributes(self) -> None:
        '''
        Sets a bunch of fixed attributes for the game. Is here so it can be changed for child classes
        '''
        self.ROWS = 2
        self.ADDITIONAL_ROWS = 2
        self.COLUMNS = 16
        self.WIDTH = 100
        self.RUNDEN = 16
        self.PLAYER1 = "pc"
        self.PLAYER2 = "player"
        # important: player1 is always starting at the top, player2 always at the bottom (relevant for the pawn's movement)
        self.BOARD = "board"
        self.RESERVE = "reserve"
        self.BOARD_COLORS = ["#CAA48C", "#925B39"]
        self.SECONDARY_COLORS = ["#FFFFFF", "#F4EAE0"]
        self.last_moved = "♟"
        return

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
        for row in range(self.ADDITIONAL_ROWS):
            for column in range(self.COLUMNS):
                x1 = column * self.WIDTH
                y1 = (row + self.ROWS) * self.WIDTH
                x2 = x1 + self.WIDTH
                y2 = y1 + self.WIDTH
                self.board_canvas.create_rectangle(x1, y1, x2, y2, fill=self.SECONDARY_COLORS[row], outline=self.SECONDARY_COLORS[0])
        self.board_canvas.create_text(self.COLUMNS * self.WIDTH // 2, self.ROWS * self.WIDTH + self.WIDTH // 2, text=self.language_texts[4], anchor="center", fill=self.BOARD_COLORS[1], font=("Arial", 20))

    def place_reserve(self):
        """
        Places the player's pieces in their reserve at the start of the game
        """
        for i in range(len(self.player2)):
            self.place_piece(i, self.ROWS+self.ADDITIONAL_ROWS-1, self.player2[i], self.RESERVE)

    def rule_popup(self):
        """
        Creates a popup with the rules of the current game
        """
        popup = tk.Toplevel()
        popup.wm_title(self.language_texts[11])
        ttk.Label(popup, text=self.language_texts[12]).grid(sticky="nsew")
        pass
    
    def next_turn(self):
        """
        Button logic for advancing the game state. Only actually usable in phase self.PLAYER2_CAPTURING
        """
        if self.continue_button['text'] == self.language_texts[5]:
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
        if self.phase == self.PLAYER1_PLACING and self.current_round == self.COLUMNS: button.configure(text=self.language_texts[9])
        elif self.phase == self.PLAYER1_PLACING: button.configure(text=self.language_texts[6])
        else: button.configure(text=self.language_texts[7])

    def turn_button_to_active(self, button):
        """
        Changes the button text to "Nächste Runde"
        """
        button.configure(text=self.language_texts[8])
    
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
        Handles the logic for the pc's capturing. It will always capture if there is at least one option
        """
        while True:
            # loops until there is no piece to capture
            best_score = 0
            best_capture = {}
            for i in range(self.ROWS * self.COLUMNS):
                # go through every field on the board
                old_x = i % self.COLUMNS
                old_y = i // self.COLUMNS
                if self.board[old_y][old_x] and self.board[old_y][old_x].player == self.PLAYER1 and self.board[old_y][old_x].movable:
                    # is a pc piece on the field?
                    capturing_piece = self.board[old_y][old_x]
                    if capturing_piece.symbol == "♞":
                        # logic only for the knight
                        for j in [-2,2]:
                            for k in [-1,1]:
                                new_x = j + old_x
                                new_y = k + old_y
                                if (new_x < 0 or self.COLUMNS <= new_x) or (new_y < 0 or self.ROWS <= new_y):
                                    # field inside the board?
                                    continue
                                if self.board[new_y][new_x] and self.board[new_y][new_x].player == self.PLAYER2:
                                    # enemy piece on this position?
                                    captured_piece = self.board[new_y][new_x]
                                    current_score = self.board[new_y][new_x].score
                                    if current_score > best_score:
                                        # larger score? if yes, that's the new piece to capture
                                        best_score = current_score
                                        best_capture["capturing"] = capturing_piece
                                        best_capture["captured"] = captured_piece
                    else:
                        for j in range(9):
                            # check every field in a radius of 1
                            new_x = (j % 3) - 1 + old_x
                            new_y = (j // 3) -1 + old_y
                            if (new_x < 0 or self.COLUMNS <= new_x) or (new_y < 0 or self.ROWS <= new_y):
                                # field inside the board?
                                continue
                            if self.board[new_y][new_x] and self.board[new_y][new_x].player == self.PLAYER2:
                                # enemy piece on this position?
                                captured_piece = self.board[new_y][new_x]
                                if can_move_limited(capturing_piece, new_x, new_y):
                                    # valid chess move?
                                    current_score = self.board[new_y][new_x].score
                                    if current_score > best_score:
                                        # larger score? if yes, that's the new piece to capture
                                        best_score = current_score
                                        best_capture["capturing"] = capturing_piece
                                        best_capture["captured"] = captured_piece
            if best_score == 0:
                # pc always captures if it can
                break
            self.update_idletasks()
            time.sleep(1.5)

            # deleting the captured piece
            self.board[best_capture["captured"].coords["y"]][best_capture["captured"].coords["x"]] = None
            self.board_canvas.delete(best_capture["captured"].id)

            self.place_sound.play()

            # moving the capturing piece onto its new field 
            self.board[best_capture["capturing"].coords["y"]][best_capture["capturing"].coords["x"]] = None
            self.board[best_capture["captured"].coords["y"]][best_capture["captured"].coords["x"]] = best_capture["capturing"]
            best_capture["capturing"].update_coords(best_capture["captured"].coords["x"], best_capture["captured"].coords["y"])
            best_capture["capturing"].set_unmovable()
            new_x = best_capture["captured"].coords["x"] * self.WIDTH + self.WIDTH // 2
            new_y = best_capture["captured"].coords["y"] * self.WIDTH + self.WIDTH // 2
            self.board_canvas.coords(best_capture["capturing"].id, new_x, new_y)
        return
    
    def end_game(self):
        """
        Displays the points
        """
        points = 0
        for piece in self.captured:
            points += piece.score
        message = str(points) + self.language_texts[13]
        text_item = self.board_canvas.create_text(self.COLUMNS * self.WIDTH // 2, self.ROWS * self.WIDTH // 2, text=message, anchor="center", fill=self.BOARD_COLORS[1], font=("Arial", 50))
        bbox = self.board_canvas.bbox(text_item)
        rect_item = self.board_canvas.create_rectangle(bbox, fill="#F4EAE0", outline=self.BOARD_COLORS[1])
        self.board_canvas.tag_raise(text_item,rect_item)
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
            self.place_sound.play()
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
        return can_move_limited(current_piece, new_x, new_y)

    def on_mouse_press(self, event):
        """
        Handles the event of a mouse press. A player can only drag a piece if:
        - the click is on the board and it's the player's turn for capturing and there is a piece on that field (and it's not the pc's)
        - or the click is on the reserve and it's the player's turn for setting
        """
        x = event.x // self.WIDTH
        y = event.y // self.WIDTH
        if 0 <= x < self.COLUMNS and y == self.ROWS + self.ADDITIONAL_ROWS - 1 and self.reserve[x] and self.phase == self.PLAYER2_PLACING:
            # Setting from the reserve
            ablagenfigur = self.reserve[x]
            self.selected_piece = ablagenfigur
            self.drag_item = ablagenfigur.id
        elif 0 <= x < self.COLUMNS and 0 <= y < self.ROWS and self.board[y][x] and self.phase == self.PLAYER2_CAPTURING:
            # Capturing from the board
            if self.board[y][x].player == self.PLAYER1:
                # Chosen a piece of the pc
                return
            if not self.board[y][x].movable:
                # Piece has already been moved this round
                return
            capturing_piece = self.board[y][x]
            self.selected_piece = capturing_piece
            self.drag_item = capturing_piece.id

    def on_mouse_drag(self, event):
        """
        Handles the event of a mouse drag after pressing. If there is an item being dragged, it updates its drawing coordinates
        """
        if self.drag_item:
            self.board_canvas.coords(self.drag_item, event.x, event.y)

    def on_mouse_release(self, event):
        """
        Handles the event of a mouse release
        """
        if not self.drag_item:
            return
        
        new_x = event.x // self.WIDTH
        new_y = event.y // self.WIDTH
        
        old_x = self.selected_piece.coords["x"]
        old_y = self.selected_piece.coords["y"]

        # getting the current amount of pawns
        remaining_pawns = 0
        for piece in self.player2[:8]:
            if piece.coords["y"] == self.ROWS + self.ADDITIONAL_ROWS -1 and piece.symbol == "♟":
                remaining_pawns += 1
        pawn_allowed = (self.selected_piece.symbol == "♟" and (remaining_pawns > 1 or self.current_round == 15)) or self.selected_piece.symbol != "♟"

        allowed_capture = self.can_capture(new_x, new_y)

        if self.phase == self.PLAYER2_PLACING and new_x == self.current_round and new_y == self.ROWS-1 and pawn_allowed:
            # piece has been moved from reserve AND it's not the last pawn before the last round
            self.reserve[old_x] = None
            self.last_moved = self.selected_piece.symbol
            self.selected_piece.update_coords(new_x, new_y)
            self.board[new_y][new_x] = self.selected_piece
            self.phase += 1
            self.turn_button_to_active(self.continue_button)

            self.place_sound.play()

            # centering the new position
            centered_x = new_x * self.WIDTH + self.WIDTH // 2
            centered_y = new_y * self.WIDTH + self.WIDTH // 2
            self.board_canvas.coords(self.drag_item, centered_x, centered_y)
        elif self.phase == self.PLAYER2_CAPTURING and allowed_capture:
            # piece has been moved from board and captures
            captured_piece = self.board[new_y][new_x]
            self.captured.append(captured_piece)
            self.board[new_y][new_x] = None
            self.board_canvas.delete(captured_piece.id)
            captured_piece.id = None
            
            self.board[old_y][old_x] = None
            self.board[new_y][new_x] = self.selected_piece
            self.selected_piece.update_coords(new_x, new_y)
            self.selected_piece.set_unmovable()

            self.place_sound.play()

            # centering the new position
            centered_x = new_x * self.WIDTH + self.WIDTH // 2
            centered_y = new_y * self.WIDTH + self.WIDTH // 2
            self.board_canvas.coords(self.drag_item, centered_x, centered_y)
        else:
            # drag not allowed: set the piece back
            self.board_canvas.coords(self.drag_item,
                    old_x * self.WIDTH + self.WIDTH // 2,
                    old_y * self.WIDTH + self.WIDTH // 2)

        self.drag_item = None
        self.selected_piece = None


class OriginalMirrorChess(MirrorChess):
    def __init__(self, master, return_callback, language):
        super().__init__(master, return_callback, language)


class WiderMirrorChess(MirrorChess):
    def __init__(self, master, return_callback, language):
        super().__init__(master, return_callback, language)

        self.player1_set = [True] * self.COLUMNS
        self.player2_set = [True] * self.COLUMNS
        print(self.player1_set)
        return
    
    def set_attributes(self) -> None:
        '''
        Sets a bunch of fixed attributes for the game. Is here so it can be changed for child classes
        '''
        self.ROWS = 3
        self.ADDITIONAL_ROWS = 2
        self.COLUMNS = 16
        self.WIDTH = 100
        self.RUNDEN = 16
        self.PLAYER1 = "pc"
        self.PLAYER2 = "player"
        # important: player1 is always starting at the top, player2 always at the bottom (relevant for the pawn's movement)
        self.BOARD = "board"
        self.RESERVE = "reserve"
        self.BOARD_COLORS = ["#CAA48C", "#925B39"]
        self.SECONDARY_COLORS = ["#FFFFFF", "#F4EAE0"]
        self.last_moved = "♟"
        return
    
    def pc_turn(self):
        """
        handles the pc's turn
        """
        next = True
        while next:
            # chooses the pc's piece randomly
            new_piece = random.randint(0,15)
            if not self.player1[new_piece].coords:
                while next:
                    new_x = random.randint(0,15)
                    if self.player1_set[new_x]:
                        piece = self.player1[new_piece]
                        self.place_piece(new_x, 0, piece)
                        self.player1_set[new_x] = False
                        next = False
        self.phase += 1
        self.pc_captures()
        self.phase += 1
        self.turn_button_to_inactive(self.continue_button)

    def pc_captures(self):
        """
        Handles the logic for the pc's capturing. It will always capture if there is at least one option
        """
        while True:
            # loops until there is no piece to capture
            best_score = 0
            best_capture = {}
            for i in range(self.ROWS * self.COLUMNS):
                # go through every field on the board
                old_x = i % self.COLUMNS
                old_y = i // self.COLUMNS
                if self.board[old_y][old_x] and self.board[old_y][old_x].player == self.PLAYER1 and self.board[old_y][old_x].movable:
                    # is a pc piece on the field?
                    capturing_piece = self.board[old_y][old_x]
                    if capturing_piece.symbol == "♞":
                        # logic only for the knight
                        moves = []
                        for j in [-2,2]:
                            for k in [-1,1]:
                                moves.append((j,k))
                        for j in [-1,1]:
                            for k in [-2,2]:
                                moves.append((j,k))
                        for move in moves:
                            new_x = move[0] + old_x
                            new_y = move[1] + old_y
                            if (new_x < 0 or self.COLUMNS <= new_x) or (new_y < 0 or self.ROWS <= new_y):
                                # field outside the board?
                                continue
                            if self.board[new_y][new_x] and self.board[new_y][new_x].player == self.PLAYER2:
                                # enemy piece on this position?
                                captured_piece = self.board[new_y][new_x]
                                current_score = self.board[new_y][new_x].score
                                if current_score > best_score:
                                    # larger score? if yes, that's the new piece to capture
                                    best_score = current_score
                                    best_capture["capturing"] = capturing_piece
                                    best_capture["captured"] = captured_piece
                    else:
                        for j in range(self.ROWS * self.COLUMNS):
                            # check every field in a radius of 1
                            new_x = j % self.COLUMNS
                            new_y = j  // self.COLUMNS
                            if (new_x < 0 or self.COLUMNS <= new_x) or (new_y < 0 or self.ROWS <= new_y):
                                # field inside the board?
                                continue
                            if self.board[new_y][new_x] and self.board[new_y][new_x].player == self.PLAYER2:
                                # enemy piece on this position?
                                captured_piece = self.board[new_y][new_x]
                                if can_move(capturing_piece, new_x, new_y, self.board):
                                    # valid chess move?
                                    current_score = self.board[new_y][new_x].score
                                    if current_score > best_score:
                                        # larger score? if yes, that's the new piece to capture
                                        best_score = current_score
                                        best_capture["capturing"] = capturing_piece
                                        best_capture["captured"] = captured_piece
            if best_score == 0:
                # pc always captures if it can
                break
            self.update_idletasks()
            time.sleep(1.5)

            # deleting the captured piece
            self.board[best_capture["captured"].coords["y"]][best_capture["captured"].coords["x"]] = None
            self.board_canvas.delete(best_capture["captured"].id)

            self.place_sound.play()

            # moving the capturing piece onto its new field 
            self.board[best_capture["capturing"].coords["y"]][best_capture["capturing"].coords["x"]] = None
            self.board[best_capture["captured"].coords["y"]][best_capture["captured"].coords["x"]] = best_capture["capturing"]
            best_capture["capturing"].update_coords(best_capture["captured"].coords["x"], best_capture["captured"].coords["y"])
            best_capture["capturing"].set_unmovable()
            new_x = best_capture["captured"].coords["x"] * self.WIDTH + self.WIDTH // 2
            new_y = best_capture["captured"].coords["y"] * self.WIDTH + self.WIDTH // 2
            self.board_canvas.coords(best_capture["capturing"].id, new_x, new_y)
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
        return can_move(current_piece, new_x, new_y, self.board)

    def on_mouse_release(self, event):
        """
        Handles the event of a mouse release
        """
        if not self.drag_item:
            return
        
        new_x = event.x // self.WIDTH
        new_y = event.y // self.WIDTH
        
        old_x = self.selected_piece.coords["x"]
        old_y = self.selected_piece.coords["y"]

        # getting the current amount of pawns
        remaining_pawns = 0
        for piece in self.player2[:8]:
            if piece.coords["y"] == self.ROWS + self.ADDITIONAL_ROWS -1 and piece.symbol == "♟":
                remaining_pawns += 1
        pawn_allowed = (self.selected_piece.symbol == "♟" and (remaining_pawns > 1 or self.current_round == 15)) or self.selected_piece.symbol != "♟"

        allowed_capture = self.can_capture(new_x, new_y)

        if self.phase == self.PLAYER2_PLACING and self.player2_set[new_x] and new_y == self.ROWS-1 and pawn_allowed:
            # piece has been moved from reserve AND it's not the last pawn before the last round
            self.reserve[old_x] = None
            self.last_moved = self.selected_piece.symbol
            self.selected_piece.update_coords(new_x, new_y)
            self.board[new_y][new_x] = self.selected_piece
            self.player2_set[new_x] = False
            self.phase += 1
            self.turn_button_to_active(self.continue_button)

            self.place_sound.play()

            # centering the new position
            centered_x = new_x * self.WIDTH + self.WIDTH // 2
            centered_y = new_y * self.WIDTH + self.WIDTH // 2
            self.board_canvas.coords(self.drag_item, centered_x, centered_y)
        elif self.phase == self.PLAYER2_CAPTURING and allowed_capture:
            # piece has been moved from board and captures
            captured_piece = self.board[new_y][new_x]
            self.captured.append(captured_piece)
            self.board[new_y][new_x] = None
            self.board_canvas.delete(captured_piece.id)
            captured_piece.id = None

            self.place_sound.play()
            
            self.board[old_y][old_x] = None
            self.board[new_y][new_x] = self.selected_piece
            self.selected_piece.update_coords(new_x, new_y)
            self.selected_piece.set_unmovable()

            # centering the new position
            centered_x = new_x * self.WIDTH + self.WIDTH // 2
            centered_y = new_y * self.WIDTH + self.WIDTH // 2
            self.board_canvas.coords(self.drag_item, centered_x, centered_y)
        else:
            # drag not allowed: set the piece back
            self.board_canvas.coords(self.drag_item,
                    old_x * self.WIDTH + self.WIDTH // 2,
                    old_y * self.WIDTH + self.WIDTH // 2)

        self.drag_item = None
        self.selected_piece = None


class GameSelector(ttk.Frame):
    def __init__(self, master, start_game_callback, language_texts):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")
        self.language_texts = language_texts

        label = ttk.Label(self, text=self.language_texts[1], font=("Arial", 20))
        label.grid(row=0, column=0, pady=10, padx=10)

        chess1_btn = ttk.Button(self, text=self.language_texts[2], command=lambda: start_game_callback("chess1"))
        chess1_btn.grid(row=1, column=0, padx=10, pady=10)
        
        chess2_btn = ttk.Button(self, text=self.language_texts[3], command=lambda: start_game_callback("chess2"))
        chess2_btn.grid(row=2, column=0, padx=10, pady=10)


class LanguageSelector(ttk.Frame):
    def __init__(self, master, update_language):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")

        label = ttk.Label(self, text="Choose your Language", font=("Arial", 20))
        label.grid(row=0, column=0, pady=10, padx=10)

        lang1_btn = ttk.Button(self, text="English", command=lambda: update_language("en"))
        lang1_btn.grid(row=1, column=0, padx=10, pady=10)
        
        lang2_btn = ttk.Button(self, text="Deutsch", command=lambda: update_language("de"))
        lang2_btn.grid(row=2, column=0, padx=10, pady=10)


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Mirror Chess")

        self.style = ttk.Style()
        self.style.colors.set("primary", "#925B39")
        self.style.colors.set("secondary", "#572C12")
        self.style.colors.set("selectfg", "#F4EAE0")
        self.style.configure('TButton', font=('Arial', 15))

        # Ensure the window resizes nicely
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.current_screen = None
        self.language_texts : list[str] = []

        self.show_language_selector()
    
    def update_language(self, language:str) -> None:
        """
        Updates the language
        """
        with open("assets\\languages\\" + language + ".txt", encoding="utf-8") as f:
            self.language_texts = f.read().split("\n-\n")
        self.title(self.language_texts[0])
        self.show_game_selector()
        return

    def clear_screen(self):
        if self.current_screen:
            self.current_screen.destroy()

    def show_language_selector(self):
        self.clear_screen()
        self.current_screen = LanguageSelector(self, self.update_language)
        return

    def show_game_selector(self):
        #self.language = language
        self.clear_screen()
        self.current_screen = GameSelector(self, self.start_game, self.language_texts)
        return

    def start_game(self, game_name:str) -> None:
        self.clear_screen()
        if game_name == "chess1":
            self.current_screen = OriginalMirrorChess(self, self.show_game_selector, self.language_texts)
        elif game_name == "chess2":
            self.current_screen = WiderMirrorChess(self, self.show_game_selector, self.language_texts)
        return


if __name__ == "__main__":
    app = App()
    app.mainloop()