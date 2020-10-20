from typing import List
from CSPProblem import CSPProblem
from CSPSolver import CSPSolver
from circuit_layout import print_layout_csp, create_circuitboardlayout_csp, Component, Size, _get_allowed_options
import logging

# logging.basicConfig(level=logging.DEBUG)

component_a_2by1 = ("a", 2, 1)
component_b_2by2 = ("b", 2, 2)
component_c_4by1 = ("c", 4, 1)
component_d_3by2 = ("d", 3, 2)
component_e_3by1 = ("e", 3, 1)
component_f_1by2 = ("f", 1, 2)

mrv_solver = CSPSolver(selection_heuristic=CSPSolver.SELECTION_HEURISTIC_MRV)
degree_solver = CSPSolver(selection_heuristic=CSPSolver.SELECTION_HEURISTIC_DEGREE)

mrv_forwardcheck_solver = CSPSolver(selection_heuristic=CSPSolver.SELECTION_HEURISTIC_MRV,
inference=CSPSolver.INFERENCE_FORWARD_CHECKING
)
mrv_lcv_forwardcheck_solver = CSPSolver (selection_heuristic=CSPSolver.SELECTION_HEURISTIC_MRV,
    ordering_heuristic=CSPSolver.ORDERING_HEURISTIC_LCV,
inference=CSPSolver.INFERENCE_FORWARD_CHECKING
)

lcv_solver = CSPSolver(ordering_heuristic=CSPSolver.ORDERING_HEURISTIC_LCV)

ac3_solver = CSPSolver(inference=CSPSolver.INFERENCE_AC3)
forwardcheck_solver = CSPSolver(inference=CSPSolver.INFERENCE_FORWARD_CHECKING)

full_solver = CSPSolver(
    selection_heuristic=CSPSolver.SELECTION_HEURISTIC_MRV,
    ordering_heuristic=CSPSolver.ORDERING_HEURISTIC_LCV,
    inference=CSPSolver.INFERENCE_AC3
)

def run_test(board_size: Size, components: List[Component], solver=CSPSolver(), print_test: bool=True, print_perf: bool=False) -> CSPProblem:
    problem = create_circuitboardlayout_csp(
        board_size=board_size, 
        components=components
    )
    if print_test:
        print("Before solving")
        print_layout_csp(problem, board_size, components)

    solver.solve_problem(problem)

    if print_test:
        print("After solving")
        print_layout_csp(problem, board_size, components)

    if print_perf:
        print(solver)
    return problem, solver

# Test-Initial-Domain

def test_allowed_options():
    # Suppose we have a 3x3 grid with a 1x2 and a
    # 2x2 component. There should be 8 possible combinations.

    i_domain = {
        (0, 0), (0, 1), (0, 2),
        (1, 0), (1, 1), (1, 2)
    }
    i_width = 2
    i_height = 1
    j_domain = {
        (0, 0), (0, 1),
        (1, 0), (1, 1)
    }
    j_width = 2
    j_height = 2

    opts = _get_allowed_options(
        i_domain, i_width, i_height, 
        j_domain, j_width, j_height
    )

    opts = list(opts)
    assert len(opts) == 8 
    assert set(opts) == {
        ((0, 0), (0, 1)),
        ((0, 0), (1, 1)),
        ((0, 2), (0, 0)),
        ((0, 2), (1, 0)),
        ((1, 0), (0, 1)),
        ((1, 0), (1, 1)),
        ((1, 2), (0, 0)),
        ((1, 2), (1, 0)),
    }

def test_initial_domain():
    board_size = (2, 2)
    components = [component_a_2by1]
    problem = create_circuitboardlayout_csp(
        board_size=board_size, 
        components=components
    )
    print_layout_csp(problem, board_size, components)

    assert problem.domains[0] == {
        (0, 0),
        (0, 1)    
    }    # Only one option for domain
    assert len(problem.domains) == 1

def test_singlecomponent_valid():
    board_size = (2, 2)
    components = [component_a_2by1]
    
    problem, _ = run_test(board_size, components)
    
    assert problem.assignments[0] in {(0, 0), (0, 1)}
    assert problem.is_complete_assignment()

def test_singlecomponent_nosolution():
    board_size = (2, 2)
    components = [component_c_4by1]
    problem, _ = run_test(board_size, components)
    assert problem.is_unassigned(0)
    assert not problem.is_complete_assignment()

def test_twocomponents_solution():
    board_size = (4, 1)
    components = [component_a_2by1, component_a_2by1]
    problem, _ = run_test(board_size, components)

    assert problem.is_complete_assignment()

def test_twocomponents_nosolution():
    board_size = (4, 3)
    components = [component_d_3by2, component_d_3by2]
    problem, _ = run_test(board_size, components)

    assert not problem.is_complete_assignment()   


def test_mediumcomplexity_layout():
    board_size = (4, 3)
    components = [
        component_d_3by2, 
        component_f_1by2, 
        component_c_4by1
    ]
    problem, _ = run_test(board_size, components)

    assert problem.is_complete_assignment()   

def test_mediumcomplexity_impossible():
    board_size = (4, 3)
    components = [
        component_e_3by1, 
        component_e_3by1, 
        component_f_1by2,
        component_d_3by2
    ]
    problem, _ = run_test(board_size, components)

    assert not problem.is_complete_assignment()

def test_complex_layout():
    board_size = (5, 4)
    components = [
        component_a_2by1,
        component_a_2by1,
        component_b_2by2,
        component_c_4by1,
        component_d_3by2,  
        component_f_1by2
    ]
    problem, _ = run_test(board_size, components)

    assert problem.is_complete_assignment()

def test_large_layout_performance():

    board_size = (7, 5)
    components = [
        component_a_2by1,
        component_b_2by2,
        component_c_4by1,
        component_c_4by1,
        component_c_4by1,
        component_d_3by2,
        component_d_3by2,  
        component_f_1by2,
        component_f_1by2
    ]

    # run_test(board_size, components, print_test=False, print_perf=True)
    run_test(board_size, components, print_test=False, print_perf=True, solver=mrv_solver)
    run_test(board_size, components, print_test=False, print_perf=True, solver=mrv_forwardcheck_solver)
    run_test(board_size, components, print_test=False, print_perf=True, solver=degree_solver)
    # run_test(board_size, components, print_test=False, print_perf=True, solver=lcv_solver)
    # run_test(board_size, components, print_test=False, print_perf=True, solver=ac3_solver)
    # run_test(board_size, components, print_test=False, print_perf=True, solver=forwardcheck_solver)

    run_test(board_size, components, print_test=False, print_perf=True, solver=mrv_lcv_forwardcheck_solver)
    run_test(board_size, components, print_test=False, print_perf=True, solver=full_solver)


# TODO: create test where baseline solver can't finish but full solver goes quite quickly

# TODO: compare foward checking and ac3 (use mrv). Just much much does this improve performance? Is ac3 overkill?

if __name__ == "__main__":
    # test_singlecomponent_valid()
    # test_allowed_options()
    # test_twocomponents_solution()
    # test_twocomponents_nosolution()
    # test_mediumcomplexity_layout()
    # test_complex_layout() 
    test_large_layout_performance()