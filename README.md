# MirrorChess
The game "Mirror Chess"

# To Do

## v0.1
### Visuell / Grafische Oberfläche
- [x] Spielfeld, unterschiedliche Farben für Spieler / PC

### Mechanik
- [x] abwechselnde Runden
- [x] Spielstart
- [x] Punkte zählen (jeder Figur ist gleichwertig)
- [x] PC-Schlagen
- [x] Spieler-Schlagen

## v0.2
- [x] Bugs
  - [x] Punkte richtig zählen
- [x] Gameplay
  - [x] Der Spieler kann auch mit seinen anderen Figuren schlagen (egal welche Reihenfolge)
  - [x] Man muss nicht schlagen
  - [ ] Jede Figur darf in einer Runde nur ein Mal schlagen
- [ ] GUI
  - [x] Drag and Drop

# Game Modes

- In der Entwicklung
  - Original Mirror Chess (GUI fehlt)
- Ideen
  - 3x16 Mirror Chess
  - Schach Rogue-Like




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