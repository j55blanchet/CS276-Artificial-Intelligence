from functools import partial
from SensorlessProblem import Maze, SensorlessProblem, HEURISTIC_NONADMISSIBLE_CONVERGANCE_FACTOR, HEURISTIC_NONADMISSIBLE_WEIGHT
from astar_search import astar_search
import functools


def run_astar(maze_input, goal_x, goal_y, animate=False):
    maze = Maze(maze_input, interpret_as_file=False)
    test_problem = SensorlessProblem(maze, goal_x, goal_y)

    result = astar_search(test_problem, test_problem.heuristic_composite)

    if animate:
        test_problem.animate_path(maze, result.path, (goal_x, goal_y))

    return (maze, result)


def test_maze0():
    maze0_input = """
    ##.#
    #...
    #.#.
    """
    _, result = run_astar(maze0_input, 3, 0, animate=False)
    assert len(result.path) == 6
    assert result.cost == 5


maze1_input = """
##.##.#
#..#..#
.......
#..#..#
#......
##...#.
....##.
"""

def test_maze1():
    
    maze = Maze(maze1_input, interpret_as_file=False)
    test_problem = SensorlessProblem(maze, 0, 0)

    result_composite = astar_search(test_problem, test_problem.heuristic_composite)

    assert len(result_composite.path) == 18
    assert result_composite.cost == 17

    result_weighted = astar_search(test_problem, test_problem.heuristic_nonadmissible_weighted)
    assert len(result_weighted.path) >= 16
    assert result_weighted.nodes_visited < result_composite.nodes_visited


maze2_input = """
    ##########
    #........#
    #..#.##..#
    #..#.#.#..
    #..##..##.
    #.......##
    ....######
    """    
for weight, convergence_factor in [
    
    (2,   2),
    (1.5, 2),
    (1.25, 2),
    (1,   2),
    (0.5, 2),
    
    (1.5,  2),
    (1.5,  1.5),
    (1.5,  1),
    (1.5,  0.5)
    
    ]:
        goal = (4, 1)
        maze = Maze(maze2_input, interpret_as_file=False)
        test_problem = SensorlessProblem(maze, *goal)

        heuristic = partial(test_problem.heuristic_nonadmissible_weighted, weight=weight, convergence_factor=convergence_factor)
        heuristic.__name__ = f"heuristic_nonadmissible_composite_{weight}-{convergence_factor}"
        result = astar_search(test_problem, heuristic)

        # SensorlessProblem.animate_path(maze, result.path, goal)

        print("")
        print("Heuristic Weight", weight)
        print("Convergence Factor", convergence_factor)
        print("Visited Nodes", result.nodes_visited)
        print("Solution Cost", result.cost)


