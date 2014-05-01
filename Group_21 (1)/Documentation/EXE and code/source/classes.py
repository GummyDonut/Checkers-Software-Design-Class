#class initialization
#PUBLIC INTERFACE IMPLICATION
import pygame
#The individual squares on the board itself
#This is the interface of most of the objects and defines all variables 
#behaviours of each class

#Changes from the last version are indicated by #!!!!!
#NEW CHANGE: some movement logic code was moved to the new AI class

class Tile:

    def __init__(self, index, colour, tile_size):
        self.index = index ## the index value of each tile in a matrix later one, the type of array
        self.tile_size = tile_size ## size for the board (Array)
        self.colour = colour# the possible colour of the tile is dark or light
        self.occupant = None ## whether that tile is occupies
        
    def init(self):                     
        tile_size = self.tile_size      #-width/height of square tile in pixels 
        index = self.index              #-2 element array storing index [column, row]
        self.rect = pygame.Rect(index[0]*tile_size, index[1]*tile_size, tile_size, tile_size)

    def isOccupied(self): #used to check whether the tile is currently occupied or not.
        if self.occupant != None:
            return True
        else:
            return False

class Piece:

    def __init__(self, index, team, ptype):
        self.index = index              #-2 element array storing the index of piece [column, row]
        self.team = team                #-boolean variable indicating computer or player piece. 
        self.ptype = ptype              #-boolean variable indicating normal or king type piece.
        self.state = "idle"             #-used for drag and drop mechanic.

    def update(self): #update function for individual piece.

                                        #######KING-ME check########
        if self.team == 1:              #-if the piece's team is blue
            if self.index[1] == 0:      #-if the piece is on the top row
                self.ptype = 1          #-change the piece's type to a king
        elif self.team == 0:            #-if the piece's team is red 
            if self.index[1] == 7:      #-if the piece is on the bottom row
                self.ptype = 1          #-change the piece's type to a king
        

class Board:

    def __init__(self, tile_matrix, piece_matrix): ## defines the matrices used to make the board and the number of pieces
        self.tile_matrix = tile_matrix  #-8x8 array of arrays storing tile data
        self.piece_matrix = piece_matrix#-8x8 array of arrays storing piece data
        self.turn = 1

    def update(self): #board update function
        for i in range(len(self.tile_matrix)):            #visiting each index individually
            for j in range(len(self.tile_matrix[0])):     #
                
                piece = self.piece_matrix[i][j]           # tile updates
                self.tile_matrix[i][j].occupant = piece   # 

                if piece != None:                         # piece updates
                    piece.update()                        #  
                
                
        

    def remove(self, piece): #function to remove a piece from the board
        self.piece_matrix[piece.index[0]][piece.index[1]] = None

    
    def move(self, move): #executes a legal move
        moving_piece = move.moving_piece
        new_index = move.new_index
        #!!!!!!!!!!!
        self.remove(moving_piece)
        moving_piece.index = new_index 
        self.piece_matrix[new_index[0]][new_index[1]] = moving_piece
        if move.kill:
            self.remove(move.kill)
            
        return True
        

            
