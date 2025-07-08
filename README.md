# MirrorChess
The game "Mirror Chess"

# To Do

## v1.2 - Adding a new Game & Reworking the Code
- [ ] Added new game?
- [ ] Reworking the code (no changes, just cleaner code and smaller functions)

## v1.1 - Making Quality of Life Improvements
- [x] QoL Improvements
  - [x] Added a "Rules" Popup
  - [x] Showing the Points on the Game Screen
  - [x] Seeing the PC actually move its pieces
- [x] Visuals
  - [x] More coherent design
  - [x] Added an Icon
- [x] Bugs
  - [x] Corrected movement of Queen and King
  - [ ] Corrected PC capturing behaviour (PC didn't capture on later moves)

## v1.0 - An actual working prototype!
- [x] Bugs
  - [x] Punkte richtig zählen
- [x] Gameplay
  - [x] Der Spieler kann auch mit seinen anderen Figuren schlagen (egal welche Reihenfolge)
  - [x] Man muss nicht schlagen
  - [x] Jede Figur darf in einer Runde nur ein Mal schlagen
- [x] GUI
  - [x] Drag and Drop

## v0.1
### Visuell / Grafische Oberfläche
- [x] Spielfeld, unterschiedliche Farben für Spieler / PC

### Mechanik
- [x] abwechselnde Runden
- [x] Spielstart
- [x] Punkte zählen (jeder Figur ist gleichwertig)
- [x] PC-Schlagen
- [x] Spieler-Schlagen

# Game Modes

- Ideas
  - 3x16 Mirror Chess
  - Chess Rogue-Like




if (pc ist dran): pc_schlagen()

def pc_schlagen():
    - figur die dran ist
    - Spielfeld
    loop:
        positionen, figuren = schlagen_können()
        position, figur = schlagen()
        updaten: spielfeld

def schlagen_können():
    - figur
    - Spielfeld
    if figur = Bauer
        gucken was der bauer schlagen kann
    if figur = könig
        usw.
    return positionen und figuren die geschlagen werden können

def schlagen():
    - figuren
    - positionen
    entweder: wichtigste Figuren schlagen
    bei gleichstand: nach position
    return position, figur