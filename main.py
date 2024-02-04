from Scraper import Scraper
from BoardSetup import initializeBoard, decideColor, swapCoordinates
from MoveClicker import makeMove
import time

currentColor = "white"
coordinateMap = {}
moves = []
threadStatus = None
quitStatus = False


def main(currentColor, coordinateMap, moves, threadStatus, quitStatus):
    scraper = Scraper(moves)
    scraper.login()
    scraper.startGameSession()
    scraper.resizeWindow()
    scraper.scrollToTop()

    coordinateMap = initializeBoard()

    scraper.setTimeControls()  # use default values RN like 900|10, 60|0, etc
    scraper.startGame()
    scraper.waitForGameStart()
    time.sleep(1)
    print("deciding color")
    color = decideColor(coordinateMap)

    if (currentColor != color):
        coordinateMap = swapCoordinates(coordinateMap)
        currentColor = color

    if (color == "white"):
        threadStatus = True
    else:
        threadStatus = False

    while True:
        if (threadStatus):
            i = input("Enter your move: ").lower().strip()
            if (i == "r"):
                coordinateMap = initializeBoard()
                print(coordinateMap)
            else:
                threadStatus = makeMove(coordinateMap, scraper, i)
        else:
            threadStatus = scraper.readMoves(color)


if (__name__ == "__main__"):
    main(currentColor, coordinateMap, moves, threadStatus, quitStatus)
