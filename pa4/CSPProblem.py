from typing import Callable, Dict, Generic, Iterable, Set, Tuple, List, TypeVar
import functools

VariableIndex = int
VariableValue = TypeVar('VariableValue')
VariableDomain = Set[VariableValue]
VariablePair = Tuple[VariableIndex, VariableIndex]
BinaryConstraintOptions = Set[Tuple[VariableValue, VariableValue]]
BinaryConstraint = Tuple[VariablePair, BinaryConstraintOptions]

class CSPProblem(Generic[VariableValue]):
    UNASSIGNED = -1

    def __init__(
        self,  
        domains: List[VariableDomain],
        binary_constraints: Iterable[BinaryConstraint],
        variable_label_str: Callable[[int], str],
        variable_value_str: Callable[[int], str],
          max_varlabel_len: int=0,
        ):

        self.assignments = [CSPProblem.UNASSIGNED] * len(domains)
        
        self.domains = domains

        self.variable_value_str = variable_value_str
        self.variable_label_str = variable_label_str
        self.max_varlabel_len = max_varlabel_len

        # Construct constraint dictionary
        self.binary_constraints: Dict[VariableIndex, List[BinaryConstraint]] = dict([
            (index, []) for index in range(len(domains))
        ])

        for constraint in binary_constraints:
            variable_pair, allowed_combos = constraint
            vindex_1, vindex_2 = variable_pair
            assert 0 <= vindex_1 < len(domains)
            assert 0 <= vindex_2 < len(domains)
            assert vindex_1 != vindex_2
            
            self.binary_constraints[vindex_1].append(constraint)

            reversed_pair = (vindex_2, vindex_1)
            reversed_combos = [(val_2, val_1) for (val_1, val_2) in allowed_combos]
            self.binary_constraints[vindex_2].append((reversed_pair, reversed_combos))

    def __str__(self) -> str:
        lines = [
            self.variable_str(i, self.max_varlabel_len) 
            for i in range(len(self.assignments))    
        ]
        return "\n".join(lines)

    def variable_str(self, var_index, justify:int=0) -> str:
        return f"{self.label_str(var_index).rjust(justify)} - " + \
                f"{self.value_str(var_index)}"

    def label_str(self, var_index) -> str:
        return self.variable_label_str(var_index)

    def value_str(self, var_index) -> str:
        return self.assn_str(self.assignments[var_index]) if \
                    self.assignments[var_index] is not CSPProblem.UNASSIGNED else \
                self.domain_str(self.domains[var_index])

    def assn_str(self, assn: VariableValue) -> str:
        return self.variable_value_str(assn)
        
    def domain_str(self, domain) -> str:
        midstr = ",".join([self.assn_str(val) for val in domain])
        return f"({midstr})"

    def is_unassigned(self, var_index: VariableIndex) -> bool:
        return self.assignments[var_index] == CSPProblem.UNASSIGNED

    def is_complete_assignment(self) -> bool:
        for assn in self.assignments:
            if assn == CSPProblem.UNASSIGNED:
                return False
        return True

    def is_arc_consistent(self, var_index: VariableIndex, assignment: VariableValue) -> bool:

        for constraint in self.binary_constraints[var_index]:
            if not self.satisfies_binary_constraint(constraint):
                return False
            
        return True

    def satisfies_binary_constraint(self, constraint: BinaryConstraint) -> bool:

        (index_1, index_2), allowed_combinations = constraint

        for cvalue_1, cvalue_2 in allowed_combinations:
            if self._value_is_possible(index_1, cvalue_1) and \
               self._value_is_possible(index_2, cvalue_2):
                return True

        return False

    def constraints_between(self, var1: VariableIndex, var2: VariableIndex) -> List[BinaryConstraint]:
        
        return [
            # the full constraint object
            ((index1, index2), opts)
            for ((index1, index2), opts) 
                in self.binary_constraints[var1] 
            if index2 == var2
        ]

    def test_constrained_count(self, var_index: VariableIndex, test_assignment: VariableValue) -> int:
        assert self.assignments[var_index] == CSPProblem.UNASSIGNED

        constrained = 0

        for neighbor in self.get_neighbor_variables(var_index):
            if self.assignments[neighbor] != CSPProblem.UNASSIGNED:
                continue

            
            for neighbor_option in self.domains[neighbor]:
                for (i1, i2), allowed_values in self.binary_constraints[var_index]:
                    if i2 != neighbor: continue

                    allowed_opts = [v_neighbor for (v_this, v_neighbor) in allowed_values if v_this == test_assignment]
                    if neighbor_option not in allowed_opts:
                        constrained += 1
                        break
                    
        
        return constrained

    def _generate_neighbor_variables(self, var_index: VariableIndex):
        for (_, j), _ in self.binary_constraints[var_index]:
            yield j

    def get_neighbor_variables(self, var_index: VariableIndex) -> Set[VariableIndex]:
        return set(self._generate_neighbor_variables(var_index))
    
    def generate_unassigned_neighbors(self, var_index: VariableIndex):
        for (_, j), _ in self.binary_constraints[var_index]:
            if self.is_unassigned(j):
                yield j

    def get_degree(self, var_index: VariableIndex) -> int:
        return len([
            ((i, j), allowed) 
            for ((i, j), allowed) 
                in self.binary_constraints[var_index]
            if self.is_unassigned(j)
        ])


        return filter(lambda neighbor: self.assignments[neighbor] == CSPProblem.UNASSIGNED, self.get_neighbor_variables(var_index))

    def _value_is_possible(self, var_index: VariableIndex, test_val: VariableValue):
        assignment = self.assignments[var_index]

        # If variable is unassigned, make sure the domain includes the potential value
        if assignment == CSPProblem.UNASSIGNED:
            return test_val in self.domains[var_index]

        # If variable is assigned, the assignment must match the value
        return assignment == test_val

    def assign(self, var_index: VariableIndex, assignment: VariableValue):
        self.assignments[var_index] = assignment

    def unassign(self, var_index: VariableIndex):
        self.assignments[var_index] = CSPProblem.UNASSIGNED
