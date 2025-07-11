# MirrorChess
A chess variant

# To Do

## v1.3 ?
- [ ] 3x16 Mirror Chess
  - [ ] Bugs?
  - [ ] Create a better game?

## v1.2 - Adding a new Game & Reworking the Code
- [x] Added new game: 3x16 (using parent/child classes)
  - [x] board setup
  - [x] PC and Player can set their pieces onto any field on their side they haven't put a piece on before
  - [x] no limitations in regards to the capturing distance (needs more testing)
- [x] Refacturing the code (no changes, just cleaner code and smaller functions. Also making the functions work for other games too)
  - [x] reduced redundancies in checking valid moves
  - [x] English comments and names for better reusability
  - [x] Functions
    - [x] __init__
    - [x] set_attributes
    - [x] draw_board
    - [x] draw_reserve
    - [x] place_reserve
    - [x] rule_popup
    - [x] next_turn
    - [x] turn_button_to_waiting
    - [x] turn_button_to_active
    - [x] pc_turn
    - [x] pc_captures
    - [x] end_game
    - [x] place_piece
    - [x] can_capture
    - [x] on_mouse_press
    - [x] on_mouse_drag
    - [x] on_mouse_release
- [ ] QoL? Nicer gaming experience
  - [ ] Added an icon for the task bar, added more icon resolutions
  - [x] Sound effects when placing pieces
  - [x] Added German and English Language options
- [x] Bugs
  - [x] PC's Knight can't properly capture
  - [x] Pieces are now actually unmovable after having captured with them once

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
  - [x] Corrected PC capturing behaviour (PC didn't capture on later moves)

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

# Ideas

- Game Modes
  - 3x16 Mirror Chess
  - Chess Rogue-Like
  - 2 Spieler Modus (lokal)
- player can choose different materials to place the pieces on (wood, metal, gravel, etc.)
- host on a website?? not with python... :( (what about this: https://pyscript.net/ ?)



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
