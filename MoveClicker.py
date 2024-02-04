import pyautogui


def makeMove(coordinateMap, scraper, i):
    # play the move and wait for the move to happen on board then give back control
    # make use of scraper object
    frm, to = i.split(" ")
    pyautogui.click(coordinateMap[frm])
    pyautogui.click(coordinateMap[to])
    scraper.cnt = scraper.cnt + 1
    return False
