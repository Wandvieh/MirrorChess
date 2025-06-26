from tkinter import *

ROWS = 2
COLUMNS = 16
WIDTH = 100
dimensions = str(COLUMNS*WIDTH) + "x" + str(ROWS*WIDTH*2)

root = Tk()
root.geometry(dimensions)

Label(text="Mirror Chess", font=('Times New Roman', 40)).pack()

canvas = Canvas(root, width=COLUMNS*WIDTH, height=ROWS*WIDTH, bg="white")
canvas.pack(side="top")

def show_field(placement:list) -> None:
    '''
    Updates the current playing field
    placement: 16*2 nested list with all current pieces on the board
    '''
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

placement = [[""]*16, [""]*16]
show_field(placement)
inp = input("Pause")

placement = [[["Ja", "Spieler"]]*16, [["Nein", "PC"]]*16]
print(placement)
show_field(placement)
inp = input("Pause")