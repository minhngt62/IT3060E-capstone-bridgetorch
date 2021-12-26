#@title 00 - Import libraries
import itertools
import bisect
from time import time


#@title 01 - Class Problem
class Problem:
  pass

class BridgeTorch(Problem):
  def __init__(self, durations, init_state, objective=None):
    '''
    Model the problem Bridge and Torch follows 2 parameters:
    - durations  (list): Contain individuals' time taken to cross the bridge 
    - init_state (list): Contain binary elements which represent the place of
    individuals and the candle (the last element) at the moment
    '''

    durations = list(map(int, durations.split()))
    init_state = list(map(int, init_state.split()))

    if len(durations) + 1 != len(init_state):
      raise Exception('Invalid problem! Check the length of 2 inputs.')

    self.durations = durations
    self.init_state = init_state
    self.goal = [1] * len(durations)

    self.objective = objective


  def SuccessorFn(self, state):
    '''
    Parameter: Node.state (list)
    Return   : transitions (list)

    Search all the possible result states that can be reached using a simple
    action from the current state 
    '''

    cur_state = state[:]
    transitions = []

    def Act(origin, goal):
        if origin == 0 and len(cur_state) == sum(cur_state) + 2:
            for person_z in range(len(cur_state) - 1):
                if cur_state[person_z] == origin:
                    result_state = cur_state[:]
                    result_state[person_z] = goal
                    result_state[-1] = goal
                    action = [[person_z], (origin, goal)] # form of action
                    transitions.append((action, result_state)) # form of transition
          
        elif goal == 1:
            candidates = itertools.combinations(list(range(len(self.durations))), 2)
            for person_x, person_y in candidates:
                if cur_state[person_x] == origin and cur_state[person_y] == origin:
                    result_state = cur_state[:]
                    result_state[person_x] = goal
                    result_state[person_y] = goal
                    result_state[-1] = goal
                    action = [[person_x, person_y], (origin, goal)] # form of action
                    transitions.append((action, result_state)) # form of transition
        elif goal == 0:
            for person_z in range(len(cur_state) - 1):
                if cur_state[person_z] == origin:
                    result_state = cur_state[:]
                    result_state[person_z] = goal
                    result_state[-1] = goal
                    action = [[person_z], (origin, goal)] # form of action
                    transitions.append((action, result_state)) # form of transition

    Act(state[-1], abs(state[-1] - 1))
    return transitions
  

  def Heuristic1(self, state):
    '''
    Parameter: Node.state (list)
    Reuturn  : max_time (integer)

    Estimate the cost from the current state to the goal by the time to cross
    bridge of the slowest person on the side 0 at this moment
    '''

    people_pos = state[:-1]
    max_time = 0
    for i in range(len(people_pos)):
      if people_pos[i] == 0:
        max_time = max(max_time, self.durations[i])
    
    return max_time

  def Heuristic2(self, state):
    '''
    Parameter: Node.state (list)
    Reuturn  : estimated (integer)

    Estimate the cost from the current state to the goal by the sum of the time 
    of each pair in side 0 crossing bridge
    '''

    people_pos = state[:-1]
    remain_walktime = []
    for i in range(len(people_pos)):
      if people_pos[i] == 0:
        bisect.insort(remain_walktime, self.durations[i])

    estimated = 0
    l = len(remain_walktime)
    for i in range(l-1, -1, -2):
      estimated += remain_walktime[i]
    return estimated

  
  def StepCost(self, action):
    '''
    Parameter: Node.action (list - list, tuple)
    Return   : cost (integer)

    Find the cost of a single action following the rule of problem
    '''

    crossers = action[0]
    if len(crossers) == 2:
      person_x, person_y = crossers
      cost = max(self.durations[person_x], self.durations[person_y])
    else:
      person_z = crossers[0]
      cost = self.durations[person_z]
  
    return cost
  

  def Solution(self, node):
    '''
    Parameter: node (type Node)
    Return   : final answer for the problem (string)

    Backtrack and return the status and the best method to cross the bridge
    '''

    if node.state == self.init_state:
      return '\nThe method:\n'
    
    start, end = node.action[1]
    if len(node.action[0]) == 2:
      person1, person2 = node.action[0]
      if start == 0:
        return self.Solution(node.parent) + f'{person1+1} {person2+1} ->\n'
      else:
        return self.Solution(node.parent) + f'{person1+1} {person2+1} <-\n'
    elif len(node.action[0]) == 1:
      person1 = node.action[0][0]
      if start == 0:
        return self.Solution(node.parent) + f'{person1+1} ->\n'
      else:
        return self.Solution(node.parent) + f'{person1+1} <-\n'
  

  def GoalTest(self, state):
    return state[:-1] == self.goal
  
  
  def CheckObjective(self, node):
    if self.objective == None:
      return 'No data'
    return self.objective == node.path_cost


