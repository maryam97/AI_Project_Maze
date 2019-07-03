import tkinter as tk
from tkinter import ttk
from Vis import App


def read_table(path):
    f = open(path, 'r')
    table = []
    for line in f.readlines():
        table.append([int(x) for x in line.split(sep=' ')])

    table = [x for x in reversed(table)]
    # return list(map(list, zip(*table)))
    return table


def OK(entries):
    print(entries)
    table = read_table(entries['Map File Path'].get())
    src = {'x': int(entries['Source X'].get()), 'y': int(entries['Source Y'].get())}
    dest = {'x': int(entries['Destination X'].get()), 'y': int(entries['Destination Y'].get())}
    theApp = App(table, entries['Algorithms'].get(), src, dest, entries['Heuristics'].get())
    theApp.on_execute()
    root.quit()


def make_form(root, fields):
    entries = {}
    for field in fields:
        print(field)
        row = tk.Frame(root)
        lab = tk.Label(row, width=22, text=field+": ", anchor='w')
        ent = tk.Entry(row)
        row.pack(side=tk.TOP,
                 fill=tk.X,
                 padx=5,
                 pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT,
                 expand=tk.YES,
                 fill=tk.X)
        entries[field] = ent

    row = tk.Frame(root)
    lab = tk.Label(row, width=22, text="Algorithms: ", anchor='w')
    ent = ttk.Combobox(row, values=[
                                    "A*",
                                    "RBFS",
                                    "BFS",
                                    "DFS",
                                    "IDS"])
    row.pack(side=tk.TOP,
             fill=tk.X,
             padx=5,
             pady=5)
    lab.pack(side=tk.LEFT)
    ent.pack(side=tk.RIGHT,
             expand=tk.YES,
             fill=tk.X)
    entries['Algorithms'] = ent

    row = tk.Frame(root)
    lab = tk.Label(row, width=22, text="Heuristics: ", anchor='w')
    ent = ttk.Combobox(row, values=[
        "Manhattan",
        "Euclidean",
        "Diagonal"])
    row.pack(side=tk.TOP,
             fill=tk.X,
             padx=5,
             pady=5)
    lab.pack(side=tk.LEFT)
    ent.pack(side=tk.RIGHT,
             expand=tk.YES,
             fill=tk.X)
    entries['Heuristics'] = ent

    return entries


if __name__ == '__main__':
    fields_text = ('Map File Path', 'Source X', 'Source Y', 'Destination X', 'Destination Y')
    root = tk.Tk()
    ents = make_form(root, fields_text)
    b1 = tk.Button(root, text='Ok',
           command=(lambda e=ents: OK(e)))
    b1.pack(side=tk.LEFT, padx=5, pady=5)
    b3 = tk.Button(root, text='Quit', command=root.quit)
    b3.pack(side=tk.LEFT, padx=5, pady=5)
    root.mainloop()
