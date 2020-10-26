

from os import walk
from SAT import SAT
import random

random.seed(1)


def run_test(input: str, p=0.3, max_flips=100000,use_gsat=False, as_file=False):

    sat = SAT(input, as_file=as_file)
    model = []

    
    if use_gsat:
        model = sat.gsat(p, max_flips)
    else:
        model = sat.walksat(p, max_flips)


    # print(sat.solution_str(model))
    return model, sat

def test_or():
    input = """
    a b c
    -a -b
    -a -c
    -b -c
    """
    model, sat = run_test(input, use_gsat=True)
    
    assert model is not None
    assert model.count(False) == 2
    assert model.count(True) == 1

def test_walksat_outperforms_gsat():
    
    model_gsat, gsat = run_test("one_cell.cnf", use_gsat=True, as_file=True)
    print("GSAT: " + gsat.stats_str())

    model_walksat, walksat = run_test("one_cell.cnf", use_gsat=False, as_file=True)
    print("WalkSAT: " + walksat.stats_str())

    assert model_gsat != None
    assert model_walksat != None
    assert gsat.stats_time_elapsed > walksat.stats_time_elapsed



if __name__ == "__main__":
    # test_or()
    # test_walksat_outperforms_gsat()

    model_walksat, walksat = run_test("rows_and_cols.cnf", use_gsat=False, as_file=True)
    print("WalkSAT: " + walksat.stats_str())