import tkinter as tk
PLAYER1 = "PC"
PLAYER2 = "Spieler"


def create_player(player):
    pieces = []
    for i in range(8):
        pieces.append(ChessPiece("♟", player, 1))
    for item in ["♜", "♝", "♞"]:
        for i in range(2):
            pieces.append(ChessPiece(item, player, 3))
    pieces.append(ChessPiece("♛", player, 5))
    pieces.append(ChessPiece("♚", player, 6))
    return pieces
            
class ChessPiece():
    def __init__(self, symbol:str, player:str, score:int=None) -> None:
        """
        Creates a chess piece with a symbol (the kind of piece), a score (how many points it adds when captured) and a corresponding player ("PC" or sth else)
        """
        if score == None: score = 1
        self.score = score # for the final score
        self.symbol = symbol # which chess piece it is
        self.player = player # obs zum PC oder spieler gehört

        self.movable = True # if it has been moved this round
        self.coords = {} # where the piece is on the field; empty if it is not on the field

        if player == "PC":
            self.color = "#FFFFFF"
        else:
            self.color = "#000000"

        self.id = None
        return

    def set_unmovable(self) -> None:
        self.movable = False
        return
    
    def set_movable(self) -> None:
        self.movable = True
        return

    def update_coords(self, x, y) -> None:
        self.coords = {"x": x, "y": y}
        return
    
    def get_possible_capture_moves(self) -> list:
        return []
    
def can_move(capturing_piece:ChessPiece, new_x:int, new_y:int) -> bool:
    if capturing_piece.symbol == "♟":
        if capturing_piece.player == PLAYER1:
            # Player1 is always starting at the top
            if new_y == capturing_piece.coords["y"]+1 and (new_x == capturing_piece.coords["x"]-1 or new_x == capturing_piece.coords["x"]+1):
                return True
        if capturing_piece.player == PLAYER2:
            # Player2 is always starting at the bottom
            if new_y == capturing_piece.coords["y"]-1 and (new_x == capturing_piece.coords["x"]-1 or new_x == capturing_piece.coords["x"]+1):
                return True
    elif capturing_piece.symbol == "♞":
        if ((new_x == capturing_piece.coords["x"]-2 or new_x == capturing_piece.coords["x"]+2) and (new_y == capturing_piece.coords["y"]-1 or new_y == capturing_piece.coords["y"]+1)) or ((new_y == capturing_piece.coords["y"]-2 or new_y == capturing_piece.coords["y"]+2) and (new_x == capturing_piece.coords["x"]-1 or new_x == capturing_piece.coords["x"]+1)):
            return True
    elif capturing_piece.symbol == "♜" or capturing_piece.symbol == "♛" or capturing_piece.symbol == "♚":
        if ((new_x == capturing_piece.coords["x"]-1 or new_x == capturing_piece.coords["x"]+1) and new_y == capturing_piece.coords["y"]) or (new_x == capturing_piece.coords["x"] and (new_y == capturing_piece.coords["y"]-1 or new_y == capturing_piece.coords["y"]+1)):
            return True
    if capturing_piece.symbol == "♝" or capturing_piece.symbol == "♛" or capturing_piece.symbol == "♚":
        if (new_x == capturing_piece.coords["x"]-1 or new_x == capturing_piece.coords["x"]+1) and (new_y == capturing_piece.coords["y"]-1 or new_y == capturing_piece.coords["y"]+1):
            return True
    return False



if __name__ == '__main__':
    PLAYER1 = "PC"
    PLAYER2 = "Spieler"
    canvas_spielfeld = tk.Canvas(width=16*30, height=(2 + 2)*30, bg="white")
    print(canvas_spielfeld.width)

