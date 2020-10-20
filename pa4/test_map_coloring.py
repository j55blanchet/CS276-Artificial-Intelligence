
from logging import DEBUG
from typing import Union
from map_coloring import create_mapcoloring_csp
from CSPProblem import CSPProblem
from CSPSolver import CSPSolver
import inspect
import logging
import time

# logging.basicConfig(level=logging.DEBUG)

def helper_solve_problem(
    problem: CSPProblem, 
    printresult: bool = True,
    solver: CSPSolver = CSPSolver(),
    test_label: Union[str, None] = None):
    

    caller_name = test_label if test_label is not None else inspect.currentframe().f_back.f_code.co_name
    
    if printresult:
        print(f"{caller_name} - before solving")
        print(problem)

    success = solver.solve_problem(problem)
    print(solver)    

    if printresult and success:
        print(f"Solution:")
        print(problem)

    return success

txtbook_6_1 = [
    ("WA", "NT"),
    ("WA", "SA"),
    ("NT", "Q"),
    ("NT", "SA"),
    ("SA", "Q"),
    ("SA", "NSW"),
    ("SA", "V"),
    ("Q", "NSW"),
    ("NSW", "V")
]

def test_constraining_count():
    mapcolor_txtbook = create_mapcoloring_csp(txtbook_6_1, color_options=3)
    
    mapcolor_txtbook.assignments[5] = 0
    mapcolor_txtbook.assignments[1] = 1
    mapcolor_txtbook.domains[2] = {0, 2}
    mapcolor_txtbook.domains[3] = {2}

    ccount = mapcolor_txtbook.test_constrained_count(2, 2)
    print(mapcolor_txtbook)
    print("Constrained count: " + str(ccount))
    assert ccount == 2

def test1_simplest():
    sample = [
        ("A", "B")
    ]
    mapcolor_a = create_mapcoloring_csp(sample, color_options=2)
    helper_solve_problem(mapcolor_a)

contrived = [
        ("A", "B"),
        ("A", "C"),
        ("A", "D"),
        ("B", "D"),
        ("B", "F"),
        ("C", "D"),
        ("C", "E"),
        ("D", "E"),
        ("D", "F"),
        ("E", "F")
    ]
def test_contrived():
    csp = create_mapcoloring_csp(contrived)
    result = helper_solve_problem(csp)
    assert result

def test_contrived_insufficentcolors():
    csp = create_mapcoloring_csp(contrived, color_options=3) 
    success = helper_solve_problem(csp)
    assert not success

south_america_borders = [
    ("Venezuela", "Colombia"),
    ("Venezuela", "Brazil"),
    ("Venezuela", "Guyana"),
    ("Guyana", "Suriname"),
    ("Guyana", "Brazil"),
    ("Suriname", "French Guiana"),
    ("Suriname", "Brazil"),
    ("French Guiana", "Brazil"),
    ("Colombia", "Brazil"),
    ("Colombia", "Equador"),
    ("Columbia", "Peru"),
    ("Peru", "Brazil"),
    ("Peru", "Equador"),
    ("Peru", "Bolivia"),
    ("Peru", "Chile"),
    ("Bolivia", "Brazil"),
    ("Bolivia", "Chile"),
    ("Bolivia", "Paraguay"),
    ("Bolivia", "Argentina"),
    ("Chile", "Argentina"),
    ("Paraguay", "Brazil"),
    ("Paraguay", "Argentina"),
    ("Brazil", "Uruguay"),
    ("Uruguay", "Argentina")
]

def test_southamerica():
    print()
    mapcolor_1 = create_mapcoloring_csp(south_america_borders)
    helper_solve_problem(mapcolor_1)

def test_southamerica_heuristics():
    print()
    
    csp1 = create_mapcoloring_csp(south_america_borders)
    csp2 = create_mapcoloring_csp(south_america_borders)
    csp3 = create_mapcoloring_csp(south_america_borders)
    csp4 = create_mapcoloring_csp(south_america_borders)
    helper_solve_problem(csp1, solver = CSPSolver(selection_heuristic=CSPSolver.SELECTION_HEURISTIC_RANDOM), test_label="SouthAmerica-First")
    print()
    helper_solve_problem(csp2, solver = CSPSolver(selection_heuristic=CSPSolver.SELECTION_HEURISTIC_MRV), test_label="SouthAmerica-MRV")
    print()
    helper_solve_problem(csp3, solver = CSPSolver(selection_heuristic=CSPSolver.SELECTION_HEURISTIC_DEGREE), test_label="SouthAmerica-Degree")
    print()
    helper_solve_problem(csp4, solver=CSPSolver(ordering_heuristic=CSPSolver.ORDERING_HEURISTIC_LCV),
    test_label="SouthAmerica-Order-LCV")

def test_ac3():
    csp = create_mapcoloring_csp(south_america_borders)

    helper_solve_problem(csp, solver=CSPSolver(selection_heuristic="mrv", inference='ac3'))

def test_lcv():
    csp = create_mapcoloring_csp([
        ("A", "B"),
        ("B", "C"),
        ("C", "D"),
        ("D", "A")
    ])
    helper_solve_problem(csp, solver=CSPSolver(ordering_heuristic="lcv"))
    print("Done")



if __name__ == "__main__":
    # print()
    # test_southamerica()
    # print()
    test_southamerica_heuristics()
    # test_lcv()
    # test_ac3()