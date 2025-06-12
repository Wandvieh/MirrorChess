from tkinter import *

ROWS = 2
COLUMNS = 16
WIDTH = 100
dimensions = str(COLUMNS*WIDTH) + "x" + str(ROWS*WIDTH*2)
MOVES = 32

root = Tk()
root.geometry(dimensions)

scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)

Label(text="Mirror Chess", font=('Times New Roman', 40)).pack()

canvas = Canvas(root, width=COLUMNS*WIDTH, height=ROWS*WIDTH, bg="white")
canvas.pack(side="top")

# Spiel intialiisieren: leeres Spielbrett, zwei Spieler mit allen Spielfiguren und keinen geschlagenen Figuren
human_player = {"Figuren": {
    "Bauer": 8, "Turm": 2, "Springer": 2, "Läufer": 2, "Dame": 1, "König": 1
},
           "Punkte": 0}
pc_player = {"Figuren": {
    "Bauer": 8, "Turm": 2, "Springer": 2, "Läufer": 2, "Dame": 1, "König": 1
},
             "Punkte": 0}

curr_placement = [[""]*16, [""]*16]

def show_field(placement):
    for i in range(ROWS):
        y = i * WIDTH
        for j in range(COLUMNS):
            x = j * WIDTH
            canvas.create_rectangle(x, y, x+WIDTH, y+WIDTH, fill="white")
            if (placement[i][j]):
                if placement[i][j][1] == "PC": color = "blue"
                else: color = "green"
                canvas.create_text(x + 50, y + 50,fill=color,
                                text=placement[i][j][0], font=('Times New Roman', 20))
    return

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
    return pc_points - player_points

