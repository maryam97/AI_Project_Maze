from Maze import Path


def test_rbfs(table):
    for (A, B) in [({'x': 1, 'y': 1}, {'x': 8, 'y': 1}), ({'x': 1, 'y': 1}, {'x': 1, 'y': 3})]:
        for method in ['Manhattan', 'Diagonal', 'Euclidean']:
            print("Hueristic " + str(method) + ' source: ' + str(A) + ' destination: ' + str(B))
            rbfs = Path(table, method)
            path, length = rbfs.rbfs(A, B)
            print(path, length)


def test_a_star(table):
    for (A, B) in [({'x': 1, 'y': 1}, {'x': 8, 'y': 1}), ({'x': 1, 'y': 1}, {'x': 1, 'y': 3})]:
        for method in ['Manhattan', 'Diagonal', 'Euclidean']:
            print("Hueristic " + str(method) + ' source: ' + str(A) + ' destination: ' + str(B))
            a_star = Path(table, method)
            path, length = a_star.a_star(A, B)
            print(path, length)


def bfs_(path, src, dest):
    return path.bfs(src, dest)


def read_table(path):
    f = open(path, 'r')

    table = []
    for line in f.readlines():
        table.append([int(x) for x in line.split(sep=' ')])
    return [x for x in reversed(table)]


if __name__ == "__main__":
    table = read_table('map.txt')
    path = Path(table, heuristic='Manhattan')
    src_cell = {'x': 3, 'y': 8}
    dest_cell = {'x': 5, 'y': 8}
    print(bfs_(path, src_cell, dest_cell))
    test_a_star(table)
    test_rbfs(table)
