from random import randrange
import csv

# add package path
import sys
import os
sys.path.insert(0, os.getcwd())

from search.BridgeTorch import BridgeTorch
from search.Solver import Solver

data_address = f'master\\performance\\' # address the folder to store the sampling data


def calculateAverage(num):
    sum_num = 0
    for t in num:
        sum_num = sum_num + t           

    avg = sum_num / len(num)
    return avg


class Test:
    def __init__(self, n_samples):
        self.n_samples = n_samples

        self.objective = []
        self.runtime = []
        self.time_complexity = []
        self.space_complexity = []

        self.header = ['UCS', 'BB', 'A*', 'IDA*', 'BFS', 'DFS']
    

    def genRandomInput(self, n):
        '''
        Paramters: n (int), the number of people involved
        Return   : A tuple of walk_time and initial state, which define an instance
        '''

        inp_durations = ''

        for _ in range(n):
            inp_duration = randrange(1, 101) # 1 -> 100
            inp_durations += str(inp_duration) + ' '
        inp_durations = inp_durations.strip()

        inp_states = ''
        for _ in range(n):
            inp_state = randrange(0, 2)
            inp_states += str(inp_state) + ' '

        if sum(list(map(int, inp_states.split()))) == 0:
            inp_states += '0'
        else:
            candle = randrange(0, 2)
            inp_states += str(candle)
        
        return (inp_durations, inp_states)
    

    def genWorstCaseInput(self, n):
        '''
        Paramters: n (int), the number of people involved
        Return   : A tuple of walk_time and initial state, which define an instance
        '''

        inp_durations = ''

        for _ in range(n):
            inp_duration = randrange(5, 51) # 5 -> 50
            inp_durations += str(inp_duration) + ' '
        inp_durations = inp_durations.strip()

        inp_states = ''
        for _ in range(n + 1):
            inp_state = 0
            inp_states += str(inp_state) + ' '
        inp_states.strip()
        
        return (inp_durations, inp_states)

    
    def writeData(self, inp_size, datatype): # file addresses depend on each personal device
        if datatype == 'obj':
            with open(data_address + f'size{inp_size}\\obj.csv', 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)

                # write the header
                writer.writerow(self.header)

                # write multiple rows
                writer.writerows(self.objective)
        
        elif datatype == 'run':
            with open(data_address + f'size{inp_size}\\runtime.csv', 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)

                # write the header
                writer.writerow(self.header)

                # write multiple rows
                writer.writerows(self.runtime)

        elif datatype == 'time':
            with open(data_address + f'size{inp_size}\\timecplx.csv', 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)

                # write the header
                writer.writerow(self.header)

                # write multiple rows
                writer.writerows(self.time_complexity)
        
        elif datatype == 'space':
            with open(data_address + f'size{inp_size}\\spacecplx.csv', 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)

                # write the header
                writer.writerow(self.header)

                # write multiple rows
                writer.writerows(self.space_complexity)
    

    def Sampling(self, inp_size):
        for i in range(self.n_samples):
            durations, init_state = self.genRandomInput(inp_size)
            problem = BridgeTorch(durations, init_state)
            print(f'Instance n={inp_size}/[{durations}, {init_state}]: Testing')

            obj0, run0, time0, space0 = Solver(problem, 'Graph', 'UCS').StatsSolve() if inp_size < 13 else [None, None, None, None]
            #obj1, run1, time1, space1 = Solver(problem, 'Graph', 'A*').StatsSolve() if inp_size <= 13 else [None, None, None, None]
            #obj2, run2, time2, space2 = Solver(problem, 'Tree', 'IDA*').StatsSolve() if inp_size < 10 else [None, None, None, None]
            obj3, run3, time3, space3 = Solver(problem, 'Tree', 'BB', heuristic_id=2).StatsSolve() if inp_size <= 10 else [None, None, None, None]
            obj4, run4, time4, space4 = Solver(problem, 'Graph', 'A*', heuristic_id=2).StatsSolve() if inp_size <= 13 else [None, None, None, None]
            obj5, run5, time5, space5 = Solver(problem, 'Tree', 'IDA*', heuristic_id=2).StatsSolve() if inp_size <= 8 else [None, None, None, None]
            obj6, run6, time6, space6 = Solver(problem, 'Graph', 'BFS').StatsSolve() if inp_size <= 13 else [None, None, None, None]
            obj7, run7, time7, space7 = Solver(problem, 'Graph', 'DFS').StatsSolve() if inp_size <= 100 else [None, None, None, None]

            self.objective.append([obj0, obj3, obj4, obj5, obj6, obj7])
            self.runtime.append([run0, run3, run4, run5, run6, run7])
            self.time_complexity.append([time0, time3, time4, time5, time6, time7])
            self.space_complexity.append([space0, space3, space4, space5, space6, space7])

        self.writeData(inp_size, datatype='obj')
        self.writeData(inp_size, datatype='run')
        self.writeData(inp_size, datatype='time')
        self.writeData(inp_size, datatype='space')