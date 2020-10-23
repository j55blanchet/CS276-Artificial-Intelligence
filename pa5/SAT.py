

from display import display_sudoku_solution
from typing import Dict, Iterable, List, Optional, Tuple
import random
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

    def __init__(self, cnf_filepath: str) -> None:
        
        self.variable_names: Dict[int, str] = {}
        self.clauses: List[Dict[int, bool]] = []
        
        with open(cnf_filepath) as f:
            variable_indices: Dict[str, int] = {}
            for line in f:
                tokens = line.split()
                parsed = list(map(self._parse_token, tokens))
                
                self._add_missing_variables(parsed, variable_indices)
                self._add_cnf_clause(parsed, variable_indices)

        
        self.stats_flips = 0

        self.p_model_stored = None
        self.p_unsatisfied_clauses = None
    
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
            return random.choice(choices)

        # Case 2: flip the variable that maximizes # of satisfied clauses
        max_satisfied_clauses = -math.inf
        chosen_var_index = None
        for var_index in choices:
            model[var_index] = not model[var_index]
            count_satisified_clauses = len(self.get_unsatisfied_clauses(model))
            if count_satisified_clauses > max_satisfied_clauses:
                chosen_var_index = var_index
                max_satisfied_clauses = count_satisified_clauses
            model[var_index] = not model[var_index]
        
        return chosen_var_index

    def gsat(self, p: float = 0.3, max_flips: int = 100000):
        
        def pick_flip_var(model, _):
            all_variables = range(len(self.variable_names))
            return self.select_best_variable(p, model, all_variables)

        return self._sat_common(max_flips, pick_flip_var)

    def walksat(self, p: float = 0.3, max_flips: int = 100000):

        def pick_flip_var(model, unsatisfied_clauses):
            clause_of_interest = random.choice(unsatisfied_clauses)
            clause = self.clauses[clause_of_interest]

            return self.select_best_variable(p, model, list(clause.keys()))

        return self._sat_common(max_flips, pick_flip_var)
    
    def _sat_common(self, max_flips, pick_flip_var):

        # Initialize with random model
        model = [randbool() for _ in range(len(self.variable_names))]
        self.stats_flips = 0

        for _ in range(max_flips - 1):
            unsatisfied_clauses = list(self.get_unsatisfied_clauses(model))
            if len(unsatisfied_clauses) == 0:
                # Success! We've found a model that satisfies the KB
                return model
            
            flip_var = pick_flip_var(model, unsatisfied_clauses)
            model[flip_var] = not model[flip_var]
            self.stats_flips += 1

        return None
    
    def get_unsatisfied_clauses(self, model: List[bool]) -> Iterable[ClauseIndex]:
        return [i for i in range(len(self.clauses)) if not self.is_clause_satisfied(model, i)]

    def is_clause_satisfied(self, model: List[bool], clause_index: ClauseIndex):
        clause = self.clauses[clause_index]

        # if any of the variables in the clause match their value, the 
        # clause will be satisfied
        for var_index in clause:
            if model[var_index] == clause[var_index]:
                return True
        
        return False

                
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
        return "\n".join(self.generate_solution_lines(model))

    def _parse_token(self, token: str) -> Tuple[bool, str]:
        assert len(token) > 1
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