import math
import numpy as np 
import random 

AI = 2
PLAYER = 1
EMPTY = 0
COLUMNS = 7
ROWS = 6
WINDOW_LENGTH = 4

#Function that returns true if there are moves available on the board
def isMovesLeft(board):
    return any(0 in row for row in board)


def hasWon(board):
    
    for i in range(ROWS - 3):
        for j in range(COLUMNS):
            if(board[i][j] == PLAYER and board[i+1][j] == PLAYER 
            and board[i+2][j] == PLAYER and board[i+3][j] == PLAYER):
                return PLAYER
            elif(board[i][j] == AI and board[i+1][j] == AI
            and board[i+2][j] == AI and board[i+3][j] == AI):
                return AI
                
    for i in range(ROWS):
        for j in range(COLUMNS - 3):
            if(board[i][j] == PLAYER and board[i][j+1] == PLAYER 
            and board[i][j+2] == PLAYER and board[i][j+3] == PLAYER):
                return PLAYER
            elif(board[i][j] == AI and board[i][j+1] == AI
            and board[i][j+2] == AI and board[i][j+3] == AI):
                return AI

    for i in range(ROWS - 3):
        for j in range(COLUMNS - 3):
            if(board[i][j] == PLAYER and board[i+1][j+1] == PLAYER 
            and board[i+2][j+2] == PLAYER and board[i+3][j+3] == PLAYER):
                return PLAYER
            elif(board[i][j] == AI and board[i+1][j+1] == AI
            and board[i+2][j+2] == AI and board[i+3][j+3] == AI):
                return AI

    for i in range(COLUMNS - 3):
        for j in range(3, ROWS):
            if(board[i][j] == PLAYER and board[i+1][j-1] == PLAYER 
            and board[i+2][j-2] == PLAYER and board[i+3][j-3] == PLAYER):
                return PLAYER
            elif(board[i][j] == AI and board[i+1][j-1] == AI
            and board[i+2][j-2] == AI and board[i+3][j-3] == AI):
                return AI

    return False


def get_valid_positions(board):
    positions = []
    columns = np.transpose(board)
    for i in range(7):
        for j in range(6):
            if columns[i][j] == 0:
                positions.append((j, i))
                break
    return positions

def get_free_row(board, column):
    columns = np.transpose(board)
    for i in range(6):
        if columns[column][i] == 0:
            return (i, column)
    return False
    

def evaluate_window(window, piece):
    score = 0
    # Switch scoring based on turn
    opp_piece = PLAYER
    if piece == AI:
        opp_piece = AI

    # Prioritise a winning move
    # Minimax makes this less important
    if window.count(piece) == 4:
        score += 100
    # Make connecting 3 second priority
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    # Make connecting 2 third priority
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2
    # Prioritise blocking an opponent's winning move (but not over bot winning)
    # Minimax makes this less important
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

def score_position(board, piece):
    score = 0

    # Score centre column
    centre_array = [int(i) for i in list(board[:, COLUMNS // 2])]
    centre_count = centre_array.count(piece)
    score += centre_count * 3

    # Score horizontal positions
    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMNS - 3):
            # Create a horizontal window of 4
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score vertical positions
    for c in range(COLUMNS):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROWS - 3):
            # Create a vertical window of 4
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score positive diagonals
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            # Create a positive diagonal window of 4
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Score negative diagonals
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            # Create a negative diagonal window of 4
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

def minimax(board, isMax, depth):
    valid_positions = get_valid_positions(board)
    if len(valid_positions) == 0:
        return (None, 0)
    elif hasWon(board) == AI:
        return (None, 100000)
    elif hasWon(board) == PLAYER:
        return (None, -100000)
    elif depth == 0:
        return (None, score_position(board, AI))

    if isMax:
        best_position = random.choice(valid_positions); 
        value = -math.inf

        for position in valid_positions:
            board[position] = AI
            
            next_value = minimax(board, not isMax, depth - 1)[1]
            if next_value > value:
                value = next_value
                best_position = position

            board[position] = EMPTY
    
        return best_position, value
    
    else:
        best_position = random.choice(valid_positions)
        value = math.inf

        for position in valid_positions:
            board[position] = PLAYER
            
            next_value = minimax(board, not isMax, depth - 1)[1]

            if next_value < value:
                value = next_value
                best_position = position
            board[position] = EMPTY

        return best_position, value

def print_board(board):
    for i in range(ROWS - 1, -1, -1):
        row_print = ''
        for j in range(COLUMNS):
            if board[i][j] == 1:
                row_print += "🔵  "
            elif board[i][j] == 2:
                row_print += "🔴  "
            elif board[i][j] == 0: 
                row_print += 'X  '
        print(row_print)

def play_game():
    board = np.zeros((6, 7))    
    print_board(board)
    while True:

        
        col = int(input('Select a column number (1 - 7) ')) - 1
        player_move = get_free_row(board, col)
        if player_move is not False:
            board[player_move] = 1

            if hasWon(board) is not False:
                print(f"Player ${hasWon(board)} has won")
                break
        
            if len(get_valid_positions(board)) == 0:
                print('It is a tie')
                break

            ai_move = minimax(board, True, 5)[0]
            board[ai_move[0]][ai_move[1]] = 2
            print_board(board)

            if hasWon(board) is not False:
                print("Player 2 has won the game")
                break

            if len(get_valid_positions(board)) == 0:
                print('It is a tie')
                break


        else:
            print("Invalid Move")


    
while True:
    play_game()
    inp = input("Do you want to play again? (y/n)")
    if inp != 'y':
        break