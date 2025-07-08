import tkinter as tk
PLAYER1 = "PC"
PLAYER2 = "Spieler"


def figuren_erstellen(spieler):
    pieces = []
    for i in range(8):
        pieces.append(ChessPiece("♟", spieler, 1))
    for item in ["♜", "♝", "♞"]:
        for i in range(2):
            pieces.append(ChessPiece(item, spieler, 3))
    pieces.append(ChessPiece("♛", spieler, 5))
    pieces.append(ChessPiece("♚", spieler, 6))
    return pieces
            

class ChessPiece():
    def __init__(self, symbol:str, spieler:str, wertung:int=None):
        if wertung is None: wertung = 1
        self.wertung = wertung # für die auswertung
        self.symbol = symbol # wie das Symbol aussieht
        self.spieler = spieler # obs zum PC oder spieler gehört

        self.ziehbar = True # ob er diese Runde schon bewegt wurde
        self.coords = {} # wo die Figur steht

        if spieler == "PC":
            self.color = "#FFFFFF"
        else:
            self.color = "#000000"

        self.id = None
        return

    def gezogen(self):
        self.ziehbar = False
        return
    
    def neue_runde(self):
        self.ziehbar = True
        return

    def update_coords(self, x, y):
        self.coords = {"x": x, "y": y}
        return
    
def hit_possible(figur:ChessPiece, new_x:int, new_y:int) -> bool:
    if figur.symbol == "♟":
        if figur.spieler == PLAYER1:
            if new_y == figur.coords["y"]+1 and (new_x == figur.coords["x"]-1 or new_x == figur.coords["x"]+1):
                return True
        if figur.spieler == PLAYER2:
            if new_y == figur.coords["y"]-1 and (new_x == figur.coords["x"]-1 or new_x == figur.coords["x"]+1):
                return True
    elif figur.symbol == "♞":
        if ((new_x == figur.coords["x"]-2 or new_x == figur.coords["x"]+2) and (new_y == figur.coords["y"]-1 or new_y == figur.coords["y"]+1)) or ((new_y == figur.coords["y"]-2 or new_y == figur.coords["y"]+2) and (new_x == figur.coords["x"]-1 or new_x == figur.coords["x"]+1)):
            return True
    elif figur.symbol == "♜" or figur.symbol == "♛" or figur.symbol == "♚":
        if ((new_x == figur.coords["x"]-1 or new_x == figur.coords["x"]+1) and new_y == figur.coords["y"]) or (new_x == figur.coords["x"] and (new_y == figur.coords["y"]-1 or new_y == figur.coords["y"]+1)):
            return True
    if figur.symbol == "♝" or figur.symbol == "♛" or figur.symbol == "♚":
        if (new_x == figur.coords["x"]-1 or new_x == figur.coords["x"]+1) and (new_y == figur.coords["y"]-1 or new_y == figur.coords["y"]+1):
            return True
    return False


if __name__ == '__main__':
    PLAYER1 = "PC"
    PLAYER2 = "Spieler"
    canvas_spielfeld = tk.Canvas(width=16*30, height=(2 + 2)*30, bg="white")
    print(canvas_spielfeld.width)

