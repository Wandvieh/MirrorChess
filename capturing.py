from GUI import *

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


def actual_hit_pc(placement:list, hits:dict, piece:str, old_row:int, old_col:int):
    '''
    Chooses the best piece to capture for the pc and moves it
    '''
    choices = [item[0] for item in hits.values()]
    if "König" in choices:
        new_row, new_col = list(hits.keys())[choices.index("König")][0], list(hits.keys())[choices.index("König")][1]
    elif "Dame" in choices:
        new_row, new_col = list(hits.keys())[choices.index("Dame")][0], list(hits.keys())[choices.index("Dame")][1]
    elif "Springer" in choices:
        new_row, new_col = list(hits.keys())[choices.index("Springer")][0], list(hits.keys())[choices.index("Springer")][1]
    elif "Turm" in choices:
        new_row, new_col = list(hits.keys())[choices.index("Turm")][0], list(hits.keys())[choices.index("Turm")][1]
    elif "Läufer" in choices:
        new_row, new_col = list(hits.keys())[choices.index("Läufer")][0], list(hits.keys())[choices.index("Läufer")][1]
    else:
        new_row, new_col = list(hits.keys())[choices.index("Bauer")][0], list(hits.keys())[choices.index("Bauer")][1]
    placement[new_row][new_col] = [piece, "PC"]
    placement[old_row][old_col] = ''
    return placement, new_row, new_col

def pc_strike(placement:list, piece:str, row_pos:int, column_pos:int) -> list:
    '''
    Does the actual striking for the PC
    '''
    hits = possible_hits(placement, piece, row_pos, column_pos, 'PC')
    print(hits)
    if len(hits) > 0:
        placement, new_row_pos, new_column_pos = actual_hit_pc(placement, hits, piece, row_pos, column_pos)
        show_field(placement)
        input("Drücke Enter, um fortzufahren")
        placement = pc_strike(placement, piece, new_row_pos, new_column_pos)
    return placement

def actual_hit_player(placement:list, hits:dict, piece:str, old_row:int, old_col:int):
    '''
    Does the actual striking for the player
    hits: dict with a list of possible capturing options
    '''
    print("Du kannst schlagen:", hits)
    choices = [item[0] for item in hits.values()]
    while True:
        inp = input("Welche Figur schlägst du? ")
        if inp not in choices: print("Keine valide Figur!")
        else: break
    new_row, new_col = list(hits.keys())[choices.index(inp)][0], list(hits.keys())[choices.index(inp)][1]
    placement[new_row][new_col] = [piece, "Spieler"]
    placement[old_row][old_col] = ''
    return placement, new_row, new_col

def player_strike(placement:list, piece:str, row_pos:int, col_pos:int) -> list:
    '''
    Utility function to let the player choose which piece to capture
    '''
    hits = possible_hits(placement, piece, row_pos, col_pos, 'Spieler')
    if len(hits) == 0:
        return placement
    placement, new_row_pos, new_col_pos = actual_hit_player(placement, hits, piece, row_pos, col_pos)
    show_field(placement)
    placement = player_strike(placement, piece, new_row_pos, new_col_pos)
    return placement

def check_movable_pieces(placement:list, player:str) -> dict:
    '''
    Checks to see if the player has any more moves they can make
    '''
    movable_pieces = {}
    piece_positions = {}
    # check every piece on the board for whether it's the current player's
    # then check for every piece if it can capture other pieces
    for i in range(2):
        for j in range(16):
            if placement[i][j]:
                if placement[i][j][1] == player:
                    hits = possible_hits(placement, placement[i][j][0], i, j, player)
                    if len(hits) > 0:
                        movable_pieces[placement[i][j][0]] = hits
                        piece_positions[placement[i][j][0]] = (i, j)
    return movable_pieces, piece_positions

def decide_active_piece(movable_pieces:dict, piece_positions:dict) -> tuple [str, int, int]:
    print("Du kannst außerdem folgende Züge machen:", movable_pieces)
    while True:
        inp = input("Welche Figur willst du bewegen? ")
        if inp not in list(movable_pieces.keys()): print("Keine valide Figur!")
        else: break
    return inp, piece_positions[inp][0], piece_positions[inp][1]