import math
import os

from ortools.sat.python import cp_model

from inp import Input, Constant

def ilp(inp_path):
    inp = Input.from_file(inp_path)

    max_sensors = [[0]*inp.n for _ in range(inp.n)]
    recharging_rate = [[0]*inp.n for _ in range(inp.n)]
    for cell in inp.cells:
        if len(inp.T[cell]) == 0:
            max_sensors[cell.x][cell.y] = 0 
            continue
        max_sensors[cell.x][cell.y] = math.ceil(Constant.P/cell.recharging_rate)
        recharging_rate[cell.x][cell.y] = cell.recharging_rate

    targets = []
    target_cells = [[] for _ in range(inp.number_of_targets)]
    for ind, target in enumerate(inp.targets):
        targets.append((target.x, target.y))
        for cell in inp.C[target]:
            target_cells[ind].append((cell.x, cell.y))

    model = cp_model.CpModel()

    x = []
        
    for i in range(inp.n):
        x.append([model.NewIntVar(0, max_sensors[i][j] ,f'x_{i}_{j}') for j in range(inp.n)])

    for cells in target_cells:
        model.Add(sum([int(recharging_rate[i][j]*1e3)*x[i][j] for i,j in cells]) >= Constant.P*1000)

    model.Minimize(sum([val for val in [sum(row) for row in x]]))

    solver = cp_model.CpSolver()
    solver.Solve(model)

    c = [[] for _ in range(inp.n)]
    for i in range(inp.n):
        for j in range(inp.n):
            c[i].append(solver.Value(x[i][j]))
    
    return sum([sum(tmp) for tmp in c])

if __name__ == "__main__":

    for exp in ['ranges', 'targets']:
        dir = os.path.join('data', exp)
        f = open(os.path.join('result', exp + '.txt'), 'w+')
        fns = sorted(os.listdir(dir), key=lambda x: (len(x), x))

        for fn in fns:
            print(f"SOLVING {fn}")
            f.write(f'{os.path.join(dir, fn)} {ilp(os.path.join(dir, fn))}\n')