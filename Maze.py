import math

inf = int(1e5)
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

    def dfs_recursive(self, path, src, dest, vis):
        c = Cell(src['x'], src['y'], self.n_x, self.n_y, self.grid)
        vis[src['x']][src['y']] = 1
        path.append(src)
        for e in c.neighbors:
            if e == dest:
                path.append(dest)
                return path
            elif not vis[src['s']][src['y']]:
                self.dfs_recursive(path, e, dest, vis)

    def dfs(self, src, dest):
        path = []
        vis = [[int(0) for _ in range(self.n_y)] for _ in range(self.n_x)]
        return self.dfs_recursive(path, src, dest, vis)

    def a_star(self, src, dest):
        src_cell = Cell(src['x'], src['y'], self.n_x, self.n_y, self.grid)
        src_cell.g = 0
        src_cell.h = self.heuristic(src_cell.get_xy())
        src_cell.parent = src_cell
        dest_cell = Cell(dest['x'], dest['y'], self.n_x, self.n_y, self.grid)
        open_list = [src_cell]
        closed_list = []
        done = 0

        while open_list:
            q = None
            f = inf
            index = 0
            for i in range(len(open_list)):
                if open_list[i].h + open_list[i].g > f:
                    q = open_list[i]
                    f = q.h + q.g
                    index = i
            open_list.pop(index)

            for neighbor in q.neighbors:
                tmp = Cell(neighbor['x'], neighbor['y'], self.n_x, self.n_y, self.grid)
                if dest_cell.x == tmp.x and dest_cell.y == tmp.y:
                    dest_cell.parent = q
                    done = 1
                    break
                tmp.g = q.g + 1
                tmp.h = self.heuristic(q.get_xy(), dest_cell.get_xy())

                next_neighbor = 0
                for cell in open_list:
                    if cell.x == tmp.x and cell.y == tmp.y and cell.g + cell.h < tmp.g + tmp.h:
                        next_neighbor = 1
                        break
                if next_neighbor:
                    continue
                for cell in closed_list:
                    if cell.x == tmp.x and cell.y == tmp.y and cell.g + cell.h < tmp.g + tmp.h:
                        next_neighbor = 1
                        break
                if next_neighbor:
                    continue
                tmp.parent = q
                open_list.append(tmp)
            if done is :
                break
            closed_list.append(q)

        if dest_cell.parent is None :
            return "No path found"

        else:
            path = []
            r = dest_cell
            while r.x != src_cell.x and r.y == src_cell.y:
                path.append(r)
                r = r.parent
            return path