def possible_hits(placement, piece, row_pos, column_pos):
    hits = {}
    # structure: every possible hit is a dict entry with "(x,y): [Figur, Spieler]", (x,y) being the coordinate of the Figur that can be striked
    if piece == "Bauer": # kann nur nach unten, nach links oder rechts
        if row_pos == 0: # nur wenn der Bauer tatsächlich oben steht
            try:
                if placement[row_pos+1][column_pos-1][1] == 'Spieler':
                    hits[(row_pos+1, column_pos-1)] = placement[row_pos+1][column_pos-1]
            except:
                pass
            try:
                if placement[row_pos+1][column_pos+1][1] == 'Spieler':
                    hits[(row_pos+1, column_pos+1)] = placement[row_pos+1][column_pos+1]
            except:
                pass
    elif piece == "Turm": # kann in vier Richtungen gerade
        try:
            if placement[row_pos][column_pos-1][1] == 'Spieler':
                hits[(row_pos, column_pos-1)] = placement[row_pos][column_pos-1]
        except:
            pass
        try:
            if placement[row_pos][column_pos+1][1] == 'Spieler':
                hits[(row_pos, column_pos+1)] = placement[row_pos][column_pos+1]
        except:
            pass
        try:
            if placement[row_pos-1][column_pos][1] == 'Spieler':
                hits[(row_pos-1, column_pos)] = placement[row_pos-1][column_pos]
        except:
            pass
        try:
            if placement[row_pos+1][column_pos][1] == 'Spieler':
                hits[(row_pos+1, column_pos)] = placement[row_pos+1][column_pos]
        except:
            pass
    elif piece == "Läufer": # kann in vier Richtungen diagonal
        try:
            if placement[row_pos-1][column_pos-1][1] == 'Spieler':
                hits[(row_pos-1, column_pos-1)] = placement[row_pos-1][column_pos-1]
        except:
            pass
        try:
            if placement[row_pos-1][column_pos+1][1] == 'Spieler':
                hits[(row_pos-1, column_pos+1)] = placement[row_pos-1][column_pos+1]
        except:
            pass
        try:
            if placement[row_pos+1][column_pos-1][1] == 'Spieler':
                hits[(row_pos+1, column_pos-1)] = placement[row_pos+1][column_pos-1]
        except:
            pass
        try:
            if placement[row_pos+1][column_pos+1][1] == 'Spieler':
                hits[(row_pos+1, column_pos+1)] = placement[row_pos+1][column_pos+1]
        except:
            pass
    elif piece == "Springer": # kann... kompliziert
        try:
            if placement[row_pos-1][column_pos-2][1] == 'Spieler':
                hits[(row_pos-1, column_pos-2)] = placement[row_pos-1][column_pos-2]
        except:
            pass
        try:
            if placement[row_pos-1][column_pos+2][1] == 'Spieler':
                hits[(row_pos-1, column_pos+2)] = placement[row_pos-1][column_pos+2]
        except:
            pass
        try:
            if placement[row_pos+1][column_pos-2][1] == 'Spieler':
                hits[(row_pos+1, column_pos-2)] = placement[row_pos+1][column_pos-2]
        except:
            pass
        try:
            if placement[row_pos+1][column_pos+2][1] == 'Spieler':
                hits[(row_pos+1, column_pos+2)] = placement[row_pos+1][column_pos+2]
        except:
            pass
    elif piece == "Dame": # kann in jede Richtung
        try:
            if placement[row_pos-1][column_pos-1][1] == 'Spieler':
                hits[(row_pos-1, column_pos-1)] = placement[row_pos-1][column_pos-1]
        except:
            pass
        try:
            if placement[row_pos-1][column_pos+1][1] == 'Spieler':
                hits[(row_pos-1, column_pos+1)] = placement[row_pos-1][column_pos+1]
        except:
            pass
        try:
            if placement[row_pos+1][column_pos-1][1] == 'Spieler':
                hits[(row_pos+1, column_pos-1)] = placement[row_pos+1][column_pos-1]
        except:
            pass
        try:
            if placement[row_pos+1][column_pos+1][1] == 'Spieler':
                hits[(row_pos+1, column_pos+1)] = placement[row_pos+1][column_pos+1]
        except:
            pass
        try:
            if placement[row_pos][column_pos-1][1] == 'Spieler':
                hits[(row_pos, column_pos-1)] = placement[row_pos][column_pos-1]
        except:
            pass
        try:
            if placement[row_pos][column_pos+1][1] == 'Spieler':
                hits[(row_pos, column_pos+1)] = placement[row_pos][column_pos+1]
        except:
            pass
        try:
            if placement[row_pos-1][column_pos][1] == 'Spieler':
                hits[(row_pos-1, column_pos)] = placement[row_pos-1][column_pos]
        except:
            pass
        try:
            if placement[row_pos+1][column_pos][1] == 'Spieler':
                hits[(row_pos+1, column_pos)] = placement[row_pos+1][column_pos]
        except:
            pass
    elif piece == "König": # kann in jede Richtung
        try:
            if placement[row_pos-1][column_pos-1][1] == 'Spieler':
                hits[(row_pos-1, column_pos-1)] = placement[row_pos-1][column_pos-1]
        except:
            pass
        try:
            if placement[row_pos-1][column_pos+1][1] == 'Spieler':
                hits[(row_pos-1, column_pos+1)] = placement[row_pos-1][column_pos+1]
        except:
            pass
        try:
            if placement[row_pos+1][column_pos-1][1] == 'Spieler':
                hits[(row_pos+1, column_pos-1)] = placement[row_pos+1][column_pos-1]
        except:
            pass
        try:
            if placement[row_pos+1][column_pos+1][1] == 'Spieler':
                hits[(row_pos+1, column_pos+1)] = placement[row_pos+1][column_pos+1]
        except:
            pass
        try:
            if placement[row_pos][column_pos-1][1] == 'Spieler':
                hits[(row_pos, column_pos-1)] = placement[row_pos][column_pos-1]
        except:
            pass
        try:
            if placement[row_pos][column_pos+1][1] == 'Spieler':
                hits[(row_pos, column_pos+1)] = placement[row_pos][column_pos+1]
        except:
            pass
        try:
            if placement[row_pos-1][column_pos][1] == 'Spieler':
                hits[(row_pos-1, column_pos)] = placement[row_pos-1][column_pos]
        except:
            pass
        try:
            if placement[row_pos+1][column_pos][1] == 'Spieler':
                hits[(row_pos+1, column_pos)] = placement[row_pos+1][column_pos]
        except:
            pass
    return hits

def pc_strike(placement, piece, row_pos, column_pos):
    while True:
        pass
        # get info about which pieces are hittable
        hits = possible_hits(placement, piece, row_pos, column_pos)
        print(hits)
        break
        #if choices == None: break
        # determine which piece to hit
        #placement, new_row, new_column = actual_hit(placement, choices)
    return placement


last_move = "Bauer"
for i in range(MOVES):
    # Figur setzen
    if i%2==0: # PC
        piece = pc_move(pc_player, last_move)
        curr_placement[i%2][int(i/2)]=[piece, "PC"]
        #txt = "Der PC hat " + piece + " gesetzt."
    else: # Spieler
        piece = player_move(human_player)
        last_move = piece
        curr_placement[i%2][int(i/2)]=[piece, "Spieler"]
        #txt = "Du hast " + piece + " gesetzt."
    #print(curr_placement)
    # Spielfeld zeigen
    show_field(curr_placement)
    # Spielfiguren schlagen
    if i%2==0: curr_placement = pc_strike(curr_placement, piece, i%2, int(i/2))
    #else: curr_placement = player_strike(curr_placement, piece, i%2, int(i/2))
points = tally_points(curr_placement)

print("Du hast ", points, "erhalten!")


root.mainloop()


