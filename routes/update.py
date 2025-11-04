from flask import Flask, request, jsonify, Blueprint, render_template

othello_bp = Blueprint("othello", __name__)


'''
GET request for /start returns the following
    {
        "board": [8][8],
        "curr_player": 1,
        "score": {player: score},
        "valid_moves": [(x,y)]
    }
'''

@othello_bp.route('/start', methods=["GET"])
def start():
    board = [[0 for i in range(8)] for x in range(8)]

    # Set the starting pieces
    board[3][3] = 1
    board[3][4] = 2
    board[4][3] = 2
    board[4][4] = 1

    return jsonify({
        "board": board,
        "curr_player": 1,
        "score": {1:2, 2:2},
        "valid_moves": get_valid_moves(board, 1, 2)
    })

'''
POST request for /update takes the following in:
    {
        "board": [][],
        "curr_player": 1/2,
        "curr_move": (x,y)
    }

'/update' should:
    1) Validate move
    2) Update board
    3) Update score
    4) Switch players (if applicable)
    5) Check valid moves

/update should return:
    {
        "board": [8][8],
        "score": {player: score},
        "curr_player": 1/2,
        "valid_moves": [(x,y)]
    }
'''

@othello_bp.route('/update', methods=["POST"])
def handle_move():
    data = request.get_json()
    board = data['board']
    curr_player = data['curr_player']
    curr_move = data['curr_move']

    # Automatically update player for next call
    if (curr_player == 1):
        opponent = 2
    else:
        opponent = 1

    # Should return error if curr_move is out of bounds
    if (curr_move[0] >= len(board) or curr_move[1] >= len(board[0])):
        return jsonify({"error": True, "message": f"Move out of bounds"}), 400

    if not is_valid_move(board, curr_move[0], curr_move[1], curr_player, opponent):
        return jsonify({"error": True, "message": "Invalid move"}), 400   

    updated_board = update_board(board, curr_move, curr_player, opponent)
    updated_score = update_score(updated_board, curr_player, opponent)

    opponent_valid_moves = get_valid_moves(updated_board, opponent, curr_player)

    if (len(opponent_valid_moves) == 0):
        next_player = curr_player
    else:
        next_player = opponent
    
    return jsonify({
        "board": updated_board,
        "score": updated_score,
        "curr_player": next_player,
        "valid_moves": get_valid_moves(updated_board, next_player, curr_player)
        })

def update_board(board, move, player, opponent):
    row, col = move

    board[row][col] = player # updated board will show an integer of what player controls that square
    flips = get_flips(board, row, col, player, opponent) 
    
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
    
