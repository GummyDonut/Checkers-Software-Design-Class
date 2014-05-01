#save game
from source import classes

def loadGame(board): #load an existing game onto a board

    file_name = "saves\save1.txt"   #static save-file name
    
    try:                                        
        save_file = open(file_name, 'r+')   #-open save-file for reading
        piece_string = save_file.read()     #-return string containing all data in save-file
        save_file.close()                   #-done with save-file so can close
        piece_list = piece_string.split("-")#-since data in save-file is seperated by '-', remove all '-' and return a list of all the elements.
        piece_matrix = [[None for i in range(8)] for j in range(8)] #-initialize the piece matrix as being empty.

        #####data in the save-file adheres to the following:#####
        # 0 = No piece
        # 1 = Normal red piece
        # 2 = King red piece
        # 3 = Normal blue piece
        # 4 = King blue piece
        
        
        for i in range(len(piece_matrix)):              #-visit all indexes individually
            for j in range(len(piece_matrix[0])):       #

                index = (8*i) + j                       #linear value of index for using when reffering to data from piece_list recovered from save-file.                      

                if piece_list[index] == '0':            #if empty, do nothing
                    piece_matrix[i][j] = None 
                elif piece_list[index] == '1':          #add red normal piece
                    piece_matrix[i][j] = classes.Piece([i,j], 0, 0)
                elif piece_list[index] == '3':          #add red king piece
                    piece_matrix[i][j] = classes.Piece([i,j], 0, 1)
                elif piece_list[index] == '2':          #add blue normal piece
                    piece_matrix[i][j] = classes.Piece([i,j], 1, 0)
                elif piece_list[index] == '4':          #add blue king piece
                    piece_matrix[i][j] = classes.Piece([i,j], 1, 1)
        
        board.piece_matrix = piece_matrix               #update the piece matrix for the board.

    except IOError:             #if no save-file exists, raise error.
        print "no save game found"
        
def saveGame(piece_matrix): #save an existing game

    piece_string = "" #initialize piece_string as empty since using string concatenation

    for column in piece_matrix:         #-visit all pieces individually
        for piece in column:            
            if piece == None:           
                piece_string += "0-"    #nothing here
                
            elif piece.team == 0:       ###red piece###
                if piece.ptype == 0:
                    piece_string += "1-" #normal red piece
                elif piece.ptype == 1:
                    piece_string += "3-" #king red piece
                    
            elif piece.team == 1:       ###blue piece###
                if piece.ptype == 0:
                    piece_string += "2-" #normal blue piece
                elif piece.ptype == 1:
                    piece_string += "4-" #king blue piece

    file_name = "saves\save1.txt"       #static save-file name
    save_file = open(file_name, 'w')    #open for writing, if none exists, create the file.
    save_file.write(piece_string)       #write piece_string data into the file
    save_file.close()                   #we are done. Close.


    
        
