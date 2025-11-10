from flask import Flask, request, jsonify, Blueprint, render_template
from .helper_methods.helper import *
from . import othello_bp


'''
POST request /ai_move takes in the following:
    {
        "board": [8][8],
        "curr_player": 1/2,
        "max_depth": int,
        "prune": bool
        "debug": bool
    }

/ai_move should return the following:
    {
        "suggested_move": (x,y)
    }
'''
@othello_bp.route('/ai_move', methods=['POST'])
def ai_move():
    data = request.get_json()
    board = data['board']
    curr_player = data['curr_player']
    depth = data['max_depth']
    prune = data['prune']
    debug = data['debug']

    if (curr_player == 1):
        opponent = 2
    else:
        opponent = 1
    
    _, best_move = minimax(board, depth, curr_player, opponent, prune, debug, True)

    return jsonify({
        "suggested_move": best_move
    })

# returns max val and the move that makes that max val
def minimax(board, depth, player, opponent, prune, debug, maximizing, root_depth=None, alpha=-float('inf'), beta=float('inf')):
    if root_depth is None:
        root_depth = depth
    
    valid_moves = get_valid_moves(board, player, opponent)

    if (depth == 0 or len(valid_moves) == 0):
        value = eval(board, player, opponent)
        if debug:
            indent = " " * (root_depth - depth)
            print(f"{indent}leaf => value={value}")
        return value, None
    
    if (maximizing):
        best_val = -float('inf')
        best_move = None 

        for move in valid_moves:
            temp_board = [row[:] for row in board] # copies curr state of board
            update_board(temp_board, move, player, opponent)

            val, _ = minimax(temp_board, depth-1, opponent, player, prune, debug, False, root_depth)

            if debug:
                indent = " " * (root_depth - depth)
                print(f"{indent}max consider {move} => value={val}")

            if (val > best_val):
                best_val = val
                best_move = move
            
            if (prune):
                alpha = max(alpha, best_val)
                if beta <= alpha:
                    break
            
            if (debug):
                indent = " " * (root_depth - depth)
                print(f"{indent}max choose {best_move} => {best_val}")
        
        return best_val, best_move
    
    # minimizing
    else:
        worst_val = float('inf')
        worst_move = None

        for move in valid_moves:
            temp_board = [row[:] for row in board]
            update_board(temp_board, move, player, opponent)

            val, _ = minimax(temp_board, depth-1, opponent, player, prune, debug, True, root_depth)

            if (debug):
                indent = " " * (root_depth - depth)
                print(f"{indent}min consider {move} => value={val}") 

            if (val < worst_val):
                worst_val = val 
                worst_move = move 
            
            if (prune):
                beta = min(beta, worst_val)
                if (beta <= alpha):
                    break
            
            if (debug):
                indent = " " * (root_depth - depth)
                print(f"{indent}min choose {worst_move} => {worst_val}")

        return worst_val, worst_move

def eval(board, player, opponent):
    score = update_score(board, player, opponent)
    base_score = score[player] - score[opponent]
    # bonus for heuristic
    bonus = 0

    corners = [
        (0,0),
        (0,7),
        (7, 0),
        (7, 7)
    ]

    mobility = len(get_valid_moves(board, player, opponent)) - len(get_valid_moves(board, opponent, player))
    bonus += mobility*5

    # give additional score if piece in corner
    for row, col in corners:
        if board[row][col] == player:
            bonus += 25
        elif board[row][col] == opponent:
            bonus -= 25
    
    # give additional score if piece on the wall

    # top row
    for col in range(8):
        if board[0][col] == player:
            bonus += 10
        elif board[0][col] == opponent:
            bonus -= 10

    # bottom row
    for col in range(8):
        if board[7][col] == player:
            bonus += 10
        elif board[7][col] == opponent:
            bonus -= 10

    # left column
    for row in range(8):
        if board[row][0] == player:
            bonus += 10
        elif board[row][0] == opponent:
            bonus -= 10

    # right column
    for row in range(8):
        if board[row][7] == player:
            bonus += 10
        elif board[row][7] == opponent:
            bonus -= 10
    
    # value playing a move that results in more than one disk flipping
    # punish playing a move that results in more than one disk flipping for ai
    valid_moves = get_valid_moves(board, player, opponent)
    for move in valid_moves:
        flips = get_flips(board, move[0], move[1], player, opponent)

        if len(flips) > 1:
            bonus += (len(flips) * 2)
        if len(flips) > 4:
            bonus -= len(flips)
    
    # estimate opponent's potential flips after each valid movee
    exposure_penalty = 0
    for move in valid_moves:
        temp_board = [row[:] for row in board]
        update_board(temp_board, move, player, opponent)

        opponent_moves = get_valid_moves(temp_board, opponent, player)
        for opp_move in opponent_moves:
            flips = get_flips(temp_board, opp_move[0], opp_move[1], opponent, player)
            exposure_penalty += len(flips)

    bonus -= (exposure_penalty * 2)
    
    # give massive bonus or loss if piece will be a win/lose condition
    if len(get_valid_moves(board, player, opponent)) == 0 and (len(get_valid_moves(board, opponent, player)) == 0):
        if base_score > 0:
            return 10000
        elif base_score < 0:
            return -10000
        else:
            return 0

    return base_score + bonus
