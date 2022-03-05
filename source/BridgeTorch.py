import Problem

import itertools
import bisect


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
            raise Exception('Invalid problem! Recheck the length of the two inputs.')
        
        self.durations = durations
        self.init_state = init_state
        self.goal = [1] * len(durations)
        self.objective = objective


    def findSuccessorFn(self, state):
        '''
        Parameter: Node.state (list)
        Return   : transitions (list)

        Search all the possible result states that can be reached using a simple
        action from the current state 
        '''
        cur_state = state[:]
        transitions = []
        Act(state[-1], abs(state[-1] - 1))

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

        return transitions


    def findStepCost(self, action):
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


    def findHeuristic(self, state, id=2):
        '''
        Parameter: Node.state (list)
        Reuturn  : max_time (integer)

        1: Estimate the cost from the current state to the goal by the time to cross
        bridge of the slowest person on the side 0 at this moment
        2: Estimate the cost from the current state to the goal by the sum of the time 
        of each pair in side 0 crossing bridge
        '''
        if id == 1:
            people_pos = state[:-1]
            max_time = 0
            for i in range(len(people_pos)):
                if people_pos[i] == 0:
                    max_time = max(max_time, self.durations[i])
        
            return max_time
        elif id == 2:
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


    def findSolution(self, node):
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


    def testGoal(self, state):
        return state[:-1] == self.goal


    def checkObjective(self, node):
        if self.objective == None:
            return 'No data'
        return self.objective == node.path_cost