#@title 02 - Class Node
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
    
    self.path_cost = parent.path_cost + problem.StepCost(action)
    self.heuristic = None
  

  def SetHeuristic(self, heuristic_id = 1):
    '''
    Parameters: None
    Return    : None

    Find and set the heuristic of the current state for the node if needed
    by using method Heuristic() of Problem()
    '''
    if heuristic_id == 1:
      self.heuristic = self.problem.Heuristic1(self.state)
    elif heuristic_id == 2:
      self.heuristic = self.problem.Heuristic2(self.state)

class Root(Node):
  def __init__(self, problem):
    self.problem = problem
    self.state = problem.init_state[:]
    self.parent = None
    self.action = None
    self.depth = 0

    self.path_cost = 0
    self.heuristic = None


#@title 03 - Class GraphSearch
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


    def Expand(self, node):
        '''
        Parameters: node (type Node)
        Return    : successors (list)

        Construct a list of child nodes from the current node 
        '''

        successors = []
        for action, result_state in self.problem.SuccessorFn(node.state):
            new_node = Node(self.problem, result_state, node, action)
            self.time_complexity += 1
            self.space_complexity += 1
            successors.append(new_node)

        return successors

    def Tracking(self):
        '''
        Used in some cases when the search takes too much time to run so as to track
        the search progress
        '''
        if self.time_complexity % 1e6 == 0:
            print('Reach', self.time_complexity, 'generated')
        
        if self.space_complexity % 1e6 == 0:
            print('Reach', self.space_complexity, 'kept in memory')

    
    def BreathFirstSearch(self):
        '''
        Graph search using strategy Uniform cost search
        Return solution if it find one, o.w return a failure
        '''
        while self.fringe:
            node = self.fringe.pop(0)
            
            if self.problem.GoalTest(node.state):
                self.result = node.path_cost
                self.max_space_complexity = max(self.max_space_complexity, self.space_complexity)
                return f'Status: Solution found\nOPTIMAL: {self.problem.CheckObjective(node)}\nOverall duration: {node.path_cost}\n' \
                + str(self.problem.Solution(node))
            
            if node.state not in self.explored:
                self.explored.append(node.state)
                self.space_complexity += 1 # Keep node.state in explored
                child_nodes = self.Expand(node)
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
            
            if self.problem.GoalTest(node.state):
                self.result = node.path_cost
                self.max_space_complexity = max(self.max_space_complexity, self.space_complexity)
                return f'Status: Solution found\nOPTIMAL: {self.problem.CheckObjective(node)}\nOverall duration: {node.path_cost}\n' \
                + str(self.problem.Solution(node))
            
            if node.state not in self.explored:
                self.explored.append(node.state)
                self.space_complexity += 1 # Keep node.state in explored
                child_nodes = self.Expand(node)
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
            
            if self.problem.GoalTest(node.state):
                self.result = node.path_cost
                self.max_space_complexity = max(self.max_space_complexity, self.space_complexity)
                return f'Status: Solution found\nOPTIMAL: {self.problem.CheckObjective(node)}\nOverall duration: {node.path_cost}\n' \
                + str(self.problem.Solution(node))
            
            elif node.state not in self.explored:
                self.explored.append(node.state)
                self.space_complexity += 1 # Keep node.state in explored
                child_nodes = self.Expand(node)
                self.fringe += child_nodes
            
            else:
                self.max_space_complexity = max(self.max_space_complexity, self.space_complexity)
                self.space_complexity -= 1

        self.max_space_complexity = max(self.max_space_complexity, self.space_complexity)
        return 'Status: Solution not found\n'
  

    def ASearch(self, heuristic_id = 1):
        '''
        Graph search using strategy A* search
        Return solution if it find one, o.w return a failure
        '''
        self.root_node.SetHeuristic(heuristic_id)
        while self.fringe:
            node = self.fringe.pop(self.fringe.index(min(self.fringe, 
                                                        key=lambda x: x.path_cost + x.heuristic)))

            if self.problem.GoalTest(node.state):
                self.result = node.path_cost
                self.max_space_complexity = max(self.max_space_complexity, self.space_complexity)
                return f'Status: Solution found\nOPTIMAL: {self.problem.CheckObjective(node)}\nOverall duration: {node.path_cost}\n' \
                + str(self.problem.Solution(node))
            
            elif node.state not in self.explored:
                self.explored.append(node.state)
                self.space_complexity += 1 # Keep node.state in explored
                child_nodes = self.Expand(node)
                for i in range(len(child_nodes)):
                    child_nodes[i].SetHeuristic(heuristic_id)
                self.fringe += child_nodes
            
            else:
                self.max_space_complexity = max(self.max_space_complexity, self.space_complexity)
                self.space_complexity -= 1

        self.max_space_complexity = max(self.max_space_complexity, self.space_complexity)
        return 'Status: Solution not found\n'


