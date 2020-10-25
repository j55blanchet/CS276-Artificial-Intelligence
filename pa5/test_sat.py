

from SAT import SAT
import random

random.seed(1)


def run_test(input: str, p=0.3, max_flips=100000,use_gsat=False):

    sat = SAT(input, as_file=False)
    model = []

    
    if use_gsat:
        model = sat.gsat(p, max_flips)
    else:
        model = sat.walksat(p, max_flips)


    print(sat.solution_str(model))
    return model

def test_or():
    input = """
    a b c
    -a -b
    -a -c
    -b -c
    """
    model = run_test(input, use_gsat=True)
    
    assert model is not None
    assert model.count(False) == 2
    assert model.count(True) == 1

if __name__ == "__main__":
    test_or()