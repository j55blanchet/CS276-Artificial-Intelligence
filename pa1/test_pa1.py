""" test_pa1.py

@author Julien Blanchet
@created Sept 21, 2020

Used to test functionality of my implementation of programming
assignment #1 for the COSC 276.

"""
from uninformed_search import *
from FoxProblem import *
from SearchSolution import *
import random

def test_searchnode_inparent():
    """Ensure that dfs search nodes accurately report when a state is along the explored path """
    node1 = SearchNode(1)
    node2 = SearchNode(2, node1)
    node3 = SearchNode(3, node2)
    node4 = SearchNode(4, node3)
    node5 = SearchNode(5, node4)

    for i in range(1, 5):
        assert node5.is_state_in_path(i)

    assert not node5.is_state_in_path(0)
    assert not node5.is_state_in_path(6)
    assert not node3.is_state_in_path(5)
    assert not node1.is_state_in_path(3)


problem331 = FoxProblem((3, 3, 1))
def test_331_bfs():
    result = bfs_search(problem331)
    assert len(result.path) == 12
    assert result.nodes_visited == 15

def test_331_dfs():
    result = dfs_search(problem331)
    # DFS may not return the shortest path, but it should
    # find a path if there is one.
    assert len(result.path) >= 12
    assert result.nodes_visited >= 10

def test_331_ids():
    result = ids_search(problem331)
    # IDS may not return the shortest path, but it should
    # find a path if there is one.
    assert len(result.path) >= 12
    assert result.nodes_visited >= 10

# The 551 problem should not have any solution
problem551 = FoxProblem((5, 5, 1))
def test_551_bfs():    
    result = bfs_search(problem551)
    assert len(result.path) == 0

def test_551_dfs():    
    result = dfs_search(problem551)
    assert len(result.path) == 0

def test_551_ids():    
    result = ids_search(problem551)
    assert len(result.path) == 0

# The 541 problem should have a solution
problem541 = FoxProblem((5, 4, 1))
def test_541_bfs():
    result = bfs_search(problem541)
    assert len(result.path) == 16
    assert result.nodes_visited >= 16

def test_541_dfs():
    result = dfs_search(problem541)
    assert len(result.path) >= 16
    assert result.nodes_visited >= 16

def test_541_ids():
    result = ids_search(problem541)
    assert len(result.path) >= 16
    assert result.nodes_visited >= 16

def test_get_successors():
    successors = set(problem331.get_successors((3, 3, 1)))
    assert len(successors) == 3
    assert (3,1,0) in successors
    assert (2,2,0) in successors
    assert (3,2,0) in successors

    successors = set(problem331.get_successors((3,1,0)))
    assert len(successors) == 2
    assert (3,2,1) in successors
    assert (3,3,1) in successors

def test_successors2():
    successors = set (problem551.get_successors((5, 1, 1)))
    assert len(successors) == 1
    assert (5, 0, 0) in successors

def test_fuzztest():
    for f in range(0, 7):
        for c in range(0, 7):
            problem = FoxProblem((f, c, 1))

            bfs_res = bfs_search(problem)
            dfs_res = dfs_search(problem)
            ids_res = ids_search(problem)

            bfs_found = len(bfs_res.path) > 0
            dfs_found = len(dfs_res.path) > 0
            ids_found = len(ids_res.path) > 0

            assert bfs_found == dfs_found == ids_found