#@title 02 - Class TreeSearch
class TreeSearch(GraphSearch):
  def __init__(self, problem):
    '''
    Inherit from GraphSearch(), except self.explored is none since tree search
    does not memorize what it have expanded

    Formulate the tree for searching. The way of formulation is replied on the 
    each problem. In our scope, it is Bridge and Torch.
    '''

    GraphSearch.__init__(self, problem)
    self.explored = None
  

  def IDASearch(self, heuristic_id = 1):
    '''
    Tree search using strategy IDA search
    Return solution if it find one, o.w return a failure
    '''

    def search(fringe, threshold):
      node = fringe[-1]
      if node.path_cost + node.heuristic > threshold:
        return node.path_cost + node.heuristic
      if self.problem.GoalTest(node.state):
          return "FOUND"
      min = 1e15 # INF
      child_nodes = self.Expand(node)
      for succ in child_nodes:
        succ.SetHeuristic(heuristic_id)
        fringe.append(succ)
        t = search(fringe, threshold)
        if t == "FOUND":
          return "FOUND"
        if t < min:
          min = t
        fringe.pop()
        self.max_space_complexity = max(self.max_space_complexity, self.space_complexity)
        self.space_complexity -= 1
      return min
    
    self.root_node.SetHeuristic(heuristic_id)
    threshold = self.root_node.heuristic + self.root_node.path_cost
    while self.fringe: 
      t = search(self.fringe, threshold)
      if t == "FOUND":
        node = self.fringe[-1]
        self.result = node.path_cost
        self.max_space_complexity = max(self.max_space_complexity, self.space_complexity)
        return f'Status: Solution found\nOPTIMAL: {self.problem.CheckObjective(node)}\nOverall duration: {node.path_cost}\n' \
        + str(self.problem.Solution(node))
      if t == 1e15:
        self.max_space_complexity = max(self.max_space_complexity, self.space_complexity)
        return "Status: Solution not found\n"
      threshold = t
      self.space_complexity = 1
    

  def BranchBound(self, heuristic_id = 1):
    def Branch(node):
      nonlocal f_opt, x_opt
      for succ in self.Expand(node):
        succ.SetHeuristic(heuristic_id)
        if self.problem.GoalTest(succ.state) and succ.heuristic + succ.path_cost < f_opt:
          f_opt = succ.heuristic + succ.path_cost
          x_opt = succ
        else:
          if succ.heuristic + succ.path_cost < f_opt:
            Branch(succ)
        self.max_space_complexity = max(self.max_space_complexity, self.space_complexity)
        self.space_complexity -= 1 
      return 
    
    f_opt = 1e15
    x_opt = None
    self.root_node.SetHeuristic(heuristic_id)

    if self.problem.GoalTest(self.root_node.state):
        x_opt = self.root_node
        self.max_space_complexity = max(self.max_space_complexity, self.space_complexity)
        self.result = x_opt.path_cost
        return f'Status: Solution found\nOPTIMAL: {self.problem.CheckObjective(x_opt)}\nOverall duration: {x_opt.path_cost}\n' \
        + str(self.problem.Solution(x_opt))

    Branch(self.root_node)
    if x_opt == None:
        return 'Status: Solution not found\n'

    self.space_complexity += x_opt.depth
    self.max_space_complexity = max(self.max_space_complexity, self.space_complexity)
    self.result = x_opt.path_cost
    return f'Status: Solution found\nOPTIMAL: {self.problem.CheckObjective(x_opt)}\nOverall duration: {x_opt.path_cost}\n' \
    + str(self.problem.Solution(x_opt))


