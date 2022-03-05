from source.Solver import Solver
from source.BridgeTorch import BridgeTorch


durations = '1 2 5 8'
init_state = '0 0 0 0 0'
objective = 34 # People have found this instance's optimal solution
problem = BridgeTorch(durations, init_state, objective)

print(Solver(problem, 'Graph', 'A*', heuristic_id=2).Solve())