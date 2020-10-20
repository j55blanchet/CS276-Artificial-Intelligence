from Maze import Maze
from time import sleep
import functools

class MazeworldProblemState:

    def __init__(self, robot_positions, turn):
        self.robot_positions = tuple(robot_positions)
        self.turn = turn
        assert 0 <= self.turn < len(robot_positions)
    
    def make_state_with_move(self, move):
        
        (dx, dy, _) = move
        (rx, ry) = self.robot_positions[self.turn]

        next_robot_locs = list(self.robot_positions)
        next_robot_locs[self.turn] = (rx + dx, ry + dy)
        next_turn = (self.turn + 1) % len(next_robot_locs)
        
        return MazeworldProblemState(next_robot_locs, next_turn)
    
    def __hash__(self):
        return (self.robot_positions, self.turn).__hash__()

    def __str__(self):
        return str({
            'robots': self.robot_positions,
            'turn': self.turn
        })
    
    def __repr__(self):
        return str(self)

    def __eq__(self, o):
        return self.robot_positions == o.robot_positions and self.turn == o.turn


class MazeworldProblem:

    def __init__(self, maze, goal_locations):
        self.goal_locations = tuple(goal_locations)

        # State is represented as a list of robot location tuples
        self.start_state = MazeworldProblemState(maze.robotloc, 0)
        self.maze = maze
        
    def __str__(self):
        string =  "Mazeworld problem:\n" + self.maze.string_with_goals(self.goal_locations)
        return string

        # given a sequence of states (including robot turn), modify the maze and print it out.
        #  (Be careful, this does modify the maze!)
    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state.robot_positions)

        for i in range(len(path)):
            state = path[i]
            print("Move", i, str(self))
            self.maze.robotloc = state.robot_positions
            sleep(0.25)

            # print(str(self.maze))

    def get_successors(self, state):

        potential_moves = (
            (0, 0,  0), # stay still (0.1 transition cost)
            (0, 1,  1), # north (1 transition cost)
            (1, 0,  1), # east (1 transition cost)
            (0, -1, 1), # south (1 transition cost)
            (-1, 0, 1)  # west (1 transition cost)
        )

        # blindly generate next states
        successors = [
            (move[2], state.make_state_with_move(move)) for move in potential_moves
        ]

        # filter to those that are valid
        successors = [
            (tcost, state) for (tcost, state) in successors if self.is_legal(state)
        ]

        
        return successors

    def is_legal(self, state):

        # for every robot
        for i in range(len(state.robot_positions)):
            (rx, ry) = state.robot_positions[i]

            # make sure it's not hitting a wall
            if not self.maze.is_floor(rx, ry):
                return False

            # make sure it doesn't collide with any other robot
            for j in range(i + 1, len(state.robot_positions) - i):

                if rx == state.robot_positions[j][0] and ry == state.robot_positions[j][1]:
                    return False
                
        return True

    def is_goal(self, state):
        
        assert len(self.goal_locations) == len(state.robot_positions)
        
        for i in range(len(state.robot_positions)):
            (rx, ry) = state.robot_positions[i]
            (gx, gy) = self.goal_locations[i]
            if rx != gx or ry != gy:
                return False
        
        return True
    
    def manhattan_heuristic(self, state: MazeworldProblemState):
        """Estimates cost to get to goal_state using the sum of 
        manhattan distances between current robot locations and their goals

        Args:
            state (MazeworldProblemState): Problem state to return heuristic for
        Returns:
            int: Estimated remaining path cost
        """
        estimate = 0

        for i in range(len(state.robot_positions)):
            (rx, ry) = state.robot_positions[i]
            (gx, gy) = self.goal_locations[i]
            estimate += abs(rx - gx) + abs(ry - gy)
        
        return estimate


## A bit of test code. You might want to add to it to verify that things
#  work as expected.
if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_mp = MazeworldProblem(test_maze3, ((1, 4), (1, 3), (1, 2)))

    print(test_mp.get_successors(test_mp.start_state))
