import pygame as p
from chessEngine import GameState
import requests
from time import time

width = height = 550
running = True
MAX_FPS = 60
IMAGES = {}
DIMENSION = 8
SQ_SIZE = height // DIMENSION
url = "http://localhost:5000/"
game = [
    [(6, 4), (4, 4)],
    [(0, 6), (2, 5)],
    [(7, 5), (4, 2)],
    [(0, 1), (2, 2)],
    [(7, 3), (3, 7)],
    [(1, 4), (3, 4)],
    [(3, 7), (1, 5)],
]


try:
    r = requests.get(url + "api/games")
    print(r.json())
except Exception as e:
    print(f"An error occured {e}")


p.init()
screen = p.display.set_mode((width - 4, height + 100))


# creating fen of current chess position
def posToFen(pos):
    notation = {
        "br": "r",
        "bn": "n",
        "bb": "b",
        "bq": "q",
        "bk": "k",
        "bp": "p",
        "wr": "R",
        "wn": "N",
        "wb": "B",
        "wq": "Q",
        "wk": "K",
        "wp": "P",
    }
    FEN_list = []
    for r in range(8):
        count = 0
        FEN_list.append("/")
        for c in range(8):
            if pos[r][c] != "--":
                count = 0
                FEN_list.append(notation[pos[r][c]])

            if (count == 0) & (pos[r][c] == "--"):
                FEN_list.append("0")

            if pos[r][c] == "--":
                count = count + 1
                FEN_list[-1] = str(count)
    # print(FEN_list)
    FEN = ""
    for i in range(len(FEN_list)):
        FEN = FEN + FEN_list[i]
    FEN = FEN[1:]
    # print(FEN)
    return FEN


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
    timeDuration = time()
    global running
    count = 0
    loadImages()
    clock = p.time.Clock()
    p.display.set_caption("Digital Chess Board")
    p.display.set_icon(p.image.load("chessForBoard/images/Icon.png"))
    gs = GameState()
    screen.fill(p.Color("#fffdd0"))
    drawGameState(screen, gs.board)
    try:
        FEN = posToFen(gs.board)
        r = requests.post(
            url + "/api/games",
            {"playerOne": "mann", "playerTwo": "yash", "currentPosition": FEN},
        )
    except Exception as e:
        print(e)
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

        if count < len(game) and time() - timeDuration > 2:
            gs.move(game[count][0], game[count][1])
            count += 1
            timeDuration = time()
            try:
                FEN = posToFen(gs.board)
                print(FEN)
                r = requests.put(url + "/api/games/123", {"currentPosition": FEN})
            except Exception as e:
                print(e)
        screen.fill(p.Color("#fffdd0"))
        drawGameState(screen, gs.board)
        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
