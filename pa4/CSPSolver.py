from typing import Deque, Iterable, List, Literal, Tuple
from CSPProblem import *
from collections import deque

import logging
import time
import random

OrderedDomain = List[VariableValue]

class CSPSolver:

    SELECTION_HEURISTIC_RANDOM = "random"
    SELECTION_HEURISTIC_MRV = "mrv"       # Minimum-Remaining Values
    SELECTION_HEURISTIC_DEGREE = "degree" # Number of connected vertices

    ORDERING_HEURISTIC_RANDOM = "random"
    ORDERING_HEURISTIC_LCV = "lcv" # Least-Constraining Variable

    INFERENCE_NONE = "none"
    INFERENCE_FORWARD_CHECKING = "forward-checking"
    INFERENCE_AC3 = "ac3"

    def __init__(
        self, 
        selection_heuristic: Literal["random", "mrv", "degree"] = "random",
        ordering_heuristic: Literal["random", "lcv"] = "random",
        inference: Literal["none", "forward-checking", "ac3"] = "none"):

        self.selection_heuristic = selection_heuristic
        self.ordering_heuristic = ordering_heuristic
        self.inference = inference

        self.stats_solution_found = False
        self.stats_solving_started_time = 0
        self.stats_solving_ended_time = 0
        self.stats_assignments_explored = 0
        self.stats_order_exploration = deque()
        self.stats_problem = None
        
    def solve_problem(self, problem: CSPProblem, depth: int = 0) -> bool:
        
        indent = "  " * depth

        if depth == 0:
            self.stats_assignments_explored = 0
            self.stats_order_exploration = deque()
            self.stats_solving_started_time = time.perf_counter()
            self.stats_solving_ended_time = -1
            self.stats_problem = problem
            self.stats_solution_found = False

        if problem.is_complete_assignment():
            self.stats_solving_ended_time = time.perf_counter()
            self.stats_solution_found = True
            return True

        var_index = self._select_variable(problem)
        self.stats_order_exploration.append(var_index)

        assn_options = self._order_domain_values(problem, var_index)
        logging.debug(f"{indent}Looking at options: {[problem.assn_str(opt) for opt in assn_options]} for {problem.label_str(var_index)}")

        for assn_option in assn_options:
            
            # Book-keeping / Logging
            label = problem.label_str(var_index)
            assn_label = problem.assn_str(assn_option)
            self.stats_assignments_explored += 1
            
            saved_domains = [
                domain.copy() for domain in problem.domains
            ]
            problem.assign(var_index, assn_option)

            # Test assignment for consistency - above if inconsistent
            if not problem.is_arc_consistent(var_index, assn_option):
                problem.unassign(var_index)
                logging.debug(f"{indent}Would be inconsistent to assign {assn_label} to {label}")
                continue

            logging.debug(f"{indent}Trying to assign {assn_label} to {label}")
            
            still_consistent = self._infer(indent, problem, var_index)
            if still_consistent and self.solve_problem(problem, depth + 1):
                    return True

            problem.unassign(var_index)
            problem.domains = saved_domains

        return False

    def _infer(self, log_indent: str, problem: CSPProblem, var_index) -> bool:

        if self.inference in {CSPSolver.INFERENCE_AC3, CSPSolver.INFERENCE_FORWARD_CHECKING}:

            problem.get_neighbor_variables(var_index)
            return self._ac3(
                log_indent,
                problem,
                initial_queue = [
                    (neighbor_index, var_index) 
                    for neighbor_index 
                    in problem.get_neighbor_variables(var_index)
                ],
                propogate_inference = (self.inference == CSPSolver.INFERENCE_AC3)
            )

        assert self.inference == CSPSolver.INFERENCE_NONE
        return True
    
    def _ac3(
        self,
        log_indent: str,
        problem: CSPProblem,
        initial_queue: Iterable[VariablePair],
        propogate_inference: bool
    ) -> bool:

        arc_queue: Deque[VariablePair] = deque(initial_queue)
        
        while len(arc_queue) > 0:
            x_i, x_j = arc_queue.popleft()
            if self._ac3_revise(log_indent, problem, x_i, x_j):
                if len(problem.domains[x_i]) == 0:
                    return False

                if propogate_inference:
                    for neighbor in problem.get_neighbor_variables(x_i):
                        if neighbor == x_j: continue
                        arc_queue.append((neighbor, x_i))

        return True

    def _ac3_revise(
        self,
        log_indent: str,
        problem: CSPProblem, 
        v_i: VariableIndex, 
        v_j: VariableIndex
    ) -> bool:

        revised = False

        for val_i in list(problem.domains[v_i]):
            
            for _, constraint_pairs in problem.constraints_between(v_i, v_j):
                
                possible_j_values =  [pos_valj for (cons_vali, pos_valj) 
                                                   in constraint_pairs 
                                                   if cons_vali == val_i]

                j_domain = problem.domains[v_j]
                if j_domain.isdisjoint(possible_j_values):
                    problem.domains[v_i].remove(val_i)
                    revised = True

                    logging.debug(f"{log_indent}[inference]: eliminating '{problem.assn_str(val_i)}' as option for {problem.label_str(v_i)}")
                    break

        return revised

    def _select_variable(self, problem: CSPProblem) -> VariableIndex:

        variable_options: List[VariableIndex] = [
            i for i in range(len(problem.assignments)) if problem.assignments[i] == CSPProblem.UNASSIGNED
        ]

        assert len(variable_options) > 0

        if self.selection_heuristic == CSPSolver.SELECTION_HEURISTIC_MRV:
            # Sort behavior of sets looks at the number of items. 
            # So it'll put smallest domains first!
            variable_options.sort(key=lambda i: len(problem.domains[i]))
            return variable_options[0]

        elif self.selection_heuristic == CSPSolver.SELECTION_HEURISTIC_DEGREE:
            # Select variable with largest number of unassigned neighbors
            # (reduces later branching factor)
            variable_options.sort(key= lambda i: problem.get_degree(i))
            return variable_options[-1]

        assert self.selection_heuristic == CSPSolver.SELECTION_HEURISTIC_RANDOM
        return random.choice(variable_options)
            
    def _order_domain_values(self, problem: CSPProblem, var_index: VariableIndex) -> OrderedDomain:
        domain = problem.domains[var_index]
        ordered_domain = list(domain)
        
        if self.ordering_heuristic == CSPSolver.ORDERING_HEURISTIC_LCV:
            ordered_domain.sort(key=lambda x: problem.test_constrained_count(var_index, x))

        else:
            assert self.ordering_heuristic == CSPSolver.ORDERING_HEURISTIC_RANDOM
            random.shuffle(ordered_domain)
        
        return ordered_domain

    def __str__(self) -> str:

        exploration_path = "[]"
        if self.stats_problem is not None:
            exploration_path = str([
                self.stats_problem.label_str(i) for i in self.stats_order_exploration
            ])

        return "\n".join([
            f"CSP Solver (sel: {self.selection_heuristic}) (ord: {self.ordering_heuristic}) (inf: {self.inference})",
            f"\tFound solution: {self.stats_solution_found}",
            f"\tSolving Time: {self.stats_solving_ended_time - self.stats_solving_started_time:.4f} secs",
            f"\tAttempted Assignments: {self.stats_assignments_explored}",
            # f"\tExploration path: {exploration_path}"
        ])
