# MirrorChess
The game "Mirror Chess"

# To Do
## Visuell / Grafische Oberfläche
- [x] Spielfeld, unterschiedliche Farben für Spieler / PC
- [ ] Texteingabe / Übersicht über eigene Figuren

## Mechanik
- [x] abwechselnde Runden
- [x] Spielstart
- [x] Punkte zählen
- [ ] Verhaltensweise der Figuren ((automatisches) Schlagen)





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