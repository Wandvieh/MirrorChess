import tkinter as tk
from test_tkinter_games import first_game, second_game

def first_game(window):
    global root
    root.withdraw()

    window = tk.Toplevel(root)
    tk.Label(window, text="Spiel 1", font=('Calibri', 40)).pack()
    # Und wenns fertig ist, wieder zurück
    tk.Button(window, text="Zurück zum Menü", font=('Calibri'), command=menu).pack()
    return

def second_game(window):
    global root
    # Und wenns fertig ist, wieder zurück
    return

root = tk.Tk()
root.geometry("500x300")

def menu():
    global root
    root.withdraw()
    menu_proper()

def menu_proper():
    global root
    window = tk.Frame(root)
    tk.Label(window, text="Spielauswahl", font=('Calibri', 40)).pack()
    tk.Button(window, text="Spielvariante 1", font=('Calibri'), command=lambda: first_game("1")).pack()
    tk.Button(window, text="Spielvariante 2", font=('Calibri'), command=lambda: second_game).pack()
    window.pack()
    return

menu_proper()

root.mainloop()