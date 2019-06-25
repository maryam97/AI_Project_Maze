import math


class Cell:

    def __init__(self, x, y, n_x, n_y, table):
        self.x = x
        self.y = y
        self.n_y = n_y
        self.n_x = n_x
        self.g = None
        self.h = None
        self.parent = None
        self.neighbors = []
        if x - 1 >= 0 and table[x-1][y] != 1:
            self.neighbors.append({'x': x-1, 'y': y})
        if x + 1 < self.n_x and table[x+1][y] != 1:
            self.neighbors.append({'x': x+1, 'y': y})
        if y - 1 >= 0 and table[x][y-1] != 1:
            self.neighbors.append({'x': x, 'y': y-1})
        if y + 1 < self.n_y and table[x][y+1] != 1:
            self.neighbors.append({'x': x, 'y': y+1})

    def get_xy(self):
        return {'x': self.x, 'y': self.y}


class Path:

    def __init__(self, table, heuristic):
        self.grid = table
        self.h_method = heuristic
        self.optimal_solution = []
        self.n_x = len(table)
        self.n_y = len(table[0])

    @staticmethod
    def manhattan(src, dest):
        return abs(src['x'] - dest['x']) + abs(src['y'] - dest['y'])

    @staticmethod
    def diagonal(src, dest):
        return max(abs(src['x'] - dest['x']) , abs(src['y'] - dest['y']))

    @staticmethod
    def euclidean(src, dest):
        return math.sqrt((src['x'] - dest['x'])**2 + (src['y'] - dest['y'])**2)

    def heuristic(self, src, dest):

        return {'Manhattan': lambda: self.manhattan(src, dest),
                'Diagonal': lambda: self.diagonal(src, dest),
                'euclidean': lambda: self.euclidean(src, dest),
                }[self.h_method]()

    def a_star(self, src, dest):
        src_cell = Cell(src['x'], src['y'], self.n_x, self.n_y, self.grid)
        src_cell.g = 0
        src_cell.h = self.heuristic(src_cell.get_xy())
        open_list = [src_cell]
        closed_list = []





