from flask import Flask, request, jsonify, Blueprint, render_template
from .helper_methods.helper import *
from . import othello_bp
from .ai import minimax
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
    board[3][3] = 2
    board[3][4] = 1
    board[4][3] = 1
    board[4][4] = 2

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
        "curr_move": (x,y),
        "ai": bool,
        "depth": int,
        "prune": bool,
        "debug": bool
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
    ai = data['ai']
    depth = data['depth']
    prune = data['prune']
    debug = data['debug']

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
        opponent = curr_player
    
    if ai:
        while (next_player == 2):
            ai_legal_moves = get_valid_moves(updated_board, 1, 2)
            if (ai_legal_moves):
                _, move = minimax(updated_board, depth, 2, 1, prune, debug, True)
                updated_board = update_board(updated_board, move, 2, 1)
                updated_score = update_score(updated_board, 2, 1)

                opponent_valid_moves = get_valid_moves(updated_board, 1, 2)

                if (len(opponent_valid_moves) == 0):
                    next_player = 2
                    break
                else:
                    next_player = 1
                    opponent = 2

    return jsonify({
        "board": updated_board,
        "score": updated_score,
        "curr_player": next_player,
        "valid_moves": get_valid_moves(updated_board, next_player, opponent)
        })

'''
GET request /check_win takes the following in:
    {
        "board": [8][8],
        "score": {player: int}
    }

/check_win returns the following:
    {
        "won": bool,
        "winner": player if won else None
    }
'''

@othello_bp.route('/check_win', methods=["POST"])
def check_win():
    data = request.get_json()
    board = data['board']
    score = data['score']

    winner, winning_score = get_winner(board, score)

    return jsonify({
        "winner": winner,
        "score": winning_score
    })
    
