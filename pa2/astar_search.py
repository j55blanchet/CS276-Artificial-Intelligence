from MazeworldProblem import MazeworldProblem
from SearchSolution import SearchSolution
from queue import PriorityQueue

# take the current node, and follow its parents back
#  as far as possible. Grab the states from the nodes,
#  and reverse the resulting list of states.
def backchain(state, backpointers):
    result = []
    while state is not None:
        result.append(state)
        state = backpointers[state]

    result.reverse()
    return result

def astar_search(search_problem: MazeworldProblem, heuristic_fn):
    
    solution = SearchSolution(search_problem, "Astar with heuristic " + heuristic_fn.__name__)

    frontier = PriorityQueue()
    node_age = 0
    frontier.put((heuristic_fn(search_problem.start_state), node_age, search_problem.start_state))

    path_cost = {
        search_problem.start_state: 0
    }
    backpointers = {
        search_problem.start_state: None
    }

    while not frontier.empty():
        # Expand the next best node
        (_, _, state) = frontier.get()
        cost = path_cost[state]

        # print('Expanding state: ', state)
        solution.nodes_visited += 1

        if search_problem.is_goal(state):
            solution.path = backchain(state, backpointers)
            solution.cost = path_cost[state]
            break

        # Discover new states and add them to the fringe
        for (transition_cost, successor_state) in search_problem.get_successors(state):
            successor_cost = cost + transition_cost

            # We already found a faster path to the successor, so disregard it
            if successor_state in path_cost and successor_cost >= path_cost[successor_state]:
                continue
            
            path_cost[successor_state] = successor_cost
            backpointers[successor_state] = state

            # We include node_count in the priority queue tuple as a tiebreaker for selecting 
            # nodes with even priority. This means that the oldest nodes have a preference  
            # for getting explored first 
            priority = successor_cost + heuristic_fn(successor_state)
            node_age += 1
            frontier.put( (priority, node_age, successor_state) )
            
    return solution
