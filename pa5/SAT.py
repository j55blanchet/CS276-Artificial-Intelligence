

from typing import Dict, Iterable, List, Optional, Tuple

class SAT:

    STR_PREFIXES = {
        None: '?',
        True: '',
        False: '-'
    }

    def __init__(self, cnf_filepath: str) -> None:
        
        
        
        self.filepath = cnf_filepath
        self.variable_indices: Dict[str, int] = {}
        self.variable_names: Dict[int, str] = {}
        self.clauses: List[Dict[int, bool]] = []

        with open(cnf_filepath) as f:
            for line in f:
                tokens = line.split()
                parsed = list(map(self._parse_token, tokens))
                
                self._add_missing_variables(parsed)
                self._add_cnf_clause(parsed)

        self.assignments: List[Optional[bool]] = [None] * len(self.variable_indices)
    
    def _add_missing_variables(self, vars: Iterable[Tuple[bool, str]]):
        for (_, vname) in vars:
            if not vname in self.variable_indices:
                var_index = len(self.variable_indices)
                self.variable_indices[vname] = var_index
                self.variable_names[var_index] = vname

    def _add_cnf_clause(self, vars: Iterable[Tuple[bool, str]]):

        def generate_clause_dict():
            for is_positive, var_name in vars:
                yield self.variable_indices[var_name], is_positive 
        
        clause: Dict[int, bool] = dict(generate_clause_dict())
        self.clauses.append(clause)
    
    def walksat(self):
        pass

    def write_solution(self, solution_file: str):

        

        with open(solution_file, 'w') as f:
            for (i, assn) in enumerate(self.assignments):
                prefix = SAT.STR_PREFIXES[assn]
                vname = self.variable_names[i]
                f.write(f"{prefix}{vname}\n")
    

    #####################
    # Utility Functions #
    #####################
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
    print(sat)