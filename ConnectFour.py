
#Function that returns true if there are moves available on the board
def isMovesLeft(board):
    for row in board:
        for value in row:
            if value == 0:
                return True
    return False

#Scores the current position based on the numebr of 
def score_position(board, player):
    # Score Horizontally

    # Score Vertically

    # Score Diagionally 
    pass

def minimax(board, isMax, depth,):
    pass