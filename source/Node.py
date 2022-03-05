class Node:
    def __init__(self, problem, state, parent, action):
        '''
        Parameters: problem (type Problem), state (list), parent(type Node),
        action(list - list, tuple)

        Nodes are for searching. Each node has attributes:
        - self.problem: The model of problem
        - self.parent: The parent node of the current node
        - self.action: The single action done in the parent node's state leads to
        the current state
        - self.path_cost: The total cost to reach to this node from the beginning
        - self.heuristic: Heuristic of the current state
        '''
        self.problem = problem
        self.state = state 
        self.parent = parent 
        self.action = action
        self.depth = parent.depth + 1
        self.path_cost = parent.path_cost + problem.findStepCost(action)
        self.heuristic = None
    
    
    def setHeuristic(self, id=2):
        self.heuristic = self.problem.findHeuristic(self.state, id)