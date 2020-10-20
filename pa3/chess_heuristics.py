import chess
import math

from chess import piece_name

HEURISTIC_WEIGHT_MATERIAL = 1
HEURISTIC_WEIGHT_MOVEOPTIONS = 0.01

# Looked values at: https://www.chess.com/terms/chess-piece-value#Chesspiecevals
_chesspiece_values = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}

def heuristic_material(board: chess.Board) -> float:
        
    if board.is_checkmate():
        return math.inf if board.turn == chess.BLACK else -math.inf

    heuristic = 0

    for piece in _chesspiece_values:
        count_white = len(board.pieces(piece, chess.WHITE))
        count_black = len(board.pieces(piece, chess.BLACK))
        heuristic += _chesspiece_values[piece] * (count_white - count_black)

    board.from_epd
    return heuristic

def heuristic_move_options(board: chess.Board) -> float:
    sign = 1 if board.turn == chess.WHITE else -1
    return sign * len(list(board.legal_moves))

def heuristic_master(board: chess.Board) -> float:
    return heuristic_material(board)     * HEURISTIC_WEIGHT_MATERIAL     + \
           heuristic_move_options(board) * HEURISTIC_WEIGHT_MOVEOPTIONS  
