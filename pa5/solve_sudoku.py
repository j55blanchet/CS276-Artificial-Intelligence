from display import display_sudoku_solution
import random, sys
from SAT import SAT
import time

if __name__ == "__main__":
    # for testing, always initialize the pseudorandom number generator to output the same sequence
    #  of values:
    random.seed(1)

    puzzle_name = str(sys.argv[1][:-4])
    sol_filename = puzzle_name + ".sol"

    sat = SAT(sys.argv[1])

    time_start = time.perf_counter()
    result = sat.walksat()
    secs = time.perf_counter() - time_start

    if result:
        sat.write_solution(result, sol_filename)
        display_sudoku_solution(sol_filename)
        print(f"Took {secs} secs, performed {sat.stats_flips} flips")