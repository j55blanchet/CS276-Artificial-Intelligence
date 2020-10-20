from MazeworldProblem import MazeworldProblem
from Maze import Maze

# from uninformed_search import bfs_search

from astar_search import astar_search

# null heuristic, useful for testing astar search without heuristic (uniform cost search).
def null_heuristic(state):
    return 0

def run_astar(maze_input, goal_locs, use_manhattan_heurstic, as_file=False, animate=False):
    maze = Maze(maze_input, interpret_as_file=as_file)
    maze_problem = MazeworldProblem(maze, goal_locs)
    heuristic = maze_problem.manhattan_heuristic if use_manhattan_heurstic else null_heuristic

    result = astar_search(maze_problem, heuristic)

    if animate:
        maze_problem.animate_path(result.path)
    return result

# # Test problems


# Maze 0: The simplest possible maze. Move 1 to the right
maze0_raw = """
..
\\robot 0 0
"""
def test_maze0():
    result = run_astar(maze0_raw, [(1, 0)], use_manhattan_heurstic=False)
    assert result.cost == 1
    assert len(result.path) == 2
    assert result.nodes_visited == 2

# Maze 1: Simple spiral maze. Each node has only one valid successor
maze1_raw = """
....#
###.#
..#.#
.##.#
....#
\\robot 0 4
"""
def test_maze1_nullheurstic():
    result = run_astar(maze1_raw, [(1, 2)], use_manhattan_heurstic=False)
    assert len(result.path) == 14
    assert result.cost == 13
    assert result.nodes_visited == 14

def test_maze1_manhattanheuristic():
    # Because there's only a single successor available for each node,
    # the result will be the same regardless of heuristic used.
    result = run_astar(maze1_raw, [(1, 2)], use_manhattan_heurstic=True)
    assert len(result.path) == 14
    assert result.cost == 13
    assert result.nodes_visited == 14

maze2_raw = """

..#.....
#...###.
...#..#.
#....#..
\\robot 1 0
"""
def test_maze2():
    result_manhattan = run_astar(maze2_raw, [(7, 0)], use_manhattan_heurstic=True)
    assert len(result_manhattan.path) == 13
    assert result_manhattan.cost == 12

    result_null      = run_astar(maze2_raw, [(7, 0)], use_manhattan_heurstic=False)
    assert len(result_null.path) == 13
    assert result_null.cost == 12

    assert result_manhattan.nodes_visited < result_null.nodes_visited

maze3_raw = """
..#..
..#..
..#..
.###.
.....
\\robot 0 4
\\robot 4 0
"""
def test_maze3():
    # Maze 3 ups the ante, with two robots that need to cross each other
    result_manhattan = run_astar(maze3_raw, [(3, 2), (1, 4)], use_manhattan_heurstic=True)
    assert len(result_manhattan.path) == 34
    assert result_manhattan.cost == 20

    result_null      = run_astar(maze3_raw, [(3, 2), (1, 4)], use_manhattan_heurstic=False)
    assert len(result_null.path) == 34
    assert result_null.cost == 20

    assert result_manhattan.nodes_visited < result_null.nodes_visited

maze4_raw = """
#######
...#...
##...##
##...##
...#...
\\robot 1 3
\\robot 5 3
\\robot 1 0
"""
def test_maze4():
    goals = [(6, 0), (0, 0), (6, 3)]
    result_manhattan = run_astar(maze4_raw, 
        goals, 
        use_manhattan_heurstic=True,
        animate=False)
    assert len(result_manhattan.path) == 25
    assert result_manhattan.cost == 24

def test_maze40():
    goals = [(30, 0)]
    result_manhattan = run_astar("maze40.maz", goals, 
        use_manhattan_heurstic=True, 
        as_file=True)
    
    assert result_manhattan.cost == 54

def test_maze41():
    goals = [(0, 20)]
    result_manhattan = run_astar("maze41.maz", goals, 
        use_manhattan_heurstic=True, 
        as_file=True)
    
    assert result_manhattan.cost == 60

def test_impossiblecorridor():
    maze_input = """
    .....
    \\robot 1 0
    \\robot 3 0
    """

    goals = [(4, 0), (0, 0)]
    result_manhattan = run_astar(maze_input, goals, 
        use_manhattan_heurstic=True, 
        as_file=False)

    assert len(result_manhattan.path) == 0

def test_corridor():
    maze_input = """
    ##.##
    .....
    \\robot 1 0
    \\robot 3 0
    """

    goals = [(4, 0), (0, 0)]
    result_manhattan = run_astar(maze_input, goals, 
        use_manhattan_heurstic=True, 
        as_file=False,
        animate=False)

    assert len(result_manhattan.path) > 0

def test_maze50():

    goals = [(15, 0), (0, 10)]
    result_manhattan = run_astar("maze50.maz", goals, 
        use_manhattan_heurstic=True, 
        as_file=True,
        animate=False)

    assert len(result_manhattan.path) > 0

def test_mazedisconnected():
    maze_input = """
    ..##..
    ..##..
    ..##..
    ..##..
    ..##..
    ..##..
    \\robot 0 0
    """

    goals = [(5, 5)]
    result_manhattan = run_astar(maze_input, goals, 
        use_manhattan_heurstic=True, 
        as_file=False,
        animate=False)

    assert len(result_manhattan.path) == 0