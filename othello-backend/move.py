from flask import Flask, request, jsonify, Blueprint, render_template

'''
Post request for /move takes the following in:
    {
        "board": [][],
        "curr_player": 1/2,
        "score": {"1": int, "2": int},
        "curr_move": (x,y)
    }

'/move' should:
    1) Validate move
    2) Update board
    3) Update score
'''


@app.route('/move', methods=["POST"])
def handle_move():
    data = request.get_json()
    board = data['board']
    curr_player = data['curr_player']
    score = data['score']
    curr_move = ['curr_move']

    # Should return error if curr_move is out of bounds
    if (curr_move[0] > len(board) or curr_move[1] > len(board[0])):
        return jsonify({"error": True, "message": f"Move out of bounds"}, 400)

    # Should return error if curr_move is not valid (i.e., a piece is already there)
    if (board[curr_move[0]][curr_move[1]] != 0):
        return jsonify({"error": True, "message": f"There's already a piece there"}, 400)
    
    update_board(board, curr_move, player)
    update_score(board, score)
    

def update_board(board, move, player):
    board[move[0]][move[1]] = player # updated board will show an integer of what player controls that square
    
    # loop through the surrounding squares and check if should flip

    return board 

