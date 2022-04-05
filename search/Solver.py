from .GraphSearch import GraphSearch
from .TreeSearch import TreeSearch

from time import time


class Solver:
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

