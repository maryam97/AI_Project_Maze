from Maze import Path

def read_table(path):
    f = open(path, 'r')

    table = []
    for line in f.readlines():
        table.append([int(x) for x in line.split(sep=' ')])
    return table

if __name__ == "__main__":
    table = read_table('map.txt')


