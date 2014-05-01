#gameloop

#Changes are indicated with #!!!!!!!!!!!!!!!!!!!!!
#
#NEW CHANGE: added turn counter
#NEW CHANGE: imported new class AI
#NEW CHANGE: added an additional display update
#NEW CHANGE: added CPU AI turn behaviour
#NEW CHANGE: added piece movement and alternating turn logic
#NEW CHANGE: added win condition and display logic
#NEW FUNCTION: modeSelect - gamemode selection based on mouseclick


#MODEL IMPLEMENTATION
import pygame
import sys
import random
from source import classes
from source import draw
from source import save
from source import AI #!!!!!!!!!!!!!!!!!!!!!
pygame.init()# method in which we start the game

grey = (200,200,200)
white = (255,255,255) # variable RGB colour declarations
red = (255,0,0)

small_font = pygame.font.SysFont('arial', 14) #font choice
big_font = pygame.font.SysFont('arial', 35)
def __run__(win, board, game_mode):
    turnCounter = 0 #!!!!!!!!!!!!!!!!!!!!!
    print "playing", game_mode
    running = True
    chaining = False #this variable is used for chaining kills
    moving = False
    if game_mode == "BPvC": #sets CPU to a team based on game mode selected
        cpu_team = 0
    elif game_mode == "RPvC":
        cpu_team = 1
    else:
        cpu_team = 2
    possible_moves = AI.allPossibleMoves(board, board.turn) #gets the array of Move classes for all possible moves
    while running:


        #drawing
        win.fill(grey) 
        draw.drawBoard(win, board) ## function calls the draw module several times
        draw.drawButtons2(win, small_font)
        draw.drawGameText(win, small_font, board.turn)

        #display update
        pygame.display.update() #!!!!!!!!!!!!!!!!!!!!!
 
        #!!!!!!!!!!!!!!!!!!!!!
        #turn logic for computer
        #computer randomly selects a Move class from the array of all possible moves, and executes
        if (cpu_team == board.turn):
            pygame.time.wait(250)
            ran = random.random()
            if (turnCounter != 0):
                ran_seed = int(ran*len(possible_moves))
                ran_move = possible_moves[ran_seed]
                moving_piece = ran_move.moving_piece
                new_index = ran_move.new_index
                moving = True
        #!!!!!!!!!!!!!!!!!!!!!
            
        #event handler
        mpos = pygame.mouse.get_pos()
        mouse_index = [int(mpos[0]/50), int(mpos[1]/50)]
        event = pygame.event.poll()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mouse_index[0] > 7: #if click is in button domain
                if mouse_index[1] < 1:
                    save.saveGame(board.piece_matrix)
                    pygame.quit()
                    sys.exit()
            else: #if click is on board
                holding = True
                selected_piece = board.piece_matrix[mouse_index[0]][mouse_index[1]]
                if selected_piece != None:
                    selected_piece.state = "active"
            
        elif event.type == pygame.MOUSEBUTTONUP:
            holding = False
            try:
                selected_piece.state = "idle"
            except UnboundLocalError:
                continue
            except AttributeError:
                continue
            if mouse_index[0] <= 7:
                moving_piece = selected_piece
                new_index = mouse_index
                moving = True
            
        if event.type == pygame.QUIT:
            running = False

        #!!!!!!!!!!!!!!!!!!!!!
        #move logic
        if moving:
            for move in possible_moves:
                if AI.isSame(move, moving_piece, new_index):#checks if move is a possible move
                    board.move(move)
                    if move.kill: #if the move is a kill, check for additional chaining kills
                        chain_moves = AI.possibleMoves(move.moving_piece, board, board.turn)
                        possible_moves = [] #reset possible moves array and ready to add all possible chaining kills
                        for move in chain_moves:
                            if move.kill:
                                possible_moves.append(move)
                        if len(possible_moves)>0:
                            chaining = True #keeps current turn going if more chains are possible
                        else:
                            chaining = False
                            turnCounter += 1
                            if board.turn == 1:#switches turn
                                board.turn = 0
                            elif board.turn == 0:
                                board.turn = 1
                    else:
                        turnCounter += 1
                        if board.turn == 1:#switches turn
                            board.turn = 0
                        elif board.turn == 0:
                            board.turn = 1
            moving = False
        #!!!!!!!!!!!!!!!!!!!!!
            
        #board updates
        board.update()
        if not chaining:
            possible_moves = AI.allPossibleMoves(board, board.turn) #calculates all possible moves of a turn

        #!!!!!!!!!!!!!!!!!!!!!
        #win condition (0 moves possible)
        if len(possible_moves) == 0:
            if board.turn == 0:
                winning_team = "blue"
            elif board.turn == 1:
                winning_team = "red"

            if turnCounter == 0:
                winning_team = "invalid"
            draw.winScreen(win, winning_team, big_font,turnCounter)#a screen indicating a win will appear, and program will exit
            pygame.time.delay(2000)
            pygame.quit()
        #!!!!!!!!!!!!!!!!!!!!!
            
