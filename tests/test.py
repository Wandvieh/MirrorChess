"""placement = [[1, 2, 3, 4, 5, 6, 7, 8], [9, 10, 11, 12, 13, 14, 15, 16]]

print(placement[1])

dct = {(1, 1): ['König', 'Spieler'], (2, 2): ['Bauer', 'Spieler'], (3, 3): ['Bauer', 'Spieler']}

print([item[0] for item in dct.values()])

ROWS = 2
COLUMNS = 16

print([[None for _ in range(COLUMNS)] for _ in range(ROWS)])"""

"""def update_language(language):
    with open("assets\\languages\\" + language + "\\rulesOriginal.txt", encoding="utf-8") as f:
        language_texts = f.read()
    print(language_texts.split("\n-\n")[0])
    print("hier pause")
    print(language_texts.split("\n-\n")[1])
    print("hier pause")
    print(language_texts.split("\n-\n")[2])
    # update the buttons
    return

update_language("de")"""

def knights_moves():
  b = (1, 2)
  for i in range(4):
    b = (-b[0], b[1])
    print(b)
    b = (b[1], b[0])
    print(b)

for i in range(4,2):
  print(i)

#[(1, 2), (-1, 2), (2, -1), (-2, -1), (-1, -2), (1, -2), (-2, 1), (2, 1)]
