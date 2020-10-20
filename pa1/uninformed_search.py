
from FoxProblem import FoxProblem
from collections import deque
from SearchSolution import SearchSolution

class SearchNode:
    """A search node for a DFS search (unused for BFS).
    
    The node stores parent information to allow for checking if a 
    state is along the search path
    """
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
    
    def is_state_in_path(self, state):
        if self.state == state:
            return True
        if self.parent is None:
            return False
        
        return self.parent.is_state_in_path(state)


def bfs_backtrace(backpointers, state):
    """Construct a path back to the start state

    Args:
        backpointers (dict): Backpointer dictionary
        state (Hashable): State from which to construct the path 

    Returns:
        list: The path back to the start state
    """
    path = []
    while state in backpointers and state is not None:
        path.append(state)
        state = backpointers[state]
    return path

def bfs_search(search_problem):
    """Perform a breadth first search. 

    Args:
        search_problem (FoxProblem): The search problem to find a solution to
        
    Returns:
        SearchSolution: The solution to the search
    """

    solution = SearchSolution(problem=search_problem,
                              search_method="bfs_search")
    backpointers = {
        search_problem.start_state: None
    }

    frontier = deque([search_problem.start_state])
    
    # Expand the frontier in a FIFO way
    while len(frontier) > 0 and not search_problem.goal_state in backpointers:
        state = frontier.pop()

        # print_backtrace(state)
        successors = list(search_problem.get_successors(state))  
        for successor in successors:
            if successor in backpointers:
                continue
            
            backpointers[successor] = state
            if search_problem.is_goal(successor):
                # No need to look at the rest of the successors if 
                # we've reached the goal state
                break

            frontier.append(successor)
    
    solution.nodes_visited = len(backpointers)
    
    # Reconstruct path back to starting node.
    solution.path = bfs_backtrace(backpointers, search_problem.goal_state)

    return solution


def dfs_search(search_problem, depth_limit=100, node =None, solution=None):
    """Perform a depth-first search of the search problem

    Args:
        search_problem (SearchProblem): The search problem to perform DFS on 
        depth_limit (int, optional): The maximum recusion depth to use. Defaults to 100.
        node (SearchNode, optional): Node from which to perform the depth-first search, used in recursive calls. Defaults to None.
        solution (SearchSolution, optional): The search solution, used by recursive calls to record visited nodes and the path. Defaults to None.

    Returns:
        SearchSolution: The results from the search
    """
    assert depth_limit >= 0

    # if no node object given, create a new search from starting state
    if node == None:
        node = SearchNode(search_problem.start_state)
        solution = SearchSolution(search_problem, "DFS")

    solution.nodes_visited += 1

    # Base case A: this node is the goal node! Return true and record path
    if search_problem.is_goal(node.state):
        solution.path.append(node.state)
        return solution

    # Base case B: we've reached our depth limit. Report not-found
    if depth_limit == 0:
        return solution

    # Recursion: try searching each of the successors
    for successor_state in search_problem.get_successors(node.state):
        
        # Check to make sure the successor state is not  
        # already along the path
        if node.is_state_in_path(successor_state):
            continue

        successor_node = SearchNode(successor_state, parent=node)

        # Note: this will update the exisitng search solution,
        # so no need to store the results
        dfs_search(search_problem=search_problem,
                   depth_limit=depth_limit - 1,
                   node=successor_node,
                   solution=solution)

        # If DFS on the successor found the goal, then 
        # hurray! This node is next on the path.
        if len(solution.path) > 0:
            solution.path.append(node.state)
            return solution
    
    # If we fell out of the above loop, it means that none of the bfs searches 
    # to our child nodes found the goal - so return false
    return solution

def ids_search(search_problem, depth_limit=100):

    solution = SearchSolution(search_problem, "IDS")

    for depth in range(depth_limit):
        dfs_result = dfs_search(search_problem, depth)
        solution.nodes_visited += dfs_result.nodes_visited

        if len(dfs_result.path) > 0:
            solution.path = dfs_result.path
            return solution

    # This will only occur when no solution is found.
    return solution
    
