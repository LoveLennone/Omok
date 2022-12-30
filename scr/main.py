import pygame as p

import gameState
import qlearningAgents
import multiAgents
from StonePiece import StonePiece
from time import time, sleep

WIDTH = 600
HEIGHT = 600
DIMENSION = 13
SQ_SIZE = HEIGHT / (DIMENSION-1)
MAX_FPS = 15
IMAGES = {}

# load images 1 time. Reloading images is taxing

def load_images():
    # access image by IMAGES['wp']
    pieces = ['bC', 'wC']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(
            p.image.load("C:/Users/ukhye/Desktop/Foundation of AI_CS5100/Project/CS5001_omokAIProject/resources/" + piece + ".png"),
            (SQ_SIZE, SQ_SIZE))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = gameState.GameState(dimension=DIMENSION-2)
    qa = qlearningAgents.ApproximateQAgent(alpha=0.5, dimension=DIMENSION-2)
    load_images()
    
    sqSelected = ()
    start_time = time()

    for i in range(0):    
        studying = 1
        explore_rate = 0.7 - (i * 0.05)
        qa.explorationProb(explore_rate)
        
        while studying:
            prev_gs = gs.deepCopy()
            action = qa.getAction(gs)
            row, col = action
            #print(row, col, gs.getPlayerTurn())    
            gs.updatePlayerTurn(row, col)

            if gs.is_gameOver(row, col, gs.getColor(row, col)) == True :
                if gs.player_turn >= gs.dimension * gs.dimension: # Draw
                    #print(gs)
                    qa.update(prev_gs, action, gs, 10)
                elif gs.getColor(row, col) == 'white': # WIN
                    qa.update(prev_gs, action, gs, 100)
                else:
                    qa.update(prev_gs, action, gs, -100) # LOSE
                gs.reset()
                studying += 1
            else:
                qa.update(prev_gs, action, gs, 0)

            if studying > 30: # TBD: How long are you studying?
                studying = 0

        print(gs.win_history, "Please wait. Now learning...", i+1, "/ 100")
        gs.win_history = [0, 0, 0]

    print("Finish learning. Time elapsed: ", time() - start_time)
    qa.explorationProb(0)
    gs.win_history = [0, 0, 0]

    # Play mode
    while True: 
        cmd = input("Ready to play? (1: Human vs RL, 2: Human vs MinMax, 3: RL vs MinMax, 4: Quit) ")
        start_time = time()
        
        if cmd == '1':
            running = 1
            agent = qa
            gs.reset()
        elif cmd == '2':
            running = 2
            gs.reset()
            agent = multiAgents.AlphaBetaAgent(depth = 2, dimension= DIMENSION-2)
        elif cmd == '3':
            running = 3
            gs.win_history = [0, 0, 0]
            gs.reset()
            ma = multiAgents.AlphaBetaAgent(depth = 2, dimension= DIMENSION-2)
            ngames = int(input("How many times you want to run games for RL vs MinMax? "))
        else:
            break

        while running > 0:
            prev_gs = gs.deepCopy()

            if running == 3:  # AI mode
                
                if gs.getPlayerTurn() % 2 == 0 : # RL turn                  
                    agent = qa
                else:
                    agent = ma

                action = agent.getAction(gs)
                col, row = action
                gs.updatePlayerTurn(col, row)
                #print(col, row, gs.getPlayerTurn())

                if gs.is_gameOver(col, row, gs.getColor(col, row)) == True:
                    if ngames <= 1:
                        running = False

                    if gs.getPlayerTurn() >= gs.dimension * gs.dimension: # Draw
                        qa.update(prev_gs, action, gs, -1)
                    elif gs.getPlayerTurn() % 2 == 0 : # RL turn 
                        qa.update(prev_gs, action, gs, 100)
                    else:
                        qa.update(prev_gs, action, gs, -100) # LOSE

                    #print(gs)
                    ngames -= 1
                    print(gs.win_history)
                    #print(gs.win_history, "Please wait. Now learn with Minmax...", ngames, "trial left.")
                    gs.reset()

                else:
                    qa.update(prev_gs, action, gs, 0)

                #print(gs)

            else : # Player mode
                
                if gs.getPlayerTurn() % 2 == 0 : # AI turn
                    start_time_mm = time()
                    action = agent.getAction(gs)
                    col, row = action
                    gs.updatePlayerTurn(col, row)
                    print(col, row, gs.getPlayerTurn())
                    print(gs)
                    print("Time elapsed: ", time() - start_time_mm)

                else :  # Your turn
                    for e in p.event.get():
                        if e.type == p.QUIT:
                            running = False

                        elif e.type == p.MOUSEBUTTONDOWN:
                            location = p.mouse.get_pos()  # tracks mouse xy
                            print(location)
                            row = int((location[0] - SQ_SIZE * .5) // SQ_SIZE)
                            col = int((location[1] - SQ_SIZE * .5) // SQ_SIZE)

                            if gs.checkLocation(col, row, DIMENSION) == False:
                                print("Error: Wrong place!", col, row)
                                continue

                gs.updatePlayerTurn(col, row)
                
                if gs.is_gameOver(col, row, gs.getColor(col, row)) == True:         
                    running = False
                
                if gs.getPlayerTurn() >= gs.dimension * gs.dimension: # Draw
                    qa.update(prev_gs, action, gs, -1)
                elif gs.getPlayerTurn() % 2 == 0 : # RL turn 
                    qa.update(prev_gs, action, gs, 100)
                else:
                    qa.update(prev_gs, action, gs, -100) # LOSE               
                
            drawGameState(screen, gs, sqSelected)
            clock.tick(MAX_FPS)
            black = (0, 0, 0)
            myFont = p.font.SysFont("Times New Roman", 26)
            player = ''
            if gs.getPlayerTurn() % 2 == 0:
                player = 'black'
            if gs.getPlayerTurn() % 2 == 1:
                player = 'white'

            player_display = myFont.render(player, 1, black)
            screen.blit(player_display, (200, 220))
            p.display.flip()

        print("Game Over. Time elapsed: ", time() - start_time)


def drawGameState(screen, gs, sqSelected):
    drawBoard(screen)
    drawPieces(screen, gs.matrix)

    highlight = gs.get_highlight_switch()

    if highlight == 1:
        if sqSelected == ():
            drawBoard(screen)
            drawPieces(screen, gs.matrix)

        else:
            r = sqSelected[0]
            c = sqSelected[1]
            p.draw.rect(screen, 'green', p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            piece = gs.matrix[r][c]
            screen.blit(IMAGES[piece.get_image_name()], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawBoard(screen):

    line_thickness = 2
    p.draw.rect(screen, 'brown', p.Rect(0, 0, WIDTH, HEIGHT))
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            p.draw.rect(screen, 'black', p.Rect(c * SQ_SIZE, r * SQ_SIZE, line_thickness, SQ_SIZE))
            p.draw.rect(screen, 'black', p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, line_thickness))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != 0:
                screen.blit(IMAGES[piece.get_image_name()], p.Rect((c * SQ_SIZE)+SQ_SIZE/2, (r * SQ_SIZE)+SQ_SIZE/2, SQ_SIZE, SQ_SIZE))

main()

