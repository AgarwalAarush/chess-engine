import chess
import numpy
import random
import stockfish

# Random Board Generation
def random_board(max_depth=150):
    board = chess.Board()
    depth = random.randrange(0, max_depth)

    for _ in range(depth):
        moveset = list(board.legal_moves)
        chosen_move = random.choice(moveset)
        board.push(chosen_move)
        if board.is_game_over():
            break;

    return board

# Stockfish Score
# reminder: move stockfish exe into path before building & deploying
stockfish = stockfish.Stockfish(path="../../../../../opt/homebrew/Cellar/stockfish/15.1/bin/stockfish")
def stockfish_score(board, depth=15):
    stockfish.set_position([move.uci() for move in list(board.move_stack)])
    stockfish.set_depth(depth)
    return stockfish.get_evaluation()['value']

square_index = {
    'a': 1,
    'b': 2,
    'c': 3,
    'd': 4,
    'e': 5,
    'f': 6,
    'g': 7,
    'h': 8
}

def square_to_index(square):
    letter = chess.square_name(square)
    return square_index[letter[0]] - 1, letter[1]

# Piece Charts & Attack Charts
# Experiment with adding pins, checks, threats, etc.
def board_numerical_representation(board):
    defined_board = numpy.zeros((14, 8, 8), dtype=numpy.int8)
    for piece in chess.PIECE_TYPES:
        # WHITE
        for square in board.pieces(piece, chess.WHITE):
            idx = numpy.unravel_index(square, (8, 8))
            defined_board[piece - 1][idx[0]][idx[1]] = 1
            # defined_board[12][idx[0]][idx[1]] = 1
        # BLACK
        for square in board.pieces(piece, chess.BLACK):
            idx = numpy.unravel_index(square, (8, 8))
            defined_board[piece + 5][idx[0]][idx[1]] = 1
            # defined_board[13][idx[0]][idx[1]] = 1

    # WHITE
    board.turn = chess.WHITE;
    legal_moves = board.legal_moves
    for move in legal_moves:
        idx = square_index[move.uci()[2]] - 1, int(move.uci()[3]) - 1
        defined_board[12][idx[1]][idx[0]] = 1
    
    # BLACK
    board.turn = chess.BLACK
    legal_moves = board.legal_moves
    for move in legal_moves:
        idx = square_index[move.uci()[2]] - 1, int(move.uci()[3]) - 1
        defined_board[13][idx[1]][idx[0]] = 1

    return defined_board;

# Database Creation
import pandas
def create_dataset(size=50):
    dataset = []
    for i in range(size):
        board = random_board();
        defined_board = board_numerical_representation(board);
        score = stockfish_score(board)
        dataset.append((defined_board, score))
    return dataset

def increase_dataset_size(size=50):
    df = pandas.DataFrame(create_dataset(size), columns=["board", "stockfish_score"])
    df.to_csv("resources/chess-engine-data.csv", mode='a', index=False, header=False)

