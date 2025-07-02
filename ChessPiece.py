
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
    def __init__(self, symbol:str, spieler:str, wertung:int=1):
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
    elif figur.symbol == "♜" or figur.symbol == "♛" or figur.symbol == "♚":
        if ((new_x == figur.coords["x"]-1 or new_x == figur.coords["x"]+1) and new_y == figur.coords["y"]) or (new_x == figur.coords["x"] and (new_y == figur.coords["y"]-1 or new_y == figur.coords["y"]+1)):
            return True
    elif figur.symbol == "♝" or figur.symbol == "♛" or figur.symbol == "♚":
        if (new_x == figur.coords["x"]-1 or new_x == figur.coords["x"]+1) and (new_y == figur.coords["y"]-1 or new_y == figur.coords["y"]+1):
            return True
    elif figur.symbol == "♞":
        if ((new_x == figur.coords["x"]-2 or new_x == figur.coords["x"]+2) and (new_y == figur.coords["y"]-1 or new_y == figur.coords["y"]+1)) or ((new_y == figur.coords["y"]-2 or new_y == figur.coords["y"]+2) and (new_x == figur.coords["x"]-1 or new_x == figur.coords["x"]+1)):
            return True
    return False


test= ChessPiece("a", PLAYER2)
if test.coords: print("ja")
else: print("nein")
test.update_coords(3, 4)
if test.coords: print("ja")
else: print("nein")


    
def possible_hits(placement:list, piece:str, row_pos:int, column_pos:int, player:str) -> dict:
    '''
    Shows all possible capturing moves for a given piece (a piece can only move one square at a time)
    placement: current board
    piece: the piece that's being moved
    row_pos: the row of the piece that's being moved (0-1)
    column_pos: the column of the piece that's being moved (0-15)
    player: if it's the player's ('Spieler') or the PC's ('PC') turn
    Output: dict with possible moves in the form {(x, y): [piece, ~player]}
    '''
    hits = {}
    # structure: every possible hit is a dict entry with "(x,y): [Figur, Spieler]", (x,y) being the coordinate of the Figur that can be striked
    if piece == "Bauer": # kann nur nach unten oder oben, nach links oder rechts
        if row_pos == 0 and player == 'PC': # PC, Bauer steht oben
            try:
                if placement[row_pos+1][column_pos-1][1] != player and column_pos-1 >= 0:
                    hits[(row_pos+1, column_pos-1)] = placement[row_pos+1][column_pos-1]
            except:
                pass
            try:
                if placement[row_pos+1][column_pos+1][1] != player:
                    hits[(row_pos+1, column_pos+1)] = placement[row_pos+1][column_pos+1]
            except:
                pass
        if row_pos == 1 and player == 'Spieler': # Spieler, Bauer steht unten
            try:
                if placement[row_pos-1][column_pos-1][1] != player and column_pos-1 >= 0:
                    hits[(row_pos-1, column_pos-1)] = placement[row_pos-1][column_pos-1]
            except:
                pass
            try:
                if placement[row_pos-1][column_pos+1][1] != player:
                    hits[(row_pos-1, column_pos+1)] = placement[row_pos-1][column_pos+1]
            except:
                pass
    elif piece == "Turm": # kann in vier Richtungen gerade
        try:
            if placement[row_pos][column_pos-1][1] != player and column_pos-1 >= 0:
                hits[(row_pos, column_pos-1)] = placement[row_pos][column_pos-1]
        except:
            pass
        try:
            if placement[row_pos][column_pos+1][1] != player:
                hits[(row_pos, column_pos+1)] = placement[row_pos][column_pos+1]
        except:
            pass
        try:
            if placement[row_pos-1][column_pos][1] != player and row_pos-1 >= 0:
                hits[(row_pos-1, column_pos)] = placement[row_pos-1][column_pos]
        except:
            pass
        try:
            if placement[row_pos+1][column_pos][1] != player:
                hits[(row_pos+1, column_pos)] = placement[row_pos+1][column_pos]
        except:
            pass
    elif piece == "Läufer": # kann in vier Richtungen diagonal
        try:
            if placement[row_pos-1][column_pos-1][1] != player and row_pos-1 >= 0 and column_pos-1 >= 0:
                hits[(row_pos-1, column_pos-1)] = placement[row_pos-1][column_pos-1]
        except:
            pass
        try:
            if placement[row_pos-1][column_pos+1][1] != player and row_pos-1 >= 0:
                hits[(row_pos-1, column_pos+1)] = placement[row_pos-1][column_pos+1]
        except:
            pass
        try:
            if placement[row_pos+1][column_pos-1][1] != player and column_pos-1 >= 0:
                hits[(row_pos+1, column_pos-1)] = placement[row_pos+1][column_pos-1]
        except:
            pass
        try:
            if placement[row_pos+1][column_pos+1][1] != player:
                hits[(row_pos+1, column_pos+1)] = placement[row_pos+1][column_pos+1]
        except:
            pass
    elif piece == "Springer": # kann... kompliziert
        try:
            if placement[row_pos-1][column_pos-2][1] != player and row_pos-1 >= 0 and column_pos-2 >= 0:
                hits[(row_pos-1, column_pos-2)] = placement[row_pos-1][column_pos-2]
        except:
            pass
        try:
            if placement[row_pos-1][column_pos+2][1] != player and row_pos-1 >= 0:
                hits[(row_pos-1, column_pos+2)] = placement[row_pos-1][column_pos+2]
        except:
            pass
        try:
            if placement[row_pos+1][column_pos-2][1] != player and column_pos-2 >= 0:
                hits[(row_pos+1, column_pos-2)] = placement[row_pos+1][column_pos-2]
        except:
            pass
        try:
            if placement[row_pos+1][column_pos+2][1] != player:
                hits[(row_pos+1, column_pos+2)] = placement[row_pos+1][column_pos+2]
        except:
            pass
    elif piece == "Dame": # kann in jede Richtung
        try:
            if placement[row_pos-1][column_pos-1][1] != player and row_pos-1 >= 0 and column_pos-1 >= 0:
                hits[(row_pos-1, column_pos-1)] = placement[row_pos-1][column_pos-1]
        except:
            pass
        try:
            if placement[row_pos-1][column_pos+1][1] != player and row_pos-1 >= 0:
                hits[(row_pos-1, column_pos+1)] = placement[row_pos-1][column_pos+1]
        except:
            pass
        try:
            if placement[row_pos+1][column_pos-1][1] != player and column_pos-1 >= 0:
                hits[(row_pos+1, column_pos-1)] = placement[row_pos+1][column_pos-1]
        except:
            pass
        try:
            if placement[row_pos+1][column_pos+1][1] != player:
                hits[(row_pos+1, column_pos+1)] = placement[row_pos+1][column_pos+1]
        except:
            pass
        try:
            if placement[row_pos][column_pos-1][1] != player and column_pos-1 >= 0:
                hits[(row_pos, column_pos-1)] = placement[row_pos][column_pos-1]
        except:
            pass
        try:
            if placement[row_pos][column_pos+1][1] != player:
                hits[(row_pos, column_pos+1)] = placement[row_pos][column_pos+1]
        except:
            pass
        try:
            if placement[row_pos-1][column_pos][1] != player and row_pos-1 >= 0:
                hits[(row_pos-1, column_pos)] = placement[row_pos-1][column_pos]
        except:
            pass
        try:
            if placement[row_pos+1][column_pos][1] != player:
                hits[(row_pos+1, column_pos)] = placement[row_pos+1][column_pos]
        except:
            pass
    elif piece == "König": # kann in jede Richtung
        try:
            if placement[row_pos-1][column_pos-1][1] != player and row_pos-1 >= 0 and column_pos-1 >= 0:
                hits[(row_pos-1, column_pos-1)] = placement[row_pos-1][column_pos-1]
        except:
            pass
        try:
            if placement[row_pos-1][column_pos+1][1] != player and row_pos-1 >= 0:
                hits[(row_pos-1, column_pos+1)] = placement[row_pos-1][column_pos+1]
        except:
            pass
        try:
            if placement[row_pos+1][column_pos-1][1] != player and column_pos-1 >= 0:
                hits[(row_pos+1, column_pos-1)] = placement[row_pos+1][column_pos-1]
        except:
            pass
        try:
            if placement[row_pos+1][column_pos+1][1] != player:
                hits[(row_pos+1, column_pos+1)] = placement[row_pos+1][column_pos+1]
        except:
            pass
        try:
            if placement[row_pos][column_pos-1][1] != player and column_pos-1 >= 0:
                hits[(row_pos, column_pos-1)] = placement[row_pos][column_pos-1]
        except:
            pass
        try:
            if placement[row_pos][column_pos+1][1] != player:
                hits[(row_pos, column_pos+1)] = placement[row_pos][column_pos+1]
        except:
            pass
        try:
            if placement[row_pos-1][column_pos][1] != player and row_pos-1 >= 0:
                hits[(row_pos-1, column_pos)] = placement[row_pos-1][column_pos]
        except:
            pass
        try:
            if placement[row_pos+1][column_pos][1] != player:
                hits[(row_pos+1, column_pos)] = placement[row_pos+1][column_pos]
        except:
            pass
    return hits