###################################
#Instantiation of all major variables in this module
###################################
            
#!!!!!!!!!!!!!!!!!!!!!            
def modeSelect(win):
    selecting = True
    PvPbutton = pygame.Rect([100, 50], [350, 95]) #game type selection buttons
    BPvCbutton = pygame.Rect([100, 150], [350, 95])
    RPvCbutton = pygame.Rect([100, 250], [350, 95])
    while selecting:
        draw.modeSelect(win, big_font)
        
        event = pygame.event.poll()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if PvPbutton.collidepoint(pygame.mouse.get_pos()): #selecting player versus player
                return "PvP"
            elif BPvCbutton.collidepoint(pygame.mouse.get_pos()): #selecting blue player vs red computer
                return "BPvC"
            elif RPvCbutton.collidepoint(pygame.mouse.get_pos()): #selecting red player vs blue computer
                return "RPvC"
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        pygame.display.update()
#!!!!!!!!!!!!!!!!!!!!!
        
def placePieces(win, board):
    
    placing = True
    placing_player_piece = False
    placing_computer_piece = False  ##button variables
    placing_player_king = False
    placing_computer_king = False
    unplaced_player_pieces = [classes.Piece([None, None], 0, 0) for i in range(12)] ## these two hold the counters for the total number of pieces
    unplaced_computer_pieces = [classes.Piece([None, None], 1, 0) for i in range(12)] ## these two variables are lists

    #error messages
    Ecantplacehere = small_font.render("CANT PLACE HERE", True, red)
    Eoutofpieces = small_font.render("OUT OF PIECES", True, red)

    place_error = False
    piece_error = False
    
    while placing:

        #drawing
        win.fill(grey)
        draw.drawBoard(win, board) ## calls functions from draw class ## draws the vuttons and the board
        draw.drawButtons1(win, small_font, placing_player_piece, placing_computer_piece, placing_player_king, placing_computer_king)

        #mouse position [x,y] in pixels
        mpos = pygame.mouse.get_pos() # Returns the X and Y position of the mouse cursor
        
###############################################################################################################################
#BUTTON LOGIC (i.e buttons on the side interaction)
##############
#variables involved:
        #event - takes in any current event changes
        #place_error- boolean variable for declaration if you placed in an illegal square
        #piece_error - boolean for running out of pieces
        #mpos - collects the current position of a mouse click
        #click_index - divides the click into two sections
        #placing_player_piece
        #placing_computer_piece    # these four variables show which type of piece you are currently placing (boolean)
        #placing_player_king
        #placing_computer_king
###############################################################################################################################
        event = pygame.event.poll() # Returns a single event, when a change in an event occurs
        if event.type == pygame.MOUSEBUTTONDOWN: ## when the mouse is clicked
            
            place_error = False
            piece_error = False
            
            click_index = [int(mpos[0]/50), int(mpos[1]/50)] #click index is based on where we click and divided the button into sections        
            if click_index[0] > 7:  # clicking near the buttons 
                if click_index[1] < 1:
                    placing_player_piece = True
                    placing_computer_piece = False  #option that you have chosen to place a player piece
                    placing_player_king = False
                    placing_computer_king = False
                elif click_index[1] < 2 :
                    placing_player_piece = False
                    placing_computer_piece = True #option that you have chosen to place a computer piece
                    placing_player_king = False
                    placing_computer_king = False
                elif click_index[1] < 3 :
                    placing_player_piece = False
                    placing_computer_piece = False
                    placing_player_king = True  #option that you have chosen to place a king player piece
                    placing_computer_king = False
                elif click_index[1] < 4 :
                    placing_player_piece = False
                    placing_computer_piece = False  #option that you have chosen to place a king computer piece
                    placing_player_king = False
                    placing_computer_king = True            
                elif click_index[1] <  5:# option that you have created to choose the default checkers setup
                    createDefaultStart(board)  # function call below
                    placing = False
                elif click_index[1] <  6:
                    placing = False   # force starts the game option
                elif click_index[1] < 7: #load game
                    save.loadGame(board)
                    placing = False

                    
                    #clearBoard(board) # function call below
                    #placing_player_piece = False
                    #placing_computer_piece = False   # reset options # currently this is only a soft reset# for testing only
# RESET LOGIC       #placing_player_king = False
                    #placing_computer_king = False
                    #unplaced_player_pieces = [classes.Piece([None, None], 0, 0) for i in range(12)]
                    #unplaced_computer_pieces = [classes.Piece([None, None], 1, 0) for i in range(12)]


