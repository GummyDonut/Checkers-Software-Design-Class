#main
# imports all modules required fr exectution
import pygame._view
import pygame
from source import screen
from source import gameloop
from source import classes
import sys

pygame.init() ## runs pygame

def main():
    win = screen.makewindow(400) ## created the window
    board = gameloop.createBoard(8,8) ## renders the board
    board = gameloop.placePieces(win, board) ## allows the user to place pieces
    game_mode = gameloop.modeSelect(win)    
    gameloop.__run__(win, board, game_mode) ##runs the game consistently
    pygame.quit()
    sys.exit()
    
if __name__ == '__main__':
    main()

## Current Heiarchy

