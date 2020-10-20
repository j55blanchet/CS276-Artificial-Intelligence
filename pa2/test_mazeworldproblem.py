
from MazeworldProblem import Maze, MazeworldProblem, MazeworldProblemState


def test_problemstate_makestatewithmove():
    state = MazeworldProblemState([(1, 1), (2, 2)], 0)

    assert state.robot_positions == ((1, 1), (2, 2))
    assert state.turn == 0

    next_state = state.make_state_with_move((1, 0, 1))

    assert next_state.robot_positions == ((2, 1), (2, 2))
    assert next_state.turn == 1

    next_state_2 = next_state.make_state_with_move((0, -1, 0))

    assert next_state_2.robot_positions == ((2, 1), (2, 1))
    assert next_state_2.turn == 0

def test_problemstate_hash_eq():
    state1a = MazeworldProblemState([(0, 0), (0, 1)], 1)
    state1b = MazeworldProblemState([(0, 0), (0, 1)], 1)
    state2  = MazeworldProblemState([(1, 0), (0, 1)], 1)
    state3  = MazeworldProblemState([(0, 0), (0, 1)], 0)

    assert state1a.__hash__() == state1b.__hash__() and state1a == state1b
    assert state1a.__hash__() != state2.__hash__()  and state1a != state2
    assert state1a.__hash__() != state3.__hash__()  and state1a != state3
    assert state2.__hash__()  != state3.__hash__()  and state2  != state3

basicMazeInput = """
##.#
#...
#.#.
\\robot 1 0
"""

complexMazeInput = """
##.##
#...#
#.#.#
#...#
#...#
#.###
\\robot 1 0
\\robot 1 1
\\robot 2 1
"""

def test_mazeworldproblem_init():
    maze = Maze(basicMazeInput, interpret_as_file=False)
    mazeproblem = MazeworldProblem(maze, ((3, 0),))

    assert mazeproblem.start_state == MazeworldProblemState([(1, 0)], 0)
    assert mazeproblem.goal_locations == ((3, 0),)
    assert mazeproblem.maze == maze

def test_mazeproblem_successors1():

    maze = Maze(basicMazeInput, interpret_as_file=False)
    mazeproblem = MazeworldProblem(maze, [(3, 0)])

    successors = mazeproblem.get_successors(mazeproblem.start_state)
    assert len(successors) == 2
    assert (0, MazeworldProblemState([(1, 0)], turn=0)) in successors
    assert (1, MazeworldProblemState([(1, 1)], turn=0)) in successors

def test_mazeproblem_successors2():

    maze = Maze(complexMazeInput, interpret_as_file=False)
    mazeproblem = MazeworldProblem(maze, [(3, 1), (4, 1), (4, 2)])

    # the only option here should be to wait for the second robot to get out
    # of the way
    successors = mazeproblem.get_successors(mazeproblem.start_state)
    assert len(successors) == 1
    assert (0, MazeworldProblemState(maze.robotloc, turn=1)) in successors

def test_mazeproblem_isgoal():

    maze = Maze(complexMazeInput, interpret_as_file=False)
    mazeproblem = MazeworldProblem(maze, [(3, 1), (4, 1), (4, 2)])

    assert not mazeproblem.is_goal(MazeworldProblemState( [(3, 2), (4, 1), (4, 1)], turn=0) )
    assert mazeproblem.is_goal(MazeworldProblemState( [(3, 1), (4, 1), (4, 2)], turn=2) )
    