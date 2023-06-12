import os
import tkinter as tk
from pathlib import Path


"""
buttonframe = tk.Frame(root)
buttonframe.columnconfigure(0,weight=1)
buttonframe.columnconfigure(1,weight=1)
buttonframe.columnconfigure(2,weight=1)

btn1 = tk.Button(buttonframe, text="1",font=("Arial",18))
btn1.grid(row=0,column=0,sticky=tk.W+tk.E)
buttonframe.pack(fill='x')
"""

def load_path(path_pointer,root):
    pointer_contents = os.scandir(path_pointer)
    root.title("File Searcher")
    buttons = []
    NUMROWS = 12
    pc = list(pointer_contents)
    paths = [i.path for i in pc]
    lambdas = []
    for i in range(len(paths)):
        p = paths[i]
        lambdas.append(create_lambda(p,root))

    for i in range(len(pc)):
        b = tk.Button(root, text=pc[i].path, command=lambdas[i], font=("Arial", 12))
        b.grid(row=i % NUMROWS, column=i // NUMROWS)
        buttons.append(b)


def clicked_path(path,root):
    print("hello", path)
    root.destroy()
    root = tk.Tk()
    path_pointer = Path(path) #Path.home()
    load_path(path_pointer, root)
    root.mainloop()
    pass

def create_lambda(path,root):  # need this to fix scope issue
    return lambda: clicked_path(path,root)

def set_up():
    root = tk.Tk()
    path_pointer = Path.home()
    load_path(path_pointer,root)
    ###
    root.mainloop()


def main():
    set_up()


if __name__ == '__main__':
    main()