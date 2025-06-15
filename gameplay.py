from tkinter import *
from GUI import *
from capturing import player_strike, pc_strike, check_movable_pieces, decide_active_piece

MOVES = 32

# Spiel intialiisieren: leeres Spielbrett, zwei Spieler mit allen Spielfiguren und keinen geschlagenen Figuren
human_player = {"Figuren": {
    "Bauer": 8, "Turm": 2, "Springer": 2, "Läufer": 2, "Dame": 1, "König": 1
},
           "Punkte": 0}
pc_player = {"Figuren": {
    "Bauer": 8, "Turm": 2, "Springer": 2, "Läufer": 2, "Dame": 1, "König": 1
},
             "Punkte": 0}

placement = [[""]*16, [""]*16]

# Züge: PC startet, nacheinenander, 32 Züge; Setz- und Schlagphase

def pc_move(player, last_move):
    player["Figuren"][last_move] -= 1
    print("PC:", player["Figuren"])
    return last_move

def player_move(player):
    print("Du hast noch", player["Figuren"])
    while True:
        inp = input("Welche Figur setzt du? ")
        if inp not in player["Figuren"].keys(): print("Keine valide Figur!")
        elif player["Figuren"][inp] == 0: print("Du hast davon keine Figuren mehr!")
        elif inp == "Bauer" and player["Figuren"][inp] == 1 and sum(player["Figuren"].values()) > 1: print("Du musst deinen letzten Bauern zum Schluss setzen!")
        else: break
    player["Figuren"][inp] -= 1
    print("Spieler:", player["Figuren"])
    return inp

# Eigenen Score anzeigen
def tally_points(placement):
    player_points, pc_points = 0, 0
    for i in range(2):
        for j in range(16):
            if placement[i][j]:
                if placement[i][j][1] == "Spieler": player_points += 1
                if placement[i][j][1] == "PC": pc_points += 1  
    return player_points - pc_points


last_move = "Bauer"
for i in range(MOVES):
    # Figur setzen
    if i%2==0: # PC
        piece = pc_move(pc_player, last_move)
        placement[i%2][int(i/2)]=[piece, "PC"]
        #txt = "Der PC hat " + piece + " gesetzt."
    else: # Spieler
        piece = player_move(human_player)
        last_move = piece
        placement[i%2][int(i/2)]=[piece, "Spieler"]
        #txt = "Du hast " + piece + " gesetzt."
    #print(placement)
    # Spielfeld zeigen
    show_field(placement)
    input("Drücke Enter, um fortzufahren")
    # Spielfiguren schlagen
    if i%2==0: # PC
        placement = pc_strike(placement, piece, i%2, int(i/2))
    else: # Spieler
        # first he strikes with the current piece
        #placement = player_strike(placement, piece, i%2, int(i/2))
        # then a loop: as long as there is something to strike, you have to choose to do so
        while True:
            movable_pieces, piece_positions = check_movable_pieces(placement, 'Spieler')
            if len(movable_pieces) == 0:
                break
            # player decides on which piece to strike with (and where it's located)
            piece, row, col = decide_active_piece(movable_pieces, piece_positions)
            if piece == 'Skip':
                break
            # player strikes like above
            placement = player_strike(placement, piece, row, col)
            show_field(placement)
            input("Drücke Enter, um fortzufahren")
    show_field(placement)
    input("Drücke Enter, um fortzufahren")
points = tally_points(placement)

print("Du hast", points, "Punkte erhalten!")



