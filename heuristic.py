import math
import os

from inp import Input, Constant

def heuristic(inp_path):
    inp = Input.from_file(inp_path)

    result = [[0]*inp.n for _ in range(inp.n)]
    short_fall = {}
    while True:
        stop = True
        for target in inp.targets:
            sum_rr = 0
            for cell in inp.C[target]:
                sum_rr += result[cell.x][cell.y]*cell.recharging_rate
            short_fall[(target.x, target.y)] = max(Constant.P - sum_rr, 0)
            if sum_rr < Constant.P:
                stop = False
                
        if stop:
            break
        
        best_coor = (0,0)
        dmax = 0 
        
        for cell in inp.cells:
            d = 0
            for target in inp.T[cell]:
                d += min(short_fall[(target.x, target.y)], cell.recharging_rate)
            if d > dmax:
                dmax = d
                best_coor = (cell.x, cell.y)
                
        result[best_coor[0]][best_coor[1]] += 1
    return sum([sum(tmp) for tmp in result])

if __name__ == "__main__":

    for exp in ['ranges', 'targets']:
        dir = os.path.join('data', exp)
        f = open(os.path.join('result', exp + '.txt'), 'w+')
        fns = sorted(os.listdir(dir), key=lambda x: (len(x), x))

        for fn in fns:
            inp = Input.from_file(os.path.join(dir, fn))
            print(f"SOLVING {fn}", len(inp.targets))
            # f.write(f'{os.path.join(dir, fn)} {heuristic(os.path.join(dir, fn))}\n')