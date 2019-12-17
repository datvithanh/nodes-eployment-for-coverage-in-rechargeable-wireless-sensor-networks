import os

import numpy as np
from inp import Cell, Target, Input
from argparse import ArgumentParser
MU = 65
SIGMA = 15

def random_targets(n, num_of_targets):
    targets = []
    coor = set()
    while(True):
        x, y = np.random.randint(0,n), np.random.randint(0,n)

        if (x,y) in coor:
            continue
        
        targets.append(Target(x,y))
        if len(targets) == num_of_targets:
            break

    return targets

if __name__ == "__main__":
    n = 30

    recharging_rates = np.random.normal(MU, SIGMA, n**2)
    recharging_rates = [min(90, max(10, tmp)) for tmp in recharging_rates]
    np.random.shuffle(recharging_rates)

    cells = []
    for i in range(30):
        for j in range(30):
            cells.append(Cell(i, j, recharging_rates[i*n+j]))

    # generate varius number of targets with fixed sensing range
    dir = 'data/targets'
    os.makedirs(dir, exist_ok=True)
    sensing_range = 5

    targets = []
    coor = set()

    for num_of_targets in range(9,136,9):
        # targets = random_targets(n, num_of_targets)
        while(True):
            x, y = np.random.randint(0,n), np.random.randint(0,n)

            if (x,y) in coor:
                continue
            
            targets.append(Target(x,y))
            if len(targets) == num_of_targets:
                break

        inp = Input(n, num_of_targets, sensing_range, targets, cells)
        inp.to_file(os.path.join(dir, f"sr{sensing_range}_not{num_of_targets}.json"))

    dir = 'data/ranges'
    os.makedirs(dir, exist_ok=True)
    num_of_targets = 63
    targets = random_targets(n, num_of_targets)
    # generate varius sensing range with fixed number of targets
    for sensing_range in range(3,16):
        inp = Input(n, num_of_targets, sensing_range, targets, cells)
        inp.to_file(os.path.join(dir, f"sr{sensing_range}_not{num_of_targets}.json"))





