import pygame
import random

WIDTH = 200
HEIGHT = 200
ROWS = int(WIDTH/20)
COLS = int(HEIGHT/20)
WHITE = (255, 255, 255)
BLACK = (0, 0 , 0)
SILVER = (192, 192, 192)
BLOCK_SIZE = 20

def intialGeneration():
    array = []
    for y in range(ROWS):
        col = []
        for x in range(COLS):
            col.append(random.randint(0, 1))
        array.append(col)
    return array

def printGrid(array):
    for y in array:
        print(y)

def drawLiveCell(array):
    gameDisplay.fill(WHITE)

    for y in range(ROWS):
        for x in range(COLS):
            if array[y][x] == 1:
                pygame.draw.rect(gameDisplay, BLACK, [x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE], 0)
            else: 
                pygame.draw.rect(gameDisplay, BLACK, [x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE], 1)

def countNeighbors(row, col, array):
    sumNeighbors = 0
    coordinates = []
    
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
            print(Top, Down)
            sumNeighbors += array[i][j]
    
    sumNeighbors -= array[row][col]

    print("sum:" + str(sumNeighbors))
    return sumNeighbors

def nextGeneration(array):
    newGrid = []
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
            col.append(state)
        newGrid.append(col)
    return newGrid
    
def main():
    global gameDisplay
    pygame.init()
    gameDisplay = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption("Game of Life")

    # Store cell states
    grid = []
    grid = intialGeneration()
    printGrid(grid)

    simulationExit = False
    
    while not simulationExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                simulationExit = True
                    
        drawLiveCell(grid)
        grid = nextGeneration(grid)
        pygame.display.flip()

main()