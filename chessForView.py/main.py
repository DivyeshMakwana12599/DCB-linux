import requests
import pygame as p
from requests.api import request

width = height = 550
running = True
MAX_FPS = 60
IMAGES = {}
DIMENSION = 8
SQ_SIZE = height // DIMENSION
url = "http://localhost:5000/"

p.init()
screen = p.display.set_mode((width - 4, height + 100))


# creating position from fen
def fenToPos(fen):
    pos = []
    for _ in range(8):
        p = []
        for _ in range(8):
            p.append("")
        pos.append(p)
    notation = {
        "r": "br",
        "n": "bn",
        "b": "bb",
        "q": "bq",
        "k": "bk",
        "p": "bp",
        "R": "wr",
        "N": "wn",
        "B": "wb",
        "Q": "wq",
        "K": "wk",
        "P": "wp",
    }
    column = 0
    row = 0
    for length in range(len(fen)):
        if not row % 8:
            row = 0
        if fen[length] == "/":
            column += 1
        elif not fen[length].isdigit():
            pos[column][row] = notation[fen[length]]
            row += 1
        elif fen[length].isdigit():
            r = int(fen[length]) + row
            pos[column][row:r] = int(fen[length]) * ["--"]
            row += int(fen[length])
    return pos


pos = fenToPos("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
print(pos)
# blit text to screen
def addText(text, x, y, FONT_SIZE):
    font = p.font.Font("freesansbold.ttf", FONT_SIZE)
    text = font.render(text, True, (0, 0, 0))
    screen.blit(text, (x, y))


# load Images to python
def loadImages():
    pieces = ["br", "bn", "bb", "bq", "bk", "bp", "wr", "wn", "wb", "wq", "wk", "wp"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(
            p.image.load("chessForBoard/images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE)
        )


# Making 2d ChessBoard and displaying Images on it
def drawGameState(screen, pos):
    drawBoard(screen)
    drawPieces(screen, pos)


# Making 2d Chess Board
def drawBoard(screen):
    colors = [p.Color("#f0d9b5"), p.Color("#b58863")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(
                screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            )


# displaying pieces on board according to input screen
def drawPieces(screen, board):
    letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
    numbers = ["8", "7", "6", "5", "4", "3", "2", "1"]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(
                    IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                )
    for i in range(8):
        addText(numbers[i], 0, i * SQ_SIZE, 13)
        addText(letters[i], (i * SQ_SIZE) + SQ_SIZE + 2, height - 18, 13)


def main():
    running = True
    global url, pos
    gameId = input("Enter Game ID: ")
    loadImages()
    print(IMAGES)
    clock = p.time.Clock()
    p.display.set_caption("Digital Chess Board")
    p.display.set_icon(p.image.load("chessForBoard/images/Icon.png"))
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        try:
            r = requests.get(url + "api/games/" + gameId)
            r = r.json()
            pos = fenToPos(r["currentPosition"])
        except Exception as e:
            print(e)
        screen.fill(p.Color("#fffdd0"))
        drawGameState(screen, pos)
        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()