from display import display_sudoku_solution
import random, sys
from SAT import SAT
import time
import cProfile

if __name__ == "__main__":
    # for testing, always initialize the pseudorandom number generator to output the same sequence
    #  of values:
    random.seed(1) 

    puzzle_name = str(sys.argv[1][:-4])
    sol_filename = puzzle_name + ".sol"

    sat = SAT(sys.argv[1], as_file=True)

    is_gsat = len(sys.argv) > 2 and sys.argv[2].lower() == "gsat"
    time_start = time.perf_counter()

    
    
    try:
        if is_gsat:
            sat.gsat()
        else:
            sat.walksat()

    except KeyboardInterrupt:
        print("Aborting run")
    # cProfile.run('result = sat.walksat()')
    secs = time.perf_counter() - time_start
    result = sat.model


    if result:
        sat.write_solution(result, sol_filename)
        display_sudoku_solution(sol_filename)
    else:
        print("No solution found.")

    print(sat.stats_str())
    print("gsat" if is_gsat else "walksat")
    print(sys.argv[1])
    # print(f"Took {secs} secs, performed {sat.stats_flips} flips")