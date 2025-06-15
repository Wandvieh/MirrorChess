from tkinter import *

ROWS = 2
COLUMNS = 16
WIDTH = 100
dimensions = str(COLUMNS*WIDTH) + "x" + str(ROWS*WIDTH)
dimensions2 = str(int(COLUMNS*WIDTH)) + "x" + str(int(ROWS*WIDTH))

ws = Tk()
ws.geometry(dimensions2)

Label(text="Mirror Chess", font=('Times New Roman', 40)).pack()

canvas = Canvas(ws, width=COLUMNS*WIDTH, height=ROWS*WIDTH, bg="white")
canvas.pack(side="top")

placement = [[""]*16, [""]*16]
placement[1][3] = "test"
print(placement)

for i in range(ROWS):
    y = i * WIDTH
    for j in range(COLUMNS):
        x = j * WIDTH
        canvas.create_rectangle(x, y, x+WIDTH, y+WIDTH, fill="white")
        if (placement[i][j]):
            canvas.create_text(x + 50, y + 50,
                               text=placement[i][j], font=('Times New Roman', 20))


ws.mainloop()