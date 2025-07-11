import tkinter as tk
PLAYER1 = "pc"
PLAYER2 = "player"


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

        if player == "pc":
            self.color = "#FFFFFF"
        elif player == "player":
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
    
def can_move_limited(capturing_piece:ChessPiece, new_x:int, new_y:int) -> bool:
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

def can_move(capturing_piece:ChessPiece, new_x:int, new_y:int, board:list[list[ChessPiece]]) -> bool:
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
    elif capturing_piece.symbol == "♚":
        if ((new_x == capturing_piece.coords["x"]-1 or new_x == capturing_piece.coords["x"]+1) and new_y == capturing_piece.coords["y"]) or (new_x == capturing_piece.coords["x"] and (new_y == capturing_piece.coords["y"]-1 or new_y == capturing_piece.coords["y"]+1)):
            return True
        elif (new_x == capturing_piece.coords["x"]-1 or new_x == capturing_piece.coords["x"]+1) and (new_y == capturing_piece.coords["y"]-1 or new_y == capturing_piece.coords["y"]+1):
            return True
    elif capturing_piece.symbol == "♜" or capturing_piece.symbol == "♛":
        if capturing_piece.coords["y"] == new_y:
            # checking if the new coords are on its line of movement
            # then checking if there is no piece in between
            if new_x > capturing_piece.coords["x"]:
                for i in range(capturing_piece.coords["x"]+1, new_x):
                    if board[new_y][i]: return False
                return True
            elif new_x < capturing_piece.coords["x"]:
                for i in range(new_x+1, capturing_piece.coords["x"]):
                    if board[new_y][i]: return False
                return True
        elif capturing_piece.coords["x"] == new_x:
            # checking if the new coords are on its line of movement
            # then checking if there is no piece in between
            if new_y > capturing_piece.coords["y"]:
                for i in range(capturing_piece.coords["y"]+1, new_y):
                    if board[i][new_x]: return False
                return True
            elif new_y < capturing_piece.coords["y"]:
                for i in range(new_y+1, capturing_piece.coords["y"]):
                    if board[i][new_x]: return False
                return True
    if capturing_piece.symbol == "♝" or capturing_piece.symbol == "♛":
        if capturing_piece.coords["x"] - capturing_piece.coords["y"] == new_x - new_y:
            # checking if the new coords are on its line of movement
            # then checking if there is no piece in between
            difference = new_x - new_y
            if new_x < capturing_piece.coords["x"]:
                for i in range(new_x+1, capturing_piece.coords["x"]):
                    if board[i-difference][i]: return False
                return True
            elif new_x > capturing_piece.coords["x"]:
                for i in range(capturing_piece.coords["x"]+1, new_x):
                    if board[i-difference][i]: return False
                return True
        elif capturing_piece.coords["x"] + capturing_piece.coords["y"] == new_x + new_y:
            # checking if the new coords are on its line of movement
            # then checking if there is no piece in between
            sum = new_x + new_y
            if new_x < capturing_piece.coords["x"]:
                for i in range(new_x+1, capturing_piece.coords["x"]):
                    if board[sum-i][i]: return False
                return True
            elif new_x > capturing_piece.coords["x"]:
                for i in range(capturing_piece.coords["x"]+1, new_x):
                    if board[sum-i][i]: return False
                return True
    return False



if __name__ == '__main__':
    piece = ChessPiece("♜", "pc", 3)
    piece.update_coords(3,3)
    board = [[None for _ in range(7)] for _ in range(7)]
    board[0][2] = piece
    board[2][2] = ChessPiece("♝", "pc", 3)
    board[3][2] = ChessPiece("♝", "pc", 3)
    print(can_move(piece, 2,3, board))

