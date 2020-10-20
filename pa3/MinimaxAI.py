from AlphaBetaAI import AlphaBetaAI
from typing import Dict, Callable, List
from time import sleep
import logging
import chess

class MinimaxAI(AlphaBetaAI):
    def __init__(self, depth: int, heuristic: Callable[[chess.Board], float]):
        super().__init__(
            depth=depth,
            heuristic=heuristic,
            enable_pruning=False
        )
    def __str__(self) -> str:
        return f"MinimaxAI(d={self.max_depth}, h={self.heuristic.__name__})"