# You are given a rectangular circuit board of size n x m, and k rectangular components of arbitrary sizes.  Your job is to lay the components out in such a way that they do not overlap.  For example, maybe you are given these components:

#       bbbbb   cc
# aaa   bbbbb   cc  eeeeeee
# aaa           cc

# and are asked to lay them out on a 10x3 grid

# ..........
# ..........
# ..........

# A solution might be

# eeeeeee.cc
# aaabbbbbcc
# aaabbbbbcc

# Notice that in this case the solution is not unique!

# The variables for this CSP will be the locations of the lower left corner of each component.  Assume that the lower left corner of the board has coordinates (0, 0).  

# Make sure your code displays the output in some nice (enough) way.  Ascii art would be fine.

# A particularly strong solution might consider several boards, of different sizes and with different numbers, sizes, and shapes of parts.


from CSPProblem import *

Size = Tuple[int, int]
Component = Tuple[str, int, int]
Location = Tuple[int, int]

def _make_domain(board_size: Size, component_size: Size) -> VariableDomain:
    board_width, board_height = board_size
    comp_width, comp_height = component_size

    # Add 1 to the stop parameter of range function because it includes
    # everything *up to* the stop parameter -- and we want that last value to
    # be included (so a n*m component can fit on a n*m board)
    def generate_domain():
        for x in range(0, 1 + board_width - comp_width):
            for y in range(0, 1 + board_height - comp_height):
                yield (x, y)
    
    return set(generate_domain())

def _get_allowed_options(i_domain: VariableDomain, i_width: int, i_height: int, j_domain: VariableDomain, j_width: int, j_height: int):

    # A generator that always returns the same value. Used for constructing variable 
    # pairs below using higher-order functions.
    def reapeating_generator(val):
        while True:
            yield val

    def not_overlapping(locations: Tuple[Location, Location]) -> bool:
        i_loc, j_loc = locations
        ix, iy = i_loc
        jx, jy = j_loc

        return ix + i_width  <= jx or jx + j_width  <= ix or \
               iy + i_height <= jy or jy + j_height <= iy

    for val_i in i_domain:
        combinations = zip(reapeating_generator(val_i), j_domain)
        yield from filter(not_overlapping, combinations)

def create_circuitboardlayout_csp(board_size: Size, components: List[Component]) -> CSPProblem[Location]:

    constraints: List[BinaryConstraint] = []

    # Create Domains
    domains = list(
        map(lambda c: _make_domain(board_size, (c[1], c[2])), components)
    )
    label_map = dict(map(lambda enumeratedcomp: (enumeratedcomp[0], enumeratedcomp[1][0]), enumerate(components)))
    
    # Create constraints
    for i, (name, width, height) in enumerate(components):
        i_domain = domains[i]

        for index, (_, j_width, j_height) in enumerate(components[i+1:]):
            j = i + 1 + index
            j_domain = domains[j]

            options = _get_allowed_options(domains[i], width, height,
                                           domains[j], j_width, j_height)
            
            constraints.append(
                (
                    (i, j),
                    set(options)
                )
            )

    return CSPProblem(
        domains=domains,
        binary_constraints=constraints,
        variable_label_str=lambda i: label_map[i],
        variable_value_str=lambda v: str(v)
    )

def print_layout_csp(problem: CSPProblem, board_size: Size, components: List[Component]):
    cols, rows = board_size

    include_nums = len(set([name[0] for name, _, _ in components])) != len(components)
    num_justify = len(str(len(components)))
    
    blank = '*'
    if include_nums:
        blank = '*'.rjust(num_justify, '*')

    chars = []
    for _ in range(rows):
        chars.append([blank] * cols)
    
    unassigned_vars = []

    for i in range(0, len(problem.assignments)):
        name, width, height = components[i]
        
        if not problem.is_unassigned(i):
            x, y = problem.assignments[i]
            for row in range(y, y + height):
                for col in range(x, x + width):
                    num = ''
                    if include_nums:
                        num = str(i).rjust(num_justify)
                    chars[row][col] = f"{name[0]}{num}"
        else:
            unassigned_vars.append(problem.variable_str(i))

    for row in range(rows - 1, -1, -1):
        print(" ".join(chars[row]))

    if len(unassigned_vars) > 0:
        print("Unassigned")
    for unassigned_var in unassigned_vars:
        print(f"\t{unassigned_var}")