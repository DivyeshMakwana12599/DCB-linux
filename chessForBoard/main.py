import pygame as p
from chessEngine import GameState

width = height = 550
running = True
MAX_FPS = 60
IMAGES = {}
DIMENSION = 8
SQ_SIZE = height // DIMENSION
letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
numbers = ["8", "7", "6", "5", "4", "3", "2", "1"]

p.init()
screen = p.display.set_mode((width - 4, height + 100))


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
    global running
    loadImages()
    clock = p.time.Clock()
    p.display.set_caption("Digital Chess Board")
    p.display.set_icon(p.image.load("chessForBoard/images/Icon.png"))
    screen.fill(p.Color("#fffdd0"))
    gs = GameState()
    drawGameState(screen, gs.board)
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()
