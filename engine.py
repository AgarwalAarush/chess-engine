import chess
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
def stockfish_score(board, depth):
    stockfish.set_position([move.uci() for move in list(board.move_stack)])
    stockfish.set_depth(depth)
    return stockfish.get_evaluation()['value']