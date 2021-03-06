
import functools
from display import display_sudoku_solution
from typing import Dict, Iterable, List, Optional, Tuple
import random
import time
import math

ClauseIndex = int
VariableIndex = int

def randbool():
    return random.random() > 0.5

class SAT:

    STR_PREFIXES = {
        None: '?',
        True: '',
        False: '-'
    }

    def __init__(self, input: str, as_file=True) -> None:
        
        self.variable_names: Dict[int, str] = {}
        self.clauses: List[Dict[int, bool]] = []
        
        input_lines: List[str] = []
        if as_file:
            with open(input) as f:
                input_lines = f.readlines()
        else:
            input_lines = input.split('\n')

        variable_indices: Dict[str, int] = {}
        for line in input_lines:
            tokens = line.split()
            parsed = list(map(self._parse_token, tokens))
            # empty line
            if len(parsed) == 0:
                continue
            self._add_missing_variables(parsed, variable_indices)
            self._add_cnf_clause(parsed, variable_indices)
        
        self.stats_flips = 0
        self.stats_time_started = 0
        self.stats_time_elapsed = 0
        self.stats_flipped_randomly = 0

        self.p_model_stored = None
        self.p_unsatisfied_clauses = None
        
        self.model = None
    
    def _add_missing_variables(self, vars: Iterable[Tuple[bool, str]], variable_indices):
        for (_, vname) in vars:
            if not vname in variable_indices:
                var_index = len(variable_indices)
                variable_indices[vname] = var_index
                self.variable_names[var_index] = vname

    def _add_cnf_clause(self, vars: Iterable[Tuple[bool, str]], variable_indices):

        def generate_clause_dict():
            for is_positive, var_name in vars:
                yield variable_indices[var_name], is_positive 
        
        clause: Dict[int, bool] = dict(generate_clause_dict())
        self.clauses.append(clause)
    
    def select_best_variable(self, p: float, model: List[bool], choices: Iterable[VariableIndex]):

        # Case 1: Pick a variable at random
        if random.random() < p:
            self.stats_flipped_randomly += 1
            return random.choice(choices)

        # Case 2: flip the variable that maximizes # of satisfied clauses
        max_satisfied_clauses = -math.inf
        chosen_var_index = None
        for var_index in choices:
            model[var_index] = not model[var_index]
            count_satisified_clauses = len(self.clauses) - self.count_unsatisfied_clauses(model)
            if count_satisified_clauses > max_satisfied_clauses:
                chosen_var_index = var_index
                max_satisfied_clauses = count_satisified_clauses
            model[var_index] = not model[var_index]
        
        return chosen_var_index

    def gsat(self, p: float = 0.3, max_flips: int = 100000):
        
        def pick_flip_var(model, _):
            all_variables = range(len(self.variable_names))
            return self.select_best_variable(p, model, all_variables)

        return self._sat_common("GSAT", max_flips, pick_flip_var)

    def walksat(self, p: float = 0.3, max_flips: int = 100000):

        def pick_flip_var(model, unsatisfied_clauses):
            clause_of_interest = random.choice(unsatisfied_clauses)
            clause = self.clauses[clause_of_interest]

            return self.select_best_variable(p, model, list(clause.keys()))

        return self._sat_common("WalkSAT", max_flips, pick_flip_var)
    
    def _sat_common(self, mode, max_flips, pick_flip_var):

        # Initialize with random model
        self.model = [randbool() for _ in range(len(self.variable_names))]
        self.stats_flips = 0
        self.stats_time_started = time.perf_counter()
        self.stats_flipped_randomly = 0
        self.time_last_print = time.perf_counter()

        for flipnum in range(max_flips - 1):
            unsatisfied_clauses = list(self.get_unsatisfied_clauses(self.model))
            self.stats_time_elapsed = time.perf_counter() - self.stats_time_started

            if len(unsatisfied_clauses) == 0:
                # Success! We've found a model that satisfies the KB
                return self.model
            
            if time.perf_counter() - self.time_last_print > 1:

                self.time_last_print = time.perf_counter()
                percent = 100 * (flipnum + 1) / max_flips
                percent_unsatisfied_clauses =  len(unsatisfied_clauses) / len(self.clauses)
                
                print(f"{mode}[{self.stats_time_elapsed:.1f}s] Flip {flipnum + 1}/{max_flips} ({percent:.2f}%) - {len(unsatisfied_clauses)}/{len(self.clauses)} unsatisfied clauses ({percent_unsatisfied_clauses:.2f}%) \t{self.stats_flipped_randomly} random flips")

            flip_var = pick_flip_var(self.model, unsatisfied_clauses)
            self.model[flip_var] = not self.model[flip_var]
            self.stats_flips += 1

        self.stats_time_elapsed = time.perf_counter() - self.stats_time_started
        return None
    
    def get_unsatisfied_clauses(self, model: List[bool]) -> Iterable[ClauseIndex]:
        for i in range(len(self.clauses)):
            if not self.is_clause_satisfied(model, i):
                yield i

    def count_unsatisfied_clauses(self, model: List[bool]) -> int:
        count = 0
        for i in range(len(self.clauses)):
            if not self.is_clause_satisfied(model, i):
                count += 1
        return count

    def is_clause_satisfied(self, model: List[bool], clause_index: ClauseIndex):
        clause = self.clauses[clause_index]

        # if any of the variables in the clause match their value, the 
        # clause will be satisfied
        for var_index in clause:
            if model[var_index] == clause[var_index]:
                return True

    #####################
    # Utility Functions #
    #####################

    def generate_solution_lines(self, model) -> Iterable[str]:
        for (i, assn) in enumerate(model):
                prefix = SAT.STR_PREFIXES[assn]
                vname = self.variable_names[i]
                yield f"{prefix}{vname}"

    def write_solution(self, model, solution_file: str):
        with open(solution_file, 'w') as f:
            for line in self.generate_solution_lines(model):
                f.write(line + "\n")

    def solution_str(self, model) -> str:
        s = "No solution" if model is None else "\n".join(self.generate_solution_lines(model))
        return f"{s}{self.stats_str()}"
    
    def stats_str(self) -> str:
        return f"Took {self.stats_time_elapsed} secs, performed {self.stats_flips} flips"

    def _parse_token(self, token: str) -> Tuple[bool, str]:
        assert len(token) >= 1
        positive =  token[0] != '-'
        vname = token[1:] if not positive else token
        assert len(vname) > 0

        return positive, vname

    def __str__(self):

        lines = []
        for clause in self.clauses:
            line = []
            for key in clause.keys():
                line.append(f"{SAT.STR_PREFIXES[clause[key]]}{self.variable_names[key]}")
            lines.append(' ∨ '.join(line))
        
        return "\n".join(lines)

if __name__ == "__main__":
    sat = SAT("one_cell.cnf")
    model = sat.walksat(0.3, 1000)

    print(sat.solution_str(model))

# Took 19.942013442 secs, performed 2729 flips
# 38361108 function calls (38361057 primitive calls) in 19.983 seconds
                
# Took 20.169034854 secs, performed 2729 flips
#  38466976 function calls (38466925 primitive calls) in 20.213 seconds