def update_board(board, move, player, opponent):
    row, col = move

    flips = get_flips(board, row, col, player, opponent) 
    board[row][col] = player # add new piece

    # updates all flipped pieces
    for flip_row, flip_col in flips:
        board[flip_row][flip_col] = player

    return board 

def get_flips(board, row, col, player, opponent):
    flips = []

    if (board[row][col] != 0):
        return flips

    # list containing all possible directions (up, down, etc.)
    directions = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
    
    # loops through all directions starting from the curr_move
    for d_row, d_col in directions:
        # offset row and col by the direction
        curr_row = row + d_row
        curr_col = col + d_col
        
        # temp list for holding the current indexes of pieces needing to be flipped
        temp = []


        while (0 <= curr_row < 8 and 0 <= curr_col < 8):
            
            # these pieces are controlled by opponent and should be flipped
            # add indexes in temp list
            if board[curr_row][curr_col] == opponent:
                temp.append((curr_row,curr_col))

            # at the end of the pieces that should be flipped
            # add all values from temp to flips and break loop
            elif board[curr_row][curr_col] == player:
                flips.extend(temp)
                break

            # there aren't any pieces capturable pieces
            else:
                break

            curr_row += d_row
            curr_col += d_col

    return flips

def is_valid_move(board, row, col, player, opponent):
    if board[row][col] != 0:
        return False
    
    flips = get_flips(board, row, col, player, opponent)
    return len(flips) > 0

def get_valid_moves(board,player, opponent):
    valid = []

    for row in range(8):
        for col in range(8):
            if is_valid_move(board, row, col, player, opponent):
                valid.append((row, col))
    return valid

def update_score(board, player, opponent):
    score = {player: 0, opponent: 0}

    for row in range(0,8):
        for col in range(0, 8):
            if board[row][col] == player:
                score[player] += 1
            elif board[row][col] == opponent:
                score[opponent] += 1

    return score