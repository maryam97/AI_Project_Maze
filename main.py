from Maze import Path


def test_rbfs(table):
    for (A, B) in [({'x': 8, 'y': 3}, {'x': 8, 'y': 6}),({'x': 1, 'y': 1}, {'x': 1, 'y': 3})]:
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


def test_bfs(table):
    for (A, B) in [({'x': 8, 'y': 3}, {'x': 8, 'y': 6}), ({'x': 1, 'y': 1}, {'x': 8, 'y': 1}), ({'x': 1, 'y': 1}, {'x': 1, 'y': 3})]:
        print('Source: ' + str(A) + ' destination: ' + str(B))
        bfs = Path(table)
        path, length = bfs.bfs(A, B)
        print(path, length)


def test_dfs(table):
    for (A, B) in [({'x': 8, 'y': 3}, {'x': 8, 'y': 6}), ({'x': 1, 'y': 1}, {'x': 8, 'y': 1}), ({'x': 1, 'y': 1}, {'x': 1, 'y': 3})]:
        print('Source: ' + str(A) + ' destination: ' + str(B))
        dfs = Path(table)
        path, length = dfs.dfs(A, B)
        print(path, length)


def read_table(path):
    f = open(path, 'r')

    table = []
    for line in f.readlines():
        table.append([int(x) for x in line.split(sep=' ')])

    table = [x for x in reversed(table)]
    return list(map(list, zip(*table)))




if __name__ == "__main__":
    table = read_table('map.txt')
    print("BFS:")
    test_bfs(table)
    print("DFS:")
    test_dfs(table)
    print("A_STAR:")
    test_a_star(table)
    print("RBFS:")
    test_rbfs(table)