###############################################################################################################################
#Board piece placement LOGIC (i.e  board interaction)
#variables involved:
        #event - takes in any current event changes
        #board_location
        #occupied
        #placing_player_piece
        #placing_computer_piece    # these four variables show which type of piece you are currently placing (boolean)
        #placing_player_king
        #placing_computer_king
        #piece_error    # bollean used to trigger the can't place pieces
        #place_error
#############################################################################################################################                   
            else: ## clicking other places outside the buttons, which is the board
                board_location = board.tile_matrix[click_index[0]][click_index[1]]

## note that in checkers pieces can only be placed on dark squares
                
                occupied = board_location.isOccupied() # function call to check whether the space is occupied
                if placing_player_piece: # if we chose the option to place a player piece
                    if ((not occupied) & (board_location.colour == "dark")):
                        try: ##.pop function removes the pieces from the list reducing the amount of pieces you have left
                            board.piece_matrix[click_index[0]][click_index[1]] = unplaced_player_pieces.pop(0) 
                            board.piece_matrix[click_index[0]][click_index[1]].index = click_index 
                        except IndexError: ## we change the matrix of the board and simply update
                            piece_error = True
                            continue
                    else:
                        place_error = True
## code is similar below to description mention in "if placing_player_piece" above
                if placing_computer_piece:# if we chose the option to place a computer piece
                    if ((not occupied) & (board_location.colour == "dark")):
                        try:
                            board.piece_matrix[click_index[0]][click_index[1]] = unplaced_computer_pieces.pop(0)
                            board.piece_matrix[click_index[0]][click_index[1]].index = click_index 
                        except IndexError:
                            piece_error = True
                            continue
                    else:
                        place_error = True

                if placing_player_king: # if we chose the option to place a king player piece
                    if ((not occupied) & (board_location.colour == "dark")):
                        try:
                            tempP = unplaced_player_pieces.pop(0)
                            tempP.ptype = 1
                            board.piece_matrix[click_index[0]][click_index[1]] = tempP
                            board.piece_matrix[click_index[0]][click_index[1]].index = click_index
                        except IndexError:
                            piece_error = True
                            continue
                    else:
                        place_error = True

                if placing_computer_king: # if we chose the option to place a computer king piece
                    if ((not occupied) & (board_location.colour == "dark")):
                        try:
                            tempC = unplaced_computer_pieces.pop(0)
                            tempC.ptype = 1
                            board.piece_matrix[click_index[0]][click_index[1]] = tempC
                            board.piece_matrix[click_index[0]][click_index[1]].index = click_index 
                        except IndexError:
                            piece_error = True
                            continue
                    else:
                        place_error = True

#######################
#After clicking LOGIC
##############################
        if event.type == pygame.QUIT:
            pygame.quit() ## quiting the game

        if ((unplaced_player_pieces == []) & (unplaced_computer_pieces == [])):
            placing = False ## when there are no pieces to place we cannot place anymore

        if piece_error: ## displays piece error message
            win.blit(Eoutofpieces, (405,360))

        if place_error: ## displays place error message
            win.blit(Ecantplacehere, (405,360))
            
        board.update() ## updates the look of the board, more specifically the matrix

        pygame.display.update() ## displays the entire window again
        
    #end placing loop    
    return board

#####################
#unique Board Creation
####################
##  function call for creation of the board
def createBoard(rows, columns):
    tile_matrix = [[None for i in range(rows)] for j in range(columns)]
    piece_matrix = [[None for i in range(rows)] for j in range(columns)]
    for i in range(rows):
        for j in range(columns):
            if (i+j)%2 == 1:
                colour = 'dark'
            else:
                colour = 'light'
            tile = classes.Tile([i,j], colour, 50)
            tile_matrix[i][j] = tile
            tile_matrix[i][j].init()

    board = classes.Board(tile_matrix, piece_matrix)
    return board

## function call for default starting point of the board
def createDefaultStart(board):

    for i in range(len(board.tile_matrix)):
        for j in range(7):
            if board.tile_matrix[i][j].colour != "light":
                board.piece_matrix[i][j] = None

    for i in range(len(board.tile_matrix)):   # creates the matrix values for all boards
        for j in range(3):
            if board.tile_matrix[i][j].colour != "light":
                board.piece_matrix[i][j] = classes.Piece([i, j], 0, 0)        
                
    for i in range(len(board.tile_matrix)):
        for j in range(7,4,-1):
            if board.tile_matrix[i][j].colour != "light":
                board.piece_matrix[i][j] = classes.Piece([i, j], 1, 0)
## function for completely clearing the board
def clearBoard(board):

    for i in range(len(board.tile_matrix)):
        for j in range(8):
            if board.tile_matrix[i][j].colour != "light":
                board.piece_matrix[i][j] = None
