import search

durations = '1 2 5 8' # walk time of each person
init_state = '0 0 0 0 0' # their position
objective = 34 # this instance's optimal solution
problem = search.BridgeTorch(durations, init_state, objective)

print(search.Solver(problem, 'Graph', 'A*', heuristic_id=2).Solve()) # graph search, A* search strategy