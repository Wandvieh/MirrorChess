import tkinter as tk

# ----- Spiel-Klassen -----
from Schachspiel import MirrorChess_MirrorMoves



def startbildschirm(root):
    # Erst Fenster leeren
    for widget in root.winfo_children():
        widget.destroy()

    frame = tk.Frame(root)
    frame.pack(pady=100)

    titel = tk.Label(frame, text="Spielauswahl", font=("Arial", 20))
    titel.pack(pady=20)

    schach_button = tk.Button(frame, text="Mirror Chess: Gespiegelte Züge", command=lambda: starte_schach(root))
    schach_button.pack(pady=5)

    # Weitere Spiele hinzufügen:
    # dame_button = tk.Button(frame, text="Dame spielen", command=lambda: starte_dame(root))
    # dame_button.pack(pady=5)

def starte_schach(root):
    for widget in root.winfo_children():
        widget.destroy()
    MirrorChess_MirrorMoves(root)

# def starte_dame(root):
#     for widget in root.winfo_children():
#         widget.destroy()
#     DameGUI(root)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Spielesammlung")
    startbildschirm(root)
    root.mainloop()