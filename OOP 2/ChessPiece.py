


def figuren_erstellen(spieler):
    pieces = []
    for i in range(8):
        bauer = ChessPiece("♟", spieler)
        pieces.append(bauer)
    for i in range(8,10):
        turm = ChessPiece("♜", spieler)
        pieces.append(turm)
    for i in range(8,10):
        laeufer = ChessPiece("♝", spieler)
        pieces.append(laeufer)
    for i in range(8,10):
        springer = ChessPiece("♞", spieler)
        pieces.append(springer)
    dame = ChessPiece("♛", spieler)
    pieces.append(dame)
    könig = ChessPiece("♚", spieler)
    pieces.append(könig)
    return pieces
            

class ChessPiece():
    def __init__(self, symbol, spieler):
        self.wertung = 1 # für die auswertung
        self.symbol = symbol # wie das Symbol aussieht
        self.spieler = spieler # obs zum PC oder spieler gehört

        self.ziehbar = True # ob er diese Runde schon bewegt wurde
        self.coords = {} # wo die Figur steht

        if spieler == "PC":
            self.color = "#FFFFFF"
        else:
            self.color = "#000000"

        self.id = None

    def gezogen(self):
        self.ziehbar = False
    
    def neue_runde(self):
        self.ziehbar = True

    def update_coords(self, x, y):
        self.coords = {"x": x, "y": y}
    
