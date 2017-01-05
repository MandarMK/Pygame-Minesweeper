import pygame
import time
from random import randint

pygame.init()

white = (255,255,255)
grey = (155,155,155)
dgrey =(50, 50, 50)
black=(0,0,0)
dred =(55,0,0)
red = (255,0,0)
dGreen =(0,155,0)
green = (0,255,0)

clock = pygame.time.Clock()

display_width = 800
numBombs = 10
numBlocks = 10
block_width = display_width/numBlocks
FPS = 10

gameDisplay = pygame.display.set_mode((display_width,display_width))
pygame.display.set_caption('Minesweeper')
font = pygame.font.SysFont("monospace", 40)

class Tile:
    def __init__(self):
        self.bomb = False
        self.neighbours  = 10
        self.visible = False
        self.flag = False

#checks if (y,x) is valid
def Valid(x,y):
    if x >= 0 and x < numBlocks and y >= 0 and y < numBlocks:
        return True
    else:
        return False

# Searches and outputs the no of neighbours who have bomb
def SearchNeighbours(y,x):
    sum=0
    checkList=[(1,0),(-1,0),(1,1),(-1,1),(1,-1),(-1,-1),(0,1),(0,-1)]
    for (refY,refX) in checkList:
        if Valid(y + refY,x + refX):
            if grid[y+refY][x+refX].bomb == True:
                sum+=1
    return sum

#Create Grid and set Bombs
grid = [[Tile() for n in range(numBlocks)] for n in range(numBlocks)]

for n in range(numBombs):

    while True:
        x = randint(0,numBlocks-1)
        y = randint(0,numBlocks-1)
        if(grid[y][x].bomb == False):
            grid[y][x].bomb = True
            break

#Get the no on the box
y=0
for row in grid:
    x=0
    for col in row:
        if grid[y][x].bomb == False:
            grid[y][x].neighbours = SearchNeighbours(y,x)
        x+=1
    y+=1

# Note grid initoalization and get corresponding nos has to be done only once

# Search incorporates the actions that have to be done on a click
def Search(y,x):

    if grid[y][x].bomb == True:
        return

    if grid[y][x].visible == True:
        return

    if grid[y][x].neighbours == 10:
        return

    grid[y][x].visible = True
    if grid[y][x].neighbours == 0:
        checkList = [(1, 0), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1), (0, 1), (0, -1)]
        for (refY, refX) in checkList:
            if Valid(y + refY, x + refX):
                Search(y+refY, x + refX)
    return

# Displays caption on screen
def Message_to_User(msg):
    #gameDisplay.fill(white)
    font = pygame.font.SysFont("monospace", 120)
    textSurf = font.render(msg,True, green)
    textRect= textSurf.get_rect()
    textRect.center = [display_width/2,display_width/2 ]
    gameDisplay.blit(textSurf,textRect)
    #pygame.time.delay(1000)

# Actions to do when bomb clicked
def EndGame():
    y = 0
    for row in grid:
        x = 0
        for col in row:
            if grid[y][x].bomb == True:
                grid[y][x].visible = True
            x += 1
        y += 1

    Draw()
    Message_to_User('You Loose')
    pygame.display.update()
    pygame.time.delay(3000)
    pygame.quit()
    quit()

# Counts the no of unexplored blocks
def CountHidden():
    sumH = 0
    y = 0
    for row in grid:
        x = 0
        for col in row:
            if grid[y][x].visible == False:
                 sumH += 1
            x += 1
        y += 1

    return sumH

# Actions after win
def WinGame():
    y = 0
    for row in grid:
        x = 0
        for col in row:
            if grid[y][x].bomb == True:
                grid[y][x].visible = True
            x += 1
        y += 1

    Draw()
    Message_to_User('You WIN!!')
    pygame.display.update()
    pygame.time.delay(3000)
    pygame.quit()
    quit()

# Draws the grid
def Draw():
    y = 0
    for row in grid:
        x = 0
        for col in row:
            if grid[y][x].bomb == True:
                if grid[y][x].visible == True:
                    pygame.draw.rect(gameDisplay, red, [x * block_width, y * block_width, block_width, block_width])
                else:
                    pygame.draw.rect(gameDisplay, dgrey, [x * block_width, y * block_width, block_width, block_width])

            else:
                if grid[y][x].visible == True:
                    pygame.draw.rect(gameDisplay, white, [x * block_width, y * block_width, block_width, block_width])
                else:
                    pygame.draw.rect(gameDisplay, dgrey, [x * block_width, y * block_width, block_width, block_width])
            pygame.draw.rect(gameDisplay, black, [x * block_width, y * block_width, block_width, block_width], 2)

            if grid[y][x].neighbours != 0 and grid[y][x].neighbours != 10 and grid[y][x].visible:
                textSurf = font.render(str(grid[y][x].neighbours), True, black)
                textRect = textSurf.get_rect()
                textRect.center = [x * block_width + block_width / 2, y * block_width + block_width / 2]
                gameDisplay.blit(textSurf, textRect)

            x += 1
        y += 1

    pygame.display.update()

def GameLoop():
    gameOver = False
    while not gameOver:
        gameDisplay.fill(white)

        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONUP:
                mouseX,mouseY = event.pos
                col=int(mouseX/block_width)
                row=int(mouseY/block_width)
                if grid[row][col].bomb == False:
                    if grid[row][col].visible == False:
                        Search(row,col)
                else:
                    EndGame()
        if CountHidden() == numBombs:
            WinGame()
        Draw()
        clock.tick(10)

    gameDisplay.fill(white)
    pygame.quit()
    quit()



GameLoop()