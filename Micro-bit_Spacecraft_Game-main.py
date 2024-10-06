from microbit import *
from random import randint
import music
import gc


# SETTINGS #
asteroidDensity = 3  # sets the possibility of an asteroid inversely
loopTime = 10  # refresh time of the game logic (<> game speed)
gameSpeed = 600  # defines the start speed of the game 1000 = 1s
nextLvlAt = 20    # game steps per level


# VARIABLES #
bJustStarted = True
grid = []
bYouLose = False
lvl = 1
stpsUntlNxtLvl = nextLvlAt
stpsUntlNxtRfrsh = 0
currentGameSpeed = gameSpeed


# FUNCTIONS #
def getStepsUntilNextRefresh():
    global loopTime
    global currentGameSpeed
    return int((currentGameSpeed / loopTime))


def drawGrid():
    global bYouLose
    if (len(grid) > 0):
        # if an asteroid collides with the ship then the game is lost
        if (grid[4][4]):
            bYouLose = True
        # draw the grid with the center 5 cols
        for row in range(0, len(grid)):
            for col in range(2, len(grid[row])-2):
                isOn = 0
                if (grid[row][col] or (row == 4 and col == 4)):
                    isOn = 7
                display.set_pixel(col-2, row, isOn)


def is_On():
    ret = True
    # if the randomint is true X times then the pixel is on
    for i in range(0, asteroidDensity):
        rnd = randint(0, 1)
        if (rnd == 0):
            ret = False
            break
    return ret


def createRow():
    cols = []
    # go for all 9 pixels in row
    # (5 for the grid and 2 on every side for memory)
    for i in range(0, 9):
        isOn = is_On()
        cols.append(isOn)
    return cols


def buildGrid():
    global stpsUntlNxtLvl
    global currentGameSpeed
    global lvl
    # if start of game -> build empty grid
    if (len(grid) == 0):
        for i in range(0, 5):
            grid.append([False for i in range(0, 9)])
    # if grid is already built, delete last row and create new one at the top
    else:
        grid.pop(4)
        grid.insert(0, createRow())
    # draw grid
    drawGrid()
    # count steps and increase difficulty
    stpsUntlNxtLvl -= 1
    if (stpsUntlNxtLvl == 0):
        if ((currentGameSpeed - 100) > 100):  # until 200
            currentGameSpeed -= 100
        elif ((currentGameSpeed - 20) > 20):  # until 20
            currentGameSpeed -= 20
        if (currentGameSpeed > 20):
            stpsUntlNxtLvl = nextLvlAt
            lvl += 1
            # level increase effect
            music.play(music.POWER_UP, wait=False)
            display.show(Image.ARROW_N)
            sleep(250)
            display.clear()
            sleep(250)
            display.show(Image.ARROW_N)
            sleep(250)
            display.clear()
            sleep(500)
            drawGrid()


def shiftLeft():
    for row in range(0, len(grid)):
        grid[row].pop(8)
        grid[row].insert(0, is_On())


def shiftRight():
    for row in range(0, len(grid)):
        grid[row].pop(0)
        grid[row].append(is_On())


# GAME LOOP #
stpsUntlNxtRfrsh = getStepsUntilNextRefresh()
while True:
    if (bJustStarted):
        bJustStarted = False
        gc.enable()
        display.scroll("SPACECRAFT", delay=85)
        sleep(500)
        for i in range(3, 0, -1):
            display.show(str(i))
            sleep(1000)
    elif (bYouLose):
        music.play(music.POWER_DOWN, wait=False)
        display.clear()
        if(lvl == 1 or lvl == 2): 
            display.show(Image.MEH)
        if(lvl == 3 or lvl == 4):
            display.show(Image.SURPRISED)
        if(lvl == 5 or lvl == 6):
            display.show(Image.HAPPY)
        if(lvl == 7 or lvl == 8):
            display.show(Image.SILLY)
        if(lvl == 9 or lvl >= 10):
            display.show(Image.FABULOUS)
        sleep(1000)
        display.scroll("YOU DIED AT LEVEL " + str(lvl) + "!", delay=85)
        bJustStarted = False
        grid = []
        bYouLose = False
        lvl = 1
        stpsUntlNxtLvl = nextLvlAt
        stpsUntlNxtRfrsh = 0
        currentGameSpeed = gameSpeed
        for i in range(3, 0, -1):
            display.show(str(i))
            sleep(1000)
        gc.collect()    
    else:
        if (len(grid) > 0):
            if (button_a.was_pressed()):
                shiftLeft()
                drawGrid()
            if (button_b.was_pressed()):
                shiftRight()
                drawGrid()
        if (stpsUntlNxtRfrsh == 0):
            buildGrid()
            stpsUntlNxtRfrsh = getStepsUntilNextRefresh()
        stpsUntlNxtRfrsh -= 1
        sleep(loopTime)
