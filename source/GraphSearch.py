import Root
import Node


class GraphSearch:
    def __init__(self, problem):
        '''
        Parameters: problem (type Problem)
        Attributes:
        - self.problem (Problem): The model of problem
        - self.root_node (Node): The root of the problem
        - self.fringe (list): The fringe of graph
        - self.explored (list): Contains explored state
        - self.time_complexity (integer): Time complexity of strategy implemented
        - self.space_complexity (integer): Space complexity of strategy implemented

        Formulate the graph for searching. The way of formulation is replied on the 
        each problem. In our scope, it is Bridge and Torch.
        '''
        self.problem = problem
        self.root_node = Root(problem) 
        self.fringe = [self.root_node]
        self.explored = []

        self.result = None

        self.time_complexity = 1 
        self.space_complexity = 1
        self.max_space_complexity = 1
    

    def expandNode(self, node):
        '''
        Parameters: node (type Node)
        Return    : successors (list)

        Construct a list of child nodes from the current node 
        '''
        successors = []
        for action, result_state in self.problem.findSuccessorFn(node.state):
            new_node = Node(self.problem, result_state, node, action)
            self.time_complexity += 1
            self.space_complexity += 1
            successors.append(new_node)

        return successors
    

    def BreathFirstSearch(self):
        '''
        Graph search using strategy Uniform cost search
        Return solution if it find one, o.w return a failure
        '''
        while self.fringe:
            node = self.fringe.pop(0)
            
            if self.problem.testGoal(node.state):
                self.result = node.path_cost
                self.max_space_complexity = max(self.max_space_complexity, self.space_complexity)
                return f'Status: Solution found\nOPTIMAL: {self.problem.checkObjective(node)}\nOverall duration: {node.path_cost}\n' \
                + str(self.problem.findSolution(node))
            
            if node.state not in self.explored:
                self.explored.append(node.state)
                self.space_complexity += 1 # Keep node.state in explored
                child_nodes = self.expandNode(node)
                self.fringe += child_nodes
            
            else:
                self.max_space_complexity = max(self.max_space_complexity, self.space_complexity)
                self.space_complexity -= 1

        self.max_space_complexity = max(self.max_space_complexity, self.space_complexity)
        return 'Status: Solution not found\n'
    

    def DepthFirstSearch(self):
        '''
        Graph search using strategy Depth first search
        Return solution if it find one, o.w return a failure
        '''
        while self.fringe:
            node = self.fringe.pop()
            
            if self.problem.testGoal(node.state):
                self.result = node.path_cost
                self.max_space_complexity = max(self.max_space_complexity, self.space_complexity)
                return f'Status: Solution found\nOPTIMAL: {self.problem.checkObjective(node)}\nOverall duration: {node.path_cost}\n' \
                + str(self.problem.findSolution(node))
            
            if node.state not in self.explored:
                self.explored.append(node.state)
                self.space_complexity += 1 # Keep node.state in explored
                child_nodes = self.expandNode(node)
                self.fringe += child_nodes
            
            else:
                self.max_space_complexity = max(self.max_space_complexity, self.space_complexity)
                self.space_complexity -= 1

        self.max_space_complexity = max(self.max_space_complexity, self.space_complexity)
        return 'Status: Solution not found\n'


    def UniformCostSearch(self):
        '''
        Graph search using strategy Uniform cost search
        Return solution if it find one, o.w return a failure
        '''
        while self.fringe:
            node = self.fringe.pop(self.fringe.index(min(self.fringe, 
                                                        key=lambda x: x.path_cost)))
            
            if self.problem.testGoal(node.state):
                self.result = node.path_cost
                self.max_space_complexity = max(self.max_space_complexity, self.space_complexity)
                return f'Status: Solution found\nOPTIMAL: {self.problem.checkObjective(node)}\nOverall duration: {node.path_cost}\n' \
                + str(self.problem.findSolution(node))
            
            elif node.state not in self.explored:
                self.explored.append(node.state)
                self.space_complexity += 1 # Keep node.state in explored
                child_nodes = self.expandNode(node)
                self.fringe += child_nodes
            
            else:
                self.max_space_complexity = max(self.max_space_complexity, self.space_complexity)
                self.space_complexity -= 1

        self.max_space_complexity = max(self.max_space_complexity, self.space_complexity)
        return 'Status: Solution not found\n'
    

    def ASearch(self, heuristic_id=1):
        '''
        Graph search using strategy A* search
        Return solution if it find one, o.w return a failure
        '''
        self.root_node.setHeuristic(heuristic_id)
        while self.fringe:
            node = self.fringe.pop(self.fringe.index(min(self.fringe, 
                                                        key=lambda x: x.path_cost + x.heuristic)))

            if self.problem.testGoal(node.state):
                self.result = node.path_cost
                self.max_space_complexity = max(self.max_space_complexity, self.space_complexity)
                return f'Status: Solution found\nOPTIMAL: {self.problem.checkObjective(node)}\nOverall duration: {node.path_cost}\n' \
                + str(self.problem.findSolution(node))
            
            elif node.state not in self.explored:
                self.explored.append(node.state)
                self.space_complexity += 1 # Keep node.state in explored
                child_nodes = self.expandNode(node)
                for i in range(len(child_nodes)):
                    child_nodes[i].setHeuristic(heuristic_id)
                self.fringe += child_nodes
            
            else:
                self.max_space_complexity = max(self.max_space_complexity, self.space_complexity)
                self.space_complexity -= 1

        self.max_space_complexity = max(self.max_space_complexity, self.space_complexity)
        return 'Status: Solution not found\n'

