from typing import Union

import pygame as p
import serial
import serial.tools.list_ports
from Chess import ChessEngine
import time


WIDTH = HEIGHT = 550
p.init()

screen = p.display.set_mode((WIDTH - 4, HEIGHT + 100))
connected = False


# serial board connection
def get_ports():
    ports = serial.tools.list_ports.comports()
    return ports


def findBoard(portsFound):
    commPort = "None"
    numConnection = len(portsFound)

    for i in range(0, numConnection):
        port = foundPorts[i]
        strPort = str(port)

        if "USB" in strPort:
            splitPort = strPort.split(" ")
            commPort = splitPort[0]

    return commPort


foundPorts = get_ports()
connectPort = findBoard(foundPorts)

if connectPort != "None":
    ser = serial.Serial(connectPort, baudrate=9600, timeout=1)
    print("Connected to " + connectPort)
    time.sleep(2)
    connected = True
else:
    print("Board not Connected!")
    connected = False

# diffrent parameters of screen
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
numbers = ["8", "7", "6", "5", "4", "3", "2", "1"]


# load Images to Python
def loadImages():
    pieces = ["br", "bn", "bb", "bq", "bk", "bp", "wr", "wn", "wb", "wq", "wk", "wp"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(
            p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE)
        )


# blit text to screen
def addText(text, x, y, FONT_SIZE):
    font = p.font.Font("freesansbold.ttf", FONT_SIZE)
    text = font.render(text, True, (0, 0, 0))
    screen.blit(text, (x, y))


# Making 2d ChessBoard and displaying Images on it
def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)


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
        addText(letters[i], (i * SQ_SIZE) + SQ_SIZE + 2, HEIGHT - 18, 13)


# read line from Serial port
def getData():
    data = ser.readline().decode("ascii")
    return data


# read chess string from microcontroller through serial port
def readFromBoard():
    pos = {}
    ser.write(b"1")
    for i in range(8):
        pos[i] = getData()
        print(pos[i])

    print(pos)

    temp = []

    for i in range(8):
        temp.append(
            [
                pos[i][0],
                pos[i][1],
                pos[i][2],
                pos[i][3],
                pos[i][4],
                pos[i][5],
                pos[i][6],
                pos[i][7],
            ]
        )
    print(temp)
    format = {
        "r": "br",
        "k": "bn",
        "b": "bb",
        "q": "bq",
        "a": "bk",
        "p": "bp",
        "R": "wr",
        "K": "wn",
        "B": "wb",
        "Q": "wq",
        "A": "wk",
        "P": "wp",
        " ": "--",
    }
    for i in range(8):
        for j in range(8):
            temp[i][j] = format[temp[i][j]]
    print(temp)
    return temp


# creating fen of current chess position
def printFen(gs):
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
    pos = gs.board
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
    print(FEN)
    addText(FEN, 10, HEIGHT, 15)


# main
def main():
    p.display.set_caption("Digital Chess Board")
    icon = p.image.load("images/Icon.png")
    p.display.set_icon(icon)
    clock = p.time.Clock()
    screen.fill(p.Color("#fffdd0"))
    gs = ChessEngine.GameState()
    loadImages()
    if connected == True:
        gs.board = readFromBoard()
    running = True
    drawGameState(screen, gs)
    printFen(gs)
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        clock.tick(MAX_FPS)
        p.display.flip()


# making this as main file
if __name__ == "__main__":
    main()
