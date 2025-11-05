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

    if (curr_player == 1):
        opponent = 2
    else:
        opponent = 1
    
    _, best_move = minimax(board, depth, curr_player, opponent, prune, True)

    return jsonify({
        "suggested_move": best_move
    })

# returns max val and the move that makes that max val
def minimax(board, depth, player, opponent, prune, maximizing, alpha=-float('inf'), beta=float('inf')):
    valid_moves = get_valid_moves(board, player, opponent)

    if (depth == 0 or len(valid_moves) == 0):
        return eval(board, player, opponent), None
    
    if (maximizing):
        best_val = -float('inf')
        best_move = None 

        for move in valid_moves:
            temp_board = [row[:] for row in board] # copies curr state of board
            update_board(temp_board, move, player, opponent)

            val, _ = minimax(temp_board, depth-1, opponent, player, prune, False)

            if (val > best_val):
                best_val = val
                best_move = move
            
            if (prune):
                alpha = max(alpha, best_val)
                if beta <= alpha:
                    break
        
        return best_val, best_move
    
    # minimizing
    else:
        worst_val = float('inf')
        worst_move = None

        for move in valid_moves:
            temp_board = [row[:] for row in board]
            update_board(temp_board, move, player, opponent)

            val, _ = minimax(temp_board, depth-1, opponent, player, prune, True)

            if (val < worst_val):
                worst_val = val 
                worst_move = move 
            
            if (prune):
                beta = min(beta, worst_val)
                if (beta <= alpha):
                    break

        return worst_val, worst_move
    
def eval(board, player, opponent):
    score = update_score(board, player, opponent)

    return score[player] - score[opponent] 