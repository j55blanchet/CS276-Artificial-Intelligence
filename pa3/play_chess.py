from HumanPlayer import HumanPlayer
from AlphaBetaAI import IterativeAlphaBetaAI
from ChessGame import ChessGame

from chess_heuristics import heuristic_master

player1 = HumanPlayer()
player2 = IterativeAlphaBetaAI(heuristic=heuristic_master)
game = ChessGame(player1, player2)

while not game.is_game_over():
    print(game)
    game.make_move()
