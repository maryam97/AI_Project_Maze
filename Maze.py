import math
import queue
inf = int(1e5)


class Cell:

    def __init__(self, x, y, n_x, n_y, table):
        self.x = x
        self.y = y
        self.n_y = n_y
        self.n_x = n_x
        self.g = None
        self.h = None
        self.f = None
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

    def __init__(self, table, heuristic='Manhattan'):
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
        return max(abs(src['x'] - dest['x']), abs(src['y'] - dest['y']))

    @staticmethod
    def euclidean(src, dest):
        return math.sqrt((src['x'] - dest['x'])**2 + (src['y'] - dest['y'])**2)

    def heuristic(self, src, dest):

        return {'Manhattan': lambda: self.manhattan(src, dest),
                'Diagonal': lambda: self.diagonal(src, dest),
                'Euclidean': lambda: self.euclidean(src, dest),
                }[self.h_method]()

    def dfs(self, src, dest):
        vis = []
        par = {}

        def dfs_recursive(src_):
            src_cell = Cell(src_['x'], src_['y'], self.n_x, self.n_y, self.grid)
            vis.append(src_)
            for e in src_cell.neighbors:
                if e not in vis:
                    par[(e['x'], e['y'])] = (src_cell.x, src_cell.y)
                    dfs_recursive(e)

        dfs_recursive(src)
        path = []
        src_tmp = (src['x'], src['y'])
        cell = (dest['x'], dest['y'])
        if par[cell]:
            while cell != src_tmp:
                path.append({'x': cell[0], 'y': cell[1]})
                cell = par[cell]
            path.append(src)
        return [path[::-1], len(path)]

    def ids(self, src, dest, limit):
        sol_len = 0
        path, length = self.dfs(src, dest)
        if len(path) <= limit + 1:
            sol_len = len(path)
        return [sol_len, path[::-1], len(path)]

    def bfs(self, src, dest):

        src_cell = Cell(src['x'], src['y'], self.n_x, self.n_y, self.grid)
        q = queue.Queue(maxsize=1000)
        q.put(src_cell)
        dist = [[inf for _ in range(self.n_y)] for _ in range(self.n_x)]
        dist[src['x']][src['y']] = 0
        par = {}
        vis_dest = False
        while not q.empty():
            if vis_dest:
                break
            front = q.get()
            for neigh in front.neighbors:
                if dist[neigh['x']][neigh['y']] == inf:
                    dist[neigh['x']][neigh['y']] = dist[front.x][front.y] + 1
                    new_cell = Cell(neigh['x'], neigh['y'], self.n_x, self.n_y, self.grid)
                    par[(neigh['x'], neigh['y'])] = (front.x, front.y)
                    if neigh == dest:
                        vis_dest = True
                        break
                    q.put(new_cell)

        path = []
        if vis_dest:
            src_tmp = (src['x'], src['y'])
            cell = (dest['x'], dest['y'])
            while cell != src_tmp:
                path.append({'x': cell[0], 'y': cell[1]})
                cell = par[cell]
            path.append(src)
        return [path[::-1], len(path)]

    def a_star(self, src, dest):
        src_cell = Cell(src['x'], src['y'], self.n_x, self.n_y, self.grid)
        src_cell.g = 0
        src_cell.h = self.heuristic(src_cell.get_xy(), dest)
        src_cell.f = src_cell.g + src_cell.h
        src_cell.parent = src_cell
        dest_cell = Cell(dest['x'], dest['y'], self.n_x, self.n_y, self.grid)
        open_list = [src_cell]
        closed_list = []
        done = 0

        while open_list:
            open_list.sort(key=lambda x: x.f)
            q = open_list[0]
            open_list.pop(0)

            for neighbor in q.neighbors:
                tmp = Cell(neighbor['x'], neighbor['y'], self.n_x, self.n_y, self.grid)
                if dest_cell.x == tmp.x and dest_cell.y == tmp.y:
                    dest_cell.parent = q
                    done = 1
                    break
                tmp.g = q.g + 1
                tmp.h = self.heuristic(q.get_xy(), dest_cell.get_xy())
                tmp.f = tmp.g + tmp.h
                next_neighbor = 0
                for cell in open_list:
                    if cell.get_xy() == tmp.get_xy() and cell.f < tmp.f:
                        next_neighbor = 1
                        break
                if next_neighbor:
                    continue
                for cell in closed_list:
                    if cell.get_xy() == tmp.get_xy() and cell.f < tmp.f:
                        next_neighbor = 1
                        break
                if next_neighbor:
                    continue
                tmp.parent = q
                open_list.append(tmp)
            if done == 1:
                break
            closed_list.append(q)

        if dest_cell.parent is None:
            return [[], -1]

        else:
            path = []
            r = dest_cell
            while r.get_xy() != src_cell.get_xy():
                path.append(r.get_xy())
                r = r.parent
            path.append(src_cell)
            return [[item for item in reversed(path)], len(path)]

    def rbfs(self, src, dest):
        src_cell = Cell(src['x'], src['y'], self.n_x, self.n_y, self.grid)
        src_cell.g = 0
        src_cell.h = self.heuristic(src_cell.get_xy(), dest)
        src_cell.f = src_cell.g + src_cell.h
        src_cell.parent = src_cell
        dest_cell = Cell(dest['x'], dest['y'], self.n_x, self.n_y, self.grid)

        def rbfs_recursive(node, f_in):
            if node.get_xy() == dest_cell.get_xy():
                return node, None
            neighbor_nodes = []
            for neighbor in node.neighbors:
                tmp = Cell(neighbor['x'], neighbor['y'], self.n_x, self.n_y, self.grid)
                neighbor_nodes.append(tmp)
            if len(neighbor_nodes) == 0:
                return None, inf
            for i in range(len(neighbor_nodes)):
                neighbor_nodes[i].g = node.g + 1
                neighbor_nodes[i].h = self.heuristic(neighbor_nodes[i].get_xy(), dest_cell.get_xy())
                neighbor_nodes[i].f = max(neighbor_nodes[i].g + neighbor_nodes[i].h, node.f)

            neighbor_nodes.sort(key=lambda x: x.f)
            best = neighbor_nodes[0]
            try:
                alt = neighbor_nodes[1]
            except IndexError:
                alt = Cell(0, 0, self.n_x, self.n_y, self.grid)
                alt.f = inf
            if best.f > f_in:
                return None, best.f
            result, best.f = rbfs_recursive(best, min(f_in, alt.f))
            if result is not None:
                best.parent = node
                return result, None
            else:
                return None, None

        result_out, bestf = rbfs_recursive(src_cell, inf)

        if result_out is None:
            return [[], -1]
        else:
            path = []
            r = result_out
            while r.get_xy() != src_cell.get_xy():
                path.append(r.get_xy())
                r = r.parent
            path.append(src_cell)
            return [[item for item in reversed(path)], len(path)]