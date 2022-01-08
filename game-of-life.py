import pygame
import random

BLOCK_SIZE = 15
WIDTH = 900
HEIGHT = WIDTH + (BLOCK_SIZE*2)
ROWS = int(WIDTH/BLOCK_SIZE)
COLS = int(WIDTH/BLOCK_SIZE)
WHITE = (255, 255, 255)
BLACK = (0, 0 , 0)
SILVER = (192, 192, 192)
RED = (255, 0 , 0)
FPS = 120

def intialGeneration():
    array = []
    liveCount = 0
    for y in range(ROWS):
        col = []
        for x in range(COLS):
            state = random.randint(0, 1)
            col.append(state)
            if state == 1:
                liveCount += 1
        array.append(col)
    return array, liveCount

def drawCell(array):
    gameDisplay.fill(WHITE)

    for y in range(ROWS):
        for x in range(COLS):
            if array[y][x] == 1:
                pygame.draw.rect(gameDisplay, BLACK, [x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE], 0)
            else: 
                pygame.draw.rect(gameDisplay, BLACK, [x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE], 1)

def countNeighbors(row, col, array):
    sumNeighbors = 0
    
    Top = row - 1
    Down = row + 2
    Left = col - 1
    Right = col + 2

    if Top < 0:
        Top = 0
    if Down >= ROWS:
        Down = ROWS
    if Left < 0:
        Left = 0
    if Right >= COLS:
        Right = COLS
    
    
    for i in range(Top, Down):
        for j in range(Left, Right):
            sumNeighbors += array[i][j]
    
    sumNeighbors -= array[row][col]
    return sumNeighbors

def nextGeneration(array):
    newGrid = []
    liveCount = 0
    for y in range(ROWS):
        col = []
        for x in range(COLS):
            sum = countNeighbors(y, x, array)
            state = array[y][x]
            if state == 1:
                if sum < 2 or sum > 3:
                    state = 0
            elif state == 0:
                if sum == 3:
                    state = 1
            if state == 1:
                liveCount += 1
            col.append(state)
        newGrid.append(col)
    return newGrid, liveCount

def displayStats(genCount, liveCount):
    message = pygame.font.SysFont("arial", BLOCK_SIZE * 2).render("Generation: " + str(genCount) + " Live Cells: " + str(liveCount), True, RED)
    gameDisplay.blit(message, [0, HEIGHT-BLOCK_SIZE*2])

def drawInit():
    for y in range(ROWS):
        for x in range(COLS):
            pygame.draw.rect(gameDisplay, BLACK, [x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE], 1)

    pygame.display.flip()

    drawCell = False
    coordinates = []
    initGen = []

    for y in range(ROWS):
        col = []
        for x in range(COLS):
            col.append(0)
        initGen.append(col) 

    while not drawCell:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    drawCell = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if x % 15 != 0 or y % 15 != 0:
                    x = int(x/15) * 15
                    y = int(y/15) * 15
                    pygame.draw.rect(gameDisplay, BLACK, [x, y, BLOCK_SIZE, BLOCK_SIZE], 0)
                    pygame.display.flip() 
                coordinates.append([x,y])

    for coord in coordinates:
        x = int(coord[0]/15)
        y = int(coord[1]/15)
        initGen[y][x] = 1

    return initGen

def main():
    global gameDisplay
    pygame.init()
    gameDisplay = pygame.display.set_mode([WIDTH, HEIGHT])
    gameClock = pygame.time.Clock()
    pygame.display.set_caption("Game of Life")

    # Counter
    genCount = 0
    liveCount = 0 

    # Store cell states
    grid = []
    grid, liveCount = intialGeneration()

    simulationExit = False
    simulationStart = True

    while not simulationExit:

        while simulationStart:
            gameDisplay.fill(WHITE)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    simulationExit = True
                    pygame.quit()
                    exit()
                if simulationStart:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            simulationExit = True
                            pygame.quit()
                            exit()

                        if event.key == pygame.K_c:
                            grid = drawInit()
                            simulationStart = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                simulationExit = True
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    simulationExit = True
                    exit()
                if event.key == pygame.K_c:
                    main()
        drawCell(grid)
        displayStats(genCount, liveCount)
        grid, liveCount = nextGeneration(grid)
        pygame.display.flip()
        gameClock.tick(FPS)
        genCount += 1

main()