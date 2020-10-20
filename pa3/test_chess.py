# pip3 install python-chess


import chess
from RandomAI import RandomAI
from HumanPlayer import HumanPlayer
from MinimaxAI import MinimaxAI
from AlphaBetaAI import AlphaBetaAI
from ChessGame import ChessGame
from chess_heuristics import *
import time
from typing import Tuple


# player1 = HumanPlayer()
# player2 = RandomAI()

# game = ChessGame(player1, player2)

# while not game.is_game_over():
#     print(game)
#     game.make_move()


#print(hash(str(game.board)))
alphabeta_d1 = AlphaBetaAI(1, heuristic_material)
alphabeta_d2 = AlphaBetaAI(2, heuristic_material)
alphabeta_d3 = AlphaBetaAI(3, heuristic_material)
alphabeta_d4 = AlphaBetaAI(4, heuristic_material)
alphabeta_d5 = AlphaBetaAI(5, heuristic_material)
alphabeta_d6 = AlphaBetaAI(6, heuristic_material)

minimax_d1 = MinimaxAI(1, heuristic_material)
minimax_d2 = MinimaxAI(2, heuristic_material)
minimax_d3 = MinimaxAI(3, heuristic_material)
minimax_d4 = MinimaxAI(4, heuristic_material)

def player_turn_name(board: chess.Board):
    return "White" if board.turn == chess.WHITE else "Black"

def get_move(ai, board: chess.Board) -> Tuple[float, chess.Move]:
    time_start = time.perf_counter()
    move = ai.choose_move(board)
    time_elapsed = time.perf_counter() - time_start

    print(f"{ai} ({player_turn_name(board)}) chose move {move}, took {time_elapsed} seconds")
    print(f"\tExamined {ai.stats_nodes_examined} nodes")
    print(f"\tMax depth of {ai.stats_max_depth}")
    return (time_elapsed, move)

def test_onemovecheckmate():
    print("\nRunning Test: test_onemovecheckmate")
    # https://www.dailychess.com/chess/chess-fen-viewer.php
    FEN = "7k/6pp/3R1p2/8/2B5/8/1K6/5q2 w - - 0 1"
    board = chess.Board(FEN)
    print(board)
    _, move = get_move(alphabeta_d1, board)
    board.push(move)
    print(board)

    assert move == chess.Move.from_uci('d6d8') 

def test_twomovecheckmate():
    print("\nRunning Test: test_twomovecheckmate")
    FEN = '7k/5ppp/6pp/8/8/7R/1K6/7n w - - 0 1'
    board = chess.Board(FEN)
    print(board)

    _, move = get_move(alphabeta_d4, board)
    
    # We should be moving the rook to somewhere among a3-e3
    assert move.from_square == chess.H3
    assert chess.square_rank(move.to_square) == 2
    assert chess.square_file(move.to_square) <= 4
    board.push(move)
    print(board)
    
    board.push_uci("h6h5")
    print("Performing h6h5")
    print(board)

    _, move2 = get_move(alphabeta_d4, board)
    assert chess.square_rank(move2.to_square) == 7
    board.push(move2)
    assert board.is_checkmate()
    print(board)

def test_twomovecheckmate_onedepth():
    print("\nRunning Test: test_twomovecheckmate_onedepth")
    FEN = '7k/5ppp/6pp/8/8/7R/1K6/7n w - - 0 1'
    board = chess.Board(FEN)
    print(board)

    _, move = get_move(alphabeta_d1, board)
    
    board.push(move)
    print(board)

def test_chooses_promotion():
    print("\nRunning Test: test_chooses_promotion")
    FEN = "8/1k5P/8/4p3/p1pp4/1p6/8/1R1K4 w - - 0 1"
    
    board = chess.Board(FEN)
    print(board)

    _, move = get_move(alphabeta_d4, board)
    
    assert move == chess.Move.from_uci('h7h8q')
    board.push(move)
    print(board)

    for _ in range(6):
        _, move = get_move(alphabeta_d4, board)
        board.push(move)
        print(board)

def test_alphabeta_vs_minimax_2movecheckmate():
    print("\nRunning Test: test_alphabeta_vs_minimax_2movecheckmate")
    FEN = '7k/5ppp/6pp/8/8/7R/1K6/8 w - - 0 1'
    
    print(f"Comparing alphabeta and minimax AIs for the following board:")
    print(chess.Board(FEN))

    minimax_time, minimax_move = get_move(minimax_d4, chess.Board(FEN))
    alphabeta_time, alphabeta_move = get_move(alphabeta_d4, chess.Board(FEN))
  
    assert minimax_move == alphabeta_move
    assert alphabeta_time < minimax_time

def test_alphabeta_vs_minimax_starting():
    print("\nRunning Test: test_alphabeta_vs_minimax_starting")
    
    get_move(minimax_d1, chess.Board())
    get_move(alphabeta_d1, chess.Board())
    get_move(minimax_d2, chess.Board())
    get_move(alphabeta_d2, chess.Board())
    get_move(minimax_d3, chess.Board())
    get_move(alphabeta_d3, chess.Board())
    get_move(alphabeta_d4, chess.Board())
    get_move(alphabeta_d5, chess.Board())
    # get_move(alphabeta_d6, chess.Board())

def test_move_reordering():
    FEN = '3bk3/2p4p/3p1np1/4pp2/2P5/3PPP2/4Q3/R2K3B b - - 0 1'

    ai = AlphaBetaAI(4, heuristic_material)

    print("With move reordering:")
    time_reorder, move_reorder = get_move(ai, chess.Board(FEN))
    
    print("\nWithout move reordering")
    ai.enable_move_reordering = False
    time_noreorder, move_noreorder = get_move(ai, chess.Board(FEN))

    assert time_reorder < time_noreorder
    assert move_reorder == move_noreorder

def test_heuristic_change():
    
    board = chess.Board()

    ai_material = AlphaBetaAI(4, heuristic_material)
    ai_material_moves = AlphaBetaAI(4, heuristic_master)
    print(board)
    get_move(ai_material, board)
    get_move(ai_material_moves, board)
    


    print("")

if __name__ == "__main__":
    test_onemovecheckmate()
    test_twomovecheckmate()
    test_twomovecheckmate_onedepth()
    test_chooses_promotion()
    test_alphabeta_vs_minimax_2movecheckmate()
    test_alphabeta_vs_minimax_starting()
    test_move_reordering()
    test_heuristic_change()    

