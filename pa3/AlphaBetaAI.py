import chess
from math import inf


from chess_heuristics import heuristic_material
from math import log
from queue import Queue
from typing import Dict, Callable, List
import chess
import math
import operator
import sys
import threading
from time import sleep
import concurrent.futures
import logging

class IterativeAlphaBetaAI():
    def __init__(self, heuristic: Callable[[chess.Board], float]):
        self.heuristic = heuristic
        pass

    def choose_move(self, board: chess.Board) -> chess.Move:
        
        

        move_found = threading.Event()
        move_found.set()

        best_moves = {}
        working_depth = 0
        shouldstop = False

        print("Starting Iterative Move Search")
        print("Press any key + enter to stop move searching...")
        input_queue = Queue()
        input_thread = threading.Thread(
                target=self.add_input, 
                args=(input_queue, lambda: shouldstop), 
                daemon=True)
        input_thread.start()

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as threadpool:
            while True:
                sleep(0.1)
                # Break on first key pressed
                if not input_queue.empty() and len(best_moves) > 0:
                    threadpool.shutdown(wait=False)
                    shouldstop = True
                    break
                    
                elif not input_queue.empty():
                    input_queue.get()
                    print("Hold on! Computer hasn't chosen a move yet.")

                if move_found.is_set():
                    
                    move_found.clear()
                    if working_depth > 0:
                        move = best_moves[working_depth]
                        print(f"Move found (d={working_depth}): {move}")
                        print(f"Now searching at d={working_depth + 1}")
                        print("\tReminder: Press any key + enter to stop move searching...")
                    working_depth += 1
                    threadpool.submit(
                        self._choose_move, 
                        working_depth, 
                        board, 
                        best_moves, 
                        move_found, 
                        lambda: shouldstop)

        move = best_moves[working_depth - 1]
        print("Iterative Alpha Beta Done")
        print(f"\tFinal depth: {working_depth - 1}")
        print(f"\tFinal move: {move}")

        return best_moves[working_depth - 1]

    def _choose_move(
        self, 
        depth: int, 
        board: chess.Board,
        move_dict: Dict[int, chess.Move],
        move_selected: threading.Event,
        shouldstop: Callable[[], bool]):

        ai = AlphaBetaAI(depth, self.heuristic)
        move = ai.choose_move(board, shouldstop=shouldstop)
        move_dict[depth] = move
        move_selected.set()

    # https://stackoverflow.com/questions/2408560/python-nonblocking-console-input
    @staticmethod
    def add_input(input_queue: Queue, shouldstop: Callable[[], bool]):
        while not shouldstop():
            sleep(0.1)
            input_queue.put(sys.stdin.read(1))

class AlphaBetaAI():
    def __init__(self, depth: int, heuristic: Callable[[chess.Board], float], enable_pruning: bool=True):
        self.max_depth = depth

        self.stats_nodes_examined = 0
        self.stats_pruning_operations = 0
        self.stats_max_depth = 0
        self.heuristic = heuristic
        self.enable_pruning = enable_pruning
        self.enable_move_reordering = True
    
    def __str__(self) -> str:
        return f"AlphaBetaAI(d={self.max_depth}, h={self.heuristic.__name__})"
        
    def choose_move(self, board: chess.Board, shouldstop: Callable[[], bool]=None) -> chess.Move:
        
        self.stats_nodes_examined = 0
        self.stats_pruning_operations = 0
        self.stats_max_depth = 0

        best_move, _ = self._minmax_best_move(
            board, 
            depth=self.max_depth, 
            alpha=-math.inf,
            beta=math.inf,
            shouldstop=shouldstop)

        logging.info("")
        logging.info(f"AlphaBeta (depth={self.max_depth}):\n")
        logging.info(f"\tExamined {self.stats_nodes_examined} nodes")
        logging.info(f"\tPruned {self.stats_pruning_operations} times")
        logging.info(f"\tRecommending move {best_move}")

        return best_move

    def _minmax_best_move(
        self, 
        board: chess.Board, 
        depth: int, 
        alpha: float, 
        beta: float,
        shouldstop: Callable[[], bool]
        ) -> float:

        self.stats_nodes_examined += 1
        self.stats_max_depth = max(self.stats_max_depth, self.max_depth - depth)

        if self._cutoff_test(board, depth):
            return chess.Move.null, self.heuristic(board)
                    
        is_maximizing = board.turn == chess.WHITE
        best_score = -math.inf if is_maximizing else math.inf
        best_move = chess.Move.null
        comparison = operator.gt if is_maximizing else operator.lt

        for move in self._get_moves_ordered(board):

            if shouldstop is not None and shouldstop():
                break

            board.push(move)
            next_move, score = self._minmax_best_move(board, depth - 1, alpha, beta, shouldstop)
            board.pop()

            if comparison(score, best_score):
                best_move = move
                best_score = score

            # AB Pruning
            if self.enable_pruning:
                if is_maximizing:
                    alpha = max(alpha, score)
                else:
                    beta = min(beta, score)
                if beta <= alpha:
                    self.stats_pruning_operations += 1
                    break
            
        return (best_move, best_score)

    def _cutoff_test(self, board: chess.Board, depth: int):
        return depth == 0 or board.is_game_over()
    
    def _get_moves_ordered(self, board: chess.Board) -> List[chess.Move]:

        if self.enable_move_reordering:
            # Put captures to the front of the list - they are likely to be the best moves
            moves = list(board.generate_legal_captures())
            captures = set(board.generate_legal_captures())
            moves.extend(filter(lambda move: not move in captures, board.legal_moves))
            return moves

        return board.legal_moves