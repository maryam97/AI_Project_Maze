from Maze import Path


def read_table(path):
    f = open(path, 'r')

    table = []
    for line in f.readlines():
        table.append([int(x) for x in line.split(sep=' ')])
    return table


def bfs_(path, src, dest):
    return path.bfs(src, dest)


if __name__ == "__main__":
    table = read_table('map.txt')
    path = Path(table, heuristic='Manhattan')
    src_cell = {'x': 3, 'y': 8}
    dest_cell = {'x': 5, 'y': 8}
    print(bfs_(path, src_cell, dest_cell))
