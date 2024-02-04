import pyautogui
from PIL import Image
import numpy as np
import colorsys


def extractBoard(image, colors):
    # function to separate the chess board from the rest of the image
    # takes in an image as an input
    # return the b/w numpy array with the chess board separated
    image_arr = np.array(image).astype(np.uint8)
    [rows, cols, _] = image_arr.shape
    imgBW = np.zeros((rows, cols), dtype=np.uint8)

    for i in range(rows):
        for j in range(cols):
            pixelColor = (image_arr[i][j][0], image_arr[i]
                          [j][1], image_arr[i][j][2])
            if (pixelColor in colors):
                imgBW[i][j] = 255
    return imgBW


def extractBoardCoordinates(image_arr):
    # function to get the coordinates of the chess board
    # take in input the b/w numpy array
    # return the 4 coordinates of chess board
    [rows, cols] = image_arr.shape
    x1, x2, y1, y2 = rows, 0, cols, 0
    cnt = 0
    for i in range(rows):
        for j in range(cols):
            if (image_arr[i][j] == 0):
                cnt = 0
            else:
                cnt = cnt + 1
            if (cnt >= 20):
                x1 = min(x1, i)
                x2 = max(x2, i)
    cnt = 0
    for i in range(cols):
        for j in range(rows):
            if (image_arr[j][i] == 0):
                cnt = 0
            else:
                cnt = cnt + 1
            if (cnt >= 20):
                y1 = min(y1, i)
                y2 = max(y2, i)
    return (x1, x2, y1, y2)


def createCoordinateMap(x1, x2, y1, y2):
    # x1, y1 is the top left corner of the chess board
    # the starting square corresponds to a8 on an actual board
    # the pattern goes like -
    ''' a8 b8 c8 ... h8
    a7 b7 c7 ... h7
    .
    .
    .
    a1 b1 c1 ... h1 '''

    coordinatesMap = {}
    squareSize = int((x2 - x1)/8)
    currentSquareLetter = 'a'
    currentSquareNumber = 8
    count = 1

    for i in range(x1, x2):
        for j in range(y1, y2):
            # substracting x1 from i and y1 from j because we want to position our points relative to x1, y1
            # so basically relocating x1 -> 0 and y1 -> 0
            if ((i - x1) % squareSize == 0 and (j - y1) % squareSize == 0):
                # if the coordinates i, j are at the intersection
                if ((i - x1) + int(squareSize/2) < (x2 - x1) and (j - y1) + int(squareSize/2) < (y2 - y1)):
                    # if we have room to mark a coordinate
                    coordinatesMap[str(currentSquareLetter) + str(currentSquareNumber)] = [j + int(squareSize/2), i +
                                                                                           int(squareSize/2)]
                    currentSquareLetter = chr(ord(currentSquareLetter) + 1)
                    count = count + 1
                    if (count == 9):
                        currentSquareNumber = currentSquareNumber - 1
                        currentSquareLetter = 'a'
                        count = 1
    return coordinatesMap


def initializeBoard():
    # pyautogui.sleep(3)
    img = np.array(pyautogui.screenshot()).astype(np.uint8)
    # colors = [(184, 135, 98), (237, 214, 176)]
    colors = [(233, 237, 204), (119, 153, 84)]
    imgBW = extractBoard(img, colors)
    Image.fromarray(imgBW, mode="L").save("outputBW.png")
    x1, x2, y1, y2 = extractBoardCoordinates(imgBW)
    return createCoordinateMap(x1, x2, y1, y2)


def swapCoordinates(coordinateMap):
    for i in range(1, 5):
        for j in range(97, 102):
            a = coordinateMap[str(chr(j)) + str(i)]
            b = coordinateMap[str(
                chr(ord('h') - j + ord('a'))) + str(8 - i + 1)]
            a, b = b, a
    return coordinateMap


def decideColor(coordinateMap):
    screenshot = pyautogui.screenshot().convert('L')
    screenshot.save("ss.png")
    e1 = screenshot.getpixel((coordinateMap["a1"][0], coordinateMap["a1"][1]))
    e8 = screenshot.getpixel((coordinateMap["a8"][0], coordinateMap["a8"][1]))
    print(e1, e8)
    if (e1 > e8):
        return "white"
    else:
        return "black"
