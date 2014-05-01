#draw functions
#The basic

#Changes are indicated by #!!!!!!!!!!!
#NEW CHANGE: added more colour variables
#NEW CHANGE: added code for colour indicators to show when piece is active
#NEW MODULE: modeSelect - set up mode select screen with selection buttons
#NEW MODULE: winScreen - set up win congratulatory screen

##############################################
#CONTROLLER and VIEW DESIGNATION, 
##############################################
import pygame
#command in which starts the game, this is the class in which we first start with
pygame.init() 

grey = (200,200,200)#!!!!!!!!!!!!!
darkgrey = (100,100,100)
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)   #intialization of all colour variables
darkred = (180, 0, 0)#!!!!!!!!!!!!!
blue = (0,0,255)    # and their corresponding RGB values
darkblue = (0,0,180)#!!!!!!!!!!!!
yellow = (255,255,0)
font = pygame.font.SysFont('arial', 14) ## choice of font for words
###############################################################################################################
#Controller and View
def drawBoard(win, board):
#drawing of the board
    for column in board.tile_matrix:
        for tile in column:
            if tile.colour == 'dark': ## associate tile matrix with colours then assigns the appropiate colour 
                colour = black        ## for rendering
            else:
                colour = white
            pygame.draw.rect(win, colour, tile.rect)
##Pieces
    for column in board.piece_matrix:
        for piece in column:
            if piece != None:
                if piece.team == 0:   ## rendering of piece colours and the piece onto the board
                    colour = red
                    #!!!!!!!!!!!!!!!!!!!!!!
                    if piece.state == "active":
                        colour = darkred
                        draw_location = pygame.mouse.get_pos()
                    #!!!!!!!!!!!!!!!!!!!!!!
                else:
                    colour = blue
                    #!!!!!!!!!!!!!!!!!!!!!
                    if piece.state == "active":
                        colour = darkblue
                        draw_location = pygame.mouse.get_pos()
                    #!!!!!!!!!!!!!!!!!!!!!
                if piece.state == "idle":
                    draw_location = (piece.index[0]*50 + 25, piece.index[1]*50 + 25)
                pygame.draw.circle(win, colour, draw_location, 20)
                if piece.ptype == 1:
                    Ktext = font.render("K", True, white)
                    win.blit(Ktext,(piece.index[0]*50 + 25 , \
                                                 piece.index[1]*50 + 25))
###############################################################################################################
#View and contoller- more specifically all the button view changes 
def drawButtons1(win, font, b1, b2, b3, b4): ## rendering of the buttons on the left side of the interface
    ##b1 represents that place RED piece is clicked
    if (b1): 
        button1text = font.render("choose RED piece", True, yellow)
    else:
        button1text = font.render("choose RED piece", True, white)
    ##b2 represents that place BLUE piece is clicked
    if (b2):
        button2text = font.render("choose BLUE piece", True, yellow)
    else:
        button2text = font.render("choose BLUE piece", True, white)
    ##b3 represents that place RED king is clicked
    if (b3):
        button1Ktext = font.render("choose RED king", True, yellow)
    else:
        button1Ktext = font.render("choose RED king", True, white)
    ##b4 represents that place Blue king button is clicked
    if (b4):
        button2Ktext = font.render("choose BLUE king", True, yellow)
    else:
        button2Ktext = font.render("choose BLUE king", True, white)
    ## rnndering if other buttons are clicked
    button3text = font.render("standard board", True, white)
    button3Atext = font.render("force start", True, white)
    buttonLtext = font.render("load game", True, white)
    ## draws simple rectangles for the buttons
    button1 = pygame.Rect([410, 5], [130, 40])
    button2 = pygame.Rect([410, 55], [130, 40])
    button1K = pygame.Rect([410, 105], [130, 40]) ## these are the coordinates
    button2K = pygame.Rect([410, 155], [130, 40])
    button3 = pygame.Rect([410, 205], [130, 40])
    button3A = pygame.Rect([410, 255], [130, 40])
    buttonLoad = pygame.Rect([410, 305], [130, 40])
    
    pygame.draw.rect(win, darkgrey, button1)
    pygame.draw.rect(win, darkgrey, button2)
    pygame.draw.rect(win, darkgrey, button1K) ## this is the actual drawing
    pygame.draw.rect(win, darkgrey, button2K)
    pygame.draw.rect(win, darkgrey, button3)
    pygame.draw.rect(win, darkgrey, button3A)
    pygame.draw.rect(win, darkgrey, buttonLoad)
    
    win.blit(button1text, [button1[0] + 10, button1[1] + 10])
    win.blit(button2text, [button2[0] + 10, button2[1] + 10])
    win.blit(button1Ktext, [button1K[0] + 10, button1K[1] + 10]) ## actual rendering of buttons onto window
    win.blit(button2Ktext, [button2K[0] + 10, button2K[1] + 10])
    win.blit(button3text, [button3[0] + 10, button3[1] + 10])
    win.blit(button3Atext, [button3A[0] + 10, button3A[1] + 10])   
    win.blit(buttonLtext, [buttonLoad[0] + 10, buttonLoad[1] + 10])

def drawButtons2(win, font):
    buttonStext = font.render("save and quit", True, white)
    buttonSave = pygame.Rect([410, 5], [130, 40])
    pygame.draw.rect(win, darkgrey, buttonSave)
    win.blit(buttonStext, [buttonSave[0] + 10, buttonSave[1] + 10])

def drawGameText(win, font, turn):
    blue_text = font.render("Blue's Turn", True, blue)
    red_text = font.render("Red's Turn", True, red)
    if turn == 1:
        win.blit(blue_text, (430,370))
    elif turn == 0:
        win.blit(red_text, (430,370))

#!!!!!!!!!!!!!!!!!!!!!
def modeSelect(win, font):#small function for selection of game mode GUI, more buttoms
    
    win.fill(grey)
    
    PvPtext = font.render("Player vs Player", True, white)
    BPvCtext = font.render("Blue Player vs CPU", True, white)
    RPvCtext = font.render("Red Player vs CPU", True, white)

    PvPbutton = pygame.Rect([100, 50], [350, 95])
    BPvCbutton = pygame.Rect([100, 150], [350, 95])
    RPvCbutton = pygame.Rect([100, 250], [350, 95])

    pygame.draw.rect(win, darkgrey, PvPbutton)
    pygame.draw.rect(win, darkgrey, BPvCbutton)
    pygame.draw.rect(win, darkgrey, RPvCbutton)

    win.blit(PvPtext, (120, 70))
    win.blit(BPvCtext, (120, 170))
    win.blit(RPvCtext, (120, 270))
#!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!
def winScreen(win, team, font,turnCounter):#small function to display winner
    win.fill(grey)
    if team == "invalid":
        raw_text = "A first turn can't be played! :O"
        color = darkred
    else:  
        raw_text = "The " + team + " player wins in "+ str(turnCounter)+ " move(s)!"
        if team == "blue":
            color = blue
        elif team == "red":
            color = red
            
    wintext = font.render(raw_text, True, color)
    win.blit(wintext, (70, 100))
    pygame.display.update()
#!!!!!!!!!!!!!!!!!!!!!
    

        
