from pacai.util.queue import Queue
from pacai.util.stack import Stack
from pacai.util.priorityQueue import PriorityQueue

def expand(problem, curr_node):
    children = problem.successorStates(curr_node[0])
    for child in children:
        yield child

def expandCost(problem, curr_node):
    children = problem.successorStates(curr_node[0])
    for child in children:
        childWithPathCost = (child[0], child[1], child[2] + curr_node[2])
        yield childWithPathCost

def expandCostWithHeuristic(problem, curr_node):
    children = problem.successorStates(curr_node[0])
    for child in children:
        childWithPathCost = (child[0], child[1], (child[2] + curr_node[2]))
        yield childWithPathCost

def get_directions(parents, child):
    directions = []
    goal = child
    while True:
        # If we are at the start state..
        if parents.get(child) is None:
            directions.append(goal[1])
            directions.pop(0)
            return directions
        else:
            childs_parent = parents.get(child)
            directions.insert(0, childs_parent[1])
            child = childs_parent

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first [p 85].

    Your search algorithm needs to return a list of actions that reaches the goal.
    Make sure to implement a graph search algorithm [Fig. 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    ```
    print("Start: %s" % (str(problem.startingState())))
    print("Is the start a goal?: %s" % (problem.isGoal(problem.startingState())))
    print("Start's successors: %s" % (problem.successorStates(problem.startingState())))
    ```
    """
    node = (problem.startingState(), "Stop", 0)
    if problem.isGoal(node):
        return []
    fifo_queue = Stack()
    fifo_queue.push(node)
    reached = {problem.startingState()}
    parents = {node: None}
    while not len(fifo_queue) == 0:
        node = fifo_queue.pop()
        for child in expand(problem, node):
            s = child[0]
            parents[child] = node
            if problem.isGoal(s):
                return get_directions(parents, child)
            if s not in reached:
                reached.add(s)
                fifo_queue.push(child)
    return None

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """
    node = (problem.startingState(), "Stop", 0)
    if problem.isGoal(problem.startingState()):
        return []
    fifo_queue = Queue()
    fifo_queue.push(node)
    reached = {problem.startingState()}
    parents = {node: None}
    while not len(fifo_queue) == 0:
        node = fifo_queue.pop()
        for child in expand(problem, node):
            s = child[0]
            if problem.isGoal(s):
                parents[child] = node
                return get_directions(parents, child)
            if s not in reached:
                reached.add(s)
                parents[child] = node
                fifo_queue.push(child)
    return None

def uniformCostSearch(problem):
    node = (problem.startingState(), "Stop", 0)
    if problem.isGoal(problem.startingState()):
        return []
    frontier_priority_queue = PriorityQueue()
    frontier_priority_queue.push(node, 0)
    reached = {problem.startingState(): node}
    parents = {node: None}
    costs = {node:0}
    # This variable will hold the true cost for each and every variable.
    while not len(frontier_priority_queue) == 0:
        node = frontier_priority_queue.pop()
        for child in expandCost(problem, node):
            s = child[0]
            parents[child] = node
            if problem.isGoal(s):
                return get_directions(parents, child)
            if s not in reached or child[2] < reached.get(s)[2]:
                reached[s] = child
                frontier_priority_queue.push(child, child[2])
    return None

def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    node = (problem.startingState(), "Stop", 0)
    if problem.isGoal(problem.startingState()):
        return []
    frontier_priority_queue = PriorityQueue()
    init_h_val = heuristic(node[0], problem)
    frontier_priority_queue.push(node, init_h_val)
    reached = {problem.startingState(): node}
    parents = {node: None}
    costs = {node:0}
    while not len(frontier_priority_queue) == 0:
        node = frontier_priority_queue.pop()
        for child in expandCostWithHeuristic(problem, node):
            s = child[0]
            parents[child] = node
            if problem.isGoal(s):
                return get_directions(parents, child)
            if s not in reached or child[2] < reached.get(s)[2]:
                reached[s] = child
                frontier_priority_queue.push(child, child[2] + heuristic(child[0], problem))
                costs[child] = child[2]
                # Push into fringe with cost + heuristic.
                
    return None