#@title 04 - Class SearchSolver
class SearchSolver:
    def __init__(self, problem, algorithm, strategy, heuristic_id=1):
        '''
        Parameters: problem (type Problem), algorithm (str), strategy (str)
        Attributes: 
        - self.problem (Problem): The model of the problem
        - self.built_in (dict): The dictionary of search algorithms developed
        - self.algorithm (str): The algorithm used (Tree or Graph)
        - self.strategy (str): The search strategy implemented

        Simplify the procedure to call methods for searching. With SearchSolver(), 
        just have to call: SearchSolver().Solve()
        '''

        self.problem = problem
        self.built_in = {'Graph': ['UCS', 'A*', 'DFS', 'BFS'], \
                            'Tree': ['IDA*', 'BB']}

        if algorithm not in self.built_in:
            raise Exception('AlgoUndefi: The algorithm has not been built yet!')
        elif strategy not in self.built_in[algorithm]:
            raise Exception('StraUndefi: The strategy has not been built yet!')

        self.algorithm = algorithm
        self.strategy = strategy

        self.heuristic_id = heuristic_id

    def Solve(self):
        '''
        Parameters: None
        Return : Result of a problem instance after searching is complete (str)

        Solve the problem using the algorithm and strategy chosen.
        '''

        if self.algorithm == 'Graph':
            solver = GraphSearch(self.problem)
            if self.strategy == 'BFS':
                start = time()
                solution = solver.BreathFirstSearch()
                end = time()
            elif self.strategy == 'DFS':
                start = time()
                solution = solver.DepthFirstSearch()
                end = time()
            if self.strategy == 'UCS':
                start = time()
                solution = solver.UniformCostSearch()
                end = time()
            elif self.strategy == 'A*':
                start = time()
                solution = solver.ASearch(self.heuristic_id)
                end = time()
        elif self.algorithm == 'Tree':
            solver = TreeSearch(self.problem)
            if self.strategy == 'IDA*':
                start = time()
                solution = solver.IDASearch(self.heuristic_id)
                end = time()
            elif self.strategy == 'BB':
                start = time()
                solution = solver.BranchBound(self.heuristic_id)
                end = time()
        
        return f'Instance n={len(self.problem.durations)}: {self.problem.durations}; {self.problem.init_state}\n' + \
        str(solution) + '\n' + f'Running time: {end - start}\n' + \
        f'Time complexity: {solver.time_complexity}\n' + \
        f'Space complexity: {solver.space_complexity}\n' + \
        f'Max space complexity: {solver.max_space_complexity}'

    def StatsSolve(self):
        if self.algorithm == 'Graph':
            solver = GraphSearch(self.problem)
            if self.strategy == 'BFS':
                start = time()
                solution = solver.BreathFirstSearch()
                end = time()
            elif self.strategy == 'DFS':
                start = time()
                solution = solver.DepthFirstSearch()
                end = time()
            elif self.strategy == 'UCS':
                start = time()
                solution = solver.UniformCostSearch()
                end = time()
            elif self.strategy == 'A*':
                start = time()
                solution = solver.ASearch(self.heuristic_id)
                end = time()
        elif self.algorithm == 'Tree':
            solver = TreeSearch(self.problem)
            if self.strategy == 'IDA*':
                start = time()
                solution = solver.IDASearch(self.heuristic_id)
                end = time()
            elif self.strategy == 'BB':
                start = time()
                solution = solver.BranchBound(self.heuristic_id)
                end = time()
        
        runtime = end - start
        return solver.result, runtime, solver.time_complexity, solver.max_space_complexity


#@title O - Test
if __name__ == '__main__':
    durations = '1 2 5 8'
    init_state = '0 0 0 0 0'
    objective = 34 # People have found this instance's optimal solution
    problem = BridgeTorch(durations, init_state, objective)

    print(SearchSolver(problem, 'Graph', 'A*', heuristic_id=2).Solve())