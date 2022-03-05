from GraphSearch import GraphSearch


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
            if self.problem.testGoal(node.state):
                return "FOUND"
            min = 1e15 # INF
            child_nodes = self.expandNode(node)
            for succ in child_nodes:
                succ.setHeuristic(heuristic_id)
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
        
        self.root_node.setHeuristic(heuristic_id)
        threshold = self.root_node.heuristic + self.root_node.path_cost
        while self.fringe: 
            t = search(self.fringe, threshold)
            if t == "FOUND":
                node = self.fringe[-1]
                self.result = node.path_cost
                self.max_space_complexity = max(self.max_space_complexity, self.space_complexity)
                return f'Status: Solution found\nOPTIMAL: {self.problem.checkObjective(node)}\nOverall duration: {node.path_cost}\n' \
                + str(self.problem.findSolution(node))
            if t == 1e15:
                self.max_space_complexity = max(self.max_space_complexity, self.space_complexity)
                return "Status: Solution not found\n"
            threshold = t
            self.space_complexity = 1
    

    def BranchBound(self, heuristic_id = 1):
        def Branch(node):
            nonlocal f_opt, x_opt
            for succ in self.expandNode(node):
                succ.setHeuristic(heuristic_id)
                if self.problem.testGoal(succ.state) and succ.heuristic + succ.path_cost < f_opt:
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
        self.root_node.setHeuristic(heuristic_id)

        if self.problem.testGoal(self.root_node.state):
            x_opt = self.root_node
            self.max_space_complexity = max(self.max_space_complexity, self.space_complexity)
            self.result = x_opt.path_cost
            return f'Status: Solution found\nOPTIMAL: {self.problem.checkObjective(x_opt)}\nOverall duration: {x_opt.path_cost}\n' \
            + str(self.problem.findSolution(x_opt))

        Branch(self.root_node)
        if x_opt == None:
            return 'Status: Solution not found\n'

        self.space_complexity += x_opt.depth
        self.max_space_complexity = max(self.max_space_complexity, self.space_complexity)
        self.result = x_opt.path_cost
        return f'Status: Solution found\nOPTIMAL: {self.problem.checkObjective(x_opt)}\nOverall duration: {x_opt.path_cost}\n' \
        + str(self.problem.findSolution(x_opt))
