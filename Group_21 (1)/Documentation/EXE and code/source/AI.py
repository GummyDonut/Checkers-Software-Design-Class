#!!!!!!!!!!!!!!!
#NEW MODULE: AI, includes piece movement calculation and turn logic
#!!!!!!!!!!!!!!!

class Move:
    def __init__(self, moving_piece, new_index, kill):
        self.moving_piece = moving_piece
        self.new_index = new_index
        self.kill = kill

def isSame(move, moving_piece, destination_index):
    if moving_piece == move.moving_piece:
        if destination_index == move.new_index:
            return True
        else:
            return False
    else:
        return False

def allPossibleMoves(board, turn):
    possible_moves = []
    legal_moves = []
    for row in board.piece_matrix:
        for piece in row:
            if piece:
                new_moves = possibleMoves(piece, board, turn)
                legal_moves = legal_moves + new_moves
                
    for i in range(len(legal_moves)):
        if legal_moves[i].kill != None:
            possible_moves.append(legal_moves[i])

    if len(possible_moves) == 0:
        possible_moves = legal_moves
        
    return possible_moves

#function that returns an array of all possible moves
#this array is composed of Move class instances
def possibleMoves(piece, board, turn):
    legal_moves = []
    piece_index = piece.index
    for i in range(-2,3,1):
        for j in range(-2,3,1):
            row = piece_index[0] + i
            column = piece_index[1] + j
            if ((i == 0) & (j == 0)):
                continue
            elif ((row < 0) | (row > 7) | (column < 0) | (column > 7)):
                continue
            elif board.tile_matrix[row][column].colour == "light":
                continue
            else:
                legal_move = checkMove(board, piece, [row, column], turn)
                if legal_move:
                    legal_moves.append(legal_move)
                else:
                    continue
        
    return legal_moves

def checkMove(board, moving_piece, new_index, turn): #function that checks if move is legal and if so, executes the move.
    #NEW CHANGE: the movement logic code was moved here from the Board class move method   
    old_index = moving_piece.index                          #storing the old index of the piece being moved
    piece_type = moving_piece.ptype                         #boolean 0 or 1, normal piece or king.
    new_tile = board.tile_matrix[new_index[0]][new_index[1]] #tile that the piece is moving to

    if moving_piece.team != turn:
        return None
                                                   
    if new_tile.isOccupied():   #If the destination tile is already occupied, do nothing and return.
        return None
    else:
        if moving_piece.ptype == 0:                                                    #Error checking for normal piece types#
            if (new_index[1] <= moving_piece.index[1]) & (moving_piece.team == 0):      #can only move up with blue
                return None
            elif (new_index[1] >= moving_piece.index[1]) & (moving_piece.team == 1):    #can only move down with red
                return None
    
        if new_index[0] == moving_piece.index[0]:       #Error checking vertical movement#
            return None
        elif new_tile.colour == "light":                #Error checking for non-black destination tile#
            return None
        
        else:                                                                               #####MOVEMENT LOGIC######
            moving_distance = [new_index[0] - old_index[0], new_index[1] - old_index[1]]    #-2 element array [change in column, change in row]

            if (abs(moving_distance[0]) == 1) & (abs(moving_distance[1]) == 1):             #moving diagonally 1 (mo kill)              
                return Move(moving_piece, new_index, None)
            
            if abs(moving_distance[0]) == 2:                                                    #moving diagonally 2 (with kill)
                kill_distance = [moving_distance[0]/2, moving_distance[1]/2]                    #-2 element array halving the elements of moving _distance
                kill_index = [old_index[0] + kill_distance[0], old_index[1] + kill_distance[1]] #-index of tile that is potentially being 'killed'
                kill_tile = board.tile_matrix[kill_index[0]][kill_index[1]]                      #-tile object at that index
                if kill_tile.isOccupied() != True:                                              #-if no piece on the kill_tile, do nothing, return.
                    return None
                elif kill_tile.occupant.team == moving_piece.team:                              #-if piece on kill_tile is on same team, do nothing, return.
                    return None
                else:                                                                           #otherwise, succesful move.
                    return Move(moving_piece, new_index, kill_tile.occupant) 
