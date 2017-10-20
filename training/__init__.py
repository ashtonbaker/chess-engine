import numpy as np
import random
import pickle
import chess

relu = np.vectorize(lambda x: max(0, x))

class network:
    def __init__(self):
        self.layers = []

    def output(self, x):
        result = x

        # Compute values at each layer
        for layer in self.layers[:-1]:
            result = relu(np.dot(result, layer))

        # Apply softmax to final layer
        result = np.dot(result, self.layers[-1])
        #result = result / np.linalg.norm(result)
        result = result - np.max(result)
        result = np.exp(result) / np.sum(np.exp(result))

        return result

def fen_to_input(fen):
    piece_translator = {'P' : [ 1, 0, 0, 0, 0, 0],
                        'R' : [ 0, 1, 0, 0, 0, 0],
                        'N' : [ 0, 0, 1, 0, 0, 0],
                        'B' : [ 0, 0, 0, 1, 0, 0],
                        'Q' : [ 0, 0, 0, 0, 1, 0],
                        'K' : [ 0, 0, 0, 0, 0, 1],
                        'p' : [-1, 0, 0, 0, 0, 0],
                        'r' : [ 0,-1, 0, 0, 0, 0],
                        'n' : [ 0, 0,-1, 0, 0, 0],
                        'b' : [ 0, 0, 0,-1, 0, 0],
                        'q' : [ 0, 0, 0, 0,-1, 0],
                        'k' : [ 0, 0, 0, 0, 0,-1],
                        ' ' : [ 0, 0, 0, 0, 0, 0]}

    result = np.zeros((453,), dtype=np.int8)

    board, to_move, castling_rights, en_passant, halfmove, fullmove = fen.split(' ')

    ##
    board = board.replace('/', '')

    for i in range(1, 9):
        board = board.replace(str(i), ' ' * i)

    for i in range(len(board)):
        result[i:i+6] = piece_translator[board[i]]

    if to_move == 'w':
        result[384] = 1
    elif to_move == 'b':
        result[384] = -1

    if not en_passant == '-':
        row = 9 - int(en_passant[1]) - 1
        col = ord(en_passant[0]) - 96 - 1
        pos = col + (row * 8)
        print(pos)
        result[385 + pos] = 1

    if 'K' in castling_rights:
        result[449] = 1

    if 'Q' in castling_rights:
        result[450] = 1

    if 'k' in castling_rights:
        result[451] = -1

    if 'q' in castling_rights:
        result[452] = -1

    return result

def create_player_database(num_players):
    return None

def select_two_players():
    return None

def get_move(player, fen_string):
    playing_as = fen_string.split(' ')[1]
    if playing_as == 'w':
        score_index = 0
    else:
        score_index = 1

    board = chess.Board(fen_string)

    legal_moves = []
    for move in board.legal_moves:
        legal_moves.append(move)

    best_move = None
    max_score = 0

    print(len(legal_moves))
    for move in legal_moves:
        board.push(move)
        x = fen_to_input(board.fen())
        score = player.output(x)[score_index]
        board.pop()

        if score >= max_score:
            best_move = move
            max_score = score

    return best_move
