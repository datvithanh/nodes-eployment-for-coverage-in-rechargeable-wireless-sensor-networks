import math

import json

#unit joules/h
class Constant:
    P = 150

class Point:
    def __init__(self, _x, _y):
        self.x = _x 
        self.y = _y

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y
        }

    def __repr__(self):
        return f"{self.__class__.__name__}({self.x}, {self.y})"

class Cell(Point):
    def __init__(self, _x, _y, _r):
        super().__init__(_x, _y)
        self.recharging_rate = _r

    @classmethod
    def from_dict(cls, di):
        return cls(di['x'], di['y'], di['recharging_rate'])

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "recharging_rate": self.recharging_rate
        }
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.x}, {self.y}, rr={self.recharging_rate})"

class Target(Point):
    def __init__(self, _x, _y):
        super().__init__(_x, _y)

    @classmethod
    def from_dict(cls, di):
        return cls(di['x'], di['y'])

class Input:
    def __init__(self, _n=30, _number_of_targets=9, _sensing_range=5, _target=None, _cells=None):
        self.n = _n
        self.number_of_targets = _number_of_targets
        self.sensing_range = _sensing_range
        self.targets = _target
        self.cells = _cells
        
        self.C = None
        self.T = None
        self.generate_neighbor_set()

    def generate_neighbor_set(self):
        self.C = {tmp: [] for tmp in self.targets}
        self.T = {tmp: [] for tmp in self.cells}
        
        for cell in self.cells:
            for target in self.targets:
                if distance(cell, target) <= self.sensing_range:
                    self.C[target].append(cell)
                    self.T[cell].append(target)

    @classmethod
    def from_file(cls, path):
        f = open(path)
        di = json.load(f)
        return cls.from_dict(di)

    @classmethod
    def from_dict(cls, di):
        n = di['n']

        number_of_targets = len(di['targets'])
        sensing_range = di['sensing_range']
        
        targets = []
        for tar in di['targets']:
            targets.append(Target.from_dict(tar))

        cells = []
        for ce in di['cells']:
            cells.append(Cell.from_dict(ce))

        return cls(n, number_of_targets, sensing_range, targets, cells)

    def to_dict(self):
        return {
            "n": self.n,
            "sensing_range": self.sensing_range,
            "targets": [tar.to_dict() for tar in self.targets],
            "cells": [ce.to_dict() for ce in self.cells]
        }

    def to_file(self, path):
        with open(path, 'w+') as f:
            ins_di = self.to_dict()
            ins_str = json.dumps(ins_di, indent=4)
            f.write(ins_str)

def distance(point1, point2):
    return math.sqrt((point1.x-point2.x)**2 + (point1.y-point2.y)**2)

if __name__ == "__main__":
    inp = Input.from_file('data/targets/sr9_not9.json')
    for target in inp.T[inp.cells[45]]:
        print(inp.cells[45])
        print(target)
    inp.to_file('out.json')
