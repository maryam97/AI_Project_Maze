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

    def __init__(self, table, heuristic='Manhattan', search='A*'):
        self.grid = table
        self.h_method = heuristic
        self.search_method = search
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
        expand = []

        def dfs_recursive(src_):
            src_cell = Cell(src_['x'], src_['y'], self.n_x, self.n_y, self.grid)
            vis.append(src_)
            expand.append(src_)
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
        return [path[::-1], len(path), len(expand)]

    def ids(self, src, dest):
        par = {}
        vis = []
        non_block = self.n_y * self.n_x - sum([sum(self.grid[j]) for j in range(self.n_x)])

        def ids_recursive(lim):

            stack = list()
            stack.append((src, 0))
            vis.append(src)
            reach = 0
            expand = 0
            while len(stack):
                node, d = stack.pop()
                node_cell = Cell(node['x'], node['y'], self.n_x, self.n_y, self.grid)
                expand += 1
                if lim > d:
                    break
                else:
                    for e in node_cell.neighbors:
                        if e not in vis:
                            par[(e['x'], e['y'])] = (node_cell.x, node_cell.y)
                            vis.append(e)
                            stack.append((e, d + 1))
                        if e == dest:
                            reach = 1
                            break
                        elif len(vis) >= non_block:
                            reach = -1
                            break

            return reach, expand

        ex = 0
        for l in range(inf):
            par.clear()
            vis.clear()
            re, ex = ids_recursive(l)
            if re == 1 or re == -1:
                break

        path = []
        src_tmp = (src['x'], src['y'])
        cell = (dest['x'], dest['y'])
        if par[cell]:
            while cell != src_tmp:
                path.append({'x': cell[0], 'y': cell[1]})
                cell = par[cell]
            path.append(src)
        return [path[::-1], len(path), ex]

    def bfs(self, src, dest):

        src_cell = Cell(src['x'], src['y'], self.n_x, self.n_y, self.grid)
        q = queue.Queue(maxsize=1000)
        q.put(src_cell)
        dist = [[inf for _ in range(self.n_y)] for _ in range(self.n_x)]
        dist[src['x']][src['y']] = 0
        par = {}
        vis_dest = False
        expand = 0

        while not q.empty():
            if vis_dest:
                break
            front = q.get()
            expand += 1
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
        return [path[::-1], len(path), expand]

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
                    if cell.get_xy() == tmp.get_xy() and cell.f <= tmp.f:
                        next_neighbor = 1
                        break
                if next_neighbor:
                    continue
                for cell in closed_list:
                    if cell.get_xy() == tmp.get_xy() and cell.f <= tmp.f:
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
            return [[], 0, len(closed_list)]

        else:
            path = []
            r = dest_cell
            while r.get_xy() != src_cell.get_xy():
                path.append(r.get_xy())
                r = r.parent
            path.append(src_cell.get_xy())
            return [[item for item in reversed(path)], len(path), len(closed_list)+len(open_list)]

    def rbsfs(self, src, dest):
        src_cell = Cell(src['x'], src['y'], self.n_x, self.n_y, self.grid)
        src_cell.g = 0
        src_cell.h = self.heuristic(src_cell.get_xy(), dest)
        src_cell.f = src_cell.g + src_cell.h
        src_cell.parent = src_cell
        dest_cell = Cell(dest['x'], dest['y'], self.n_x, self.n_y, self.grid)
        visited = [src]
        open_list = [src_cell]
        succ = 0
        while len(open_list):
            open_list.sort(key=lambda x:  x.f)
            if open_list[0].get_xy() == dest_cell.get_xy():
                succ = 1
                break
            visited.append(open_list[0])
            for item in open_list[0].neighbors:
                if item not in visited:
                    tmp = Cell(item['x'], item['y'], self.n_x, self.n_y, self.grid)
                    tmp.g = open_list[0].g + 1
                    tmp.h = self.heuristic(tmp.get_xy(), dest_cell.get_xy())
                    tmp.parent = open_list[0]

        if succ:
            path = []
            r = open_list[0]
            while r.get_xy() != src_cell.get_xy():
                path.append(r.get_xy())
                r = r.parent
            path.append(src_cell.get_xy())
            return [[item for item in reversed(path)], len(path), len(visited)]





    def rbfs(self, src, dest):
        src_cell = Cell(src['x'], src['y'], self.n_x, self.n_y, self.grid)
        src_cell.g = 0
        src_cell.h = self.heuristic(src_cell.get_xy(), dest)
        src_cell.f = src_cell.g + src_cell.h
        src_cell.parent = src_cell
        dest_cell = Cell(dest['x'], dest['y'], self.n_x, self.n_y, self.grid)
        visited = []

        def rbfs_recursive(node, f_in):
            visited.append(node.get_xy())
            if node.get_xy() == dest_cell.get_xy():
                print(1)
                return node, 0
            neighbor_nodes = []
            for neighbor in node.neighbors:
                if neighbor not in visited:
                    tmp = Cell(neighbor['x'], neighbor['y'], self.n_x, self.n_y, self.grid)
                    neighbor_nodes.append(tmp)
            if len(neighbor_nodes) == 0:
                print(2)
                return None, inf
            for i in range(len(neighbor_nodes)):
                neighbor_nodes[i].g = node.g + 1
                neighbor_nodes[i].h = self.heuristic(neighbor_nodes[i].get_xy(), dest_cell.get_xy())
                neighbor_nodes[i].f = max(neighbor_nodes[i].g + neighbor_nodes[i].h, node.f)
                print(neighbor_nodes[i].get_xy(), neighbor_nodes[i].f)
            while True:

                neighbor_nodes.sort(key=lambda x: x.f)

                if neighbor_nodes[0].f > f_in:
                    print(3)
                    return None, neighbor_nodes[0].f
                try:
                    print(neighbor_nodes[0].get_xy(), min(f_in, neighbor_nodes[1].f), 'w/alt')
                    result, neighbor_nodes[0].f = rbfs_recursive(neighbor_nodes[0], min(f_in, neighbor_nodes[1].f))
                    print(result, neighbor_nodes[0].f)

                except IndexError:
                    print(neighbor_nodes[0].get_xy(), f_in, 'w/o alt')
                    result, neighbor_nodes[0].f = rbfs_recursive(neighbor_nodes[0], f_in)
                    print('back to : ', node.get_xy(), result, neighbor_nodes[0].f)

                if result is not None:
                    neighbor_nodes[0].parent = node
                    print('back to : ', node.get_xy(), result, neighbor_nodes[0].f, 4)
                    return result, neighbor_nodes[0].f
        print(src_cell.get_xy(), inf)
        result_out, bestf = rbfs_recursive(src_cell, inf)
        print(result_out, bestf)
        if result_out is None:
            return [[], 0, len(visited)]
        else:
            path = []
            r = result_out
            while r.get_xy() != src_cell.get_xy():
                path.append(r.get_xy())
                r = r.parent
            path.append(src_cell.get_xy())
            return [[item for item in reversed(path)], len(path), len(visited)]

    def search(self, src, dest):
        return {'A*': lambda: self.a_star(src, dest),
                'RBFS': lambda: self.rbfs(src, dest),
                'BFS': lambda: self.bfs(src, dest),
                'DFS': lambda: self.dfs(src, dest),
                'IDS': lambda: self.ids(src, dest),
                }[self.search_method]()
