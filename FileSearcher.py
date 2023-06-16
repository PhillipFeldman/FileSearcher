"""
Found possible issue: if the filename contains a character that isn't utf-8,
Such as an accent over a vowel in Spanish,  I get the following character �.
Pycharm suggests I change encoding to  windows-1252.
I don't know if that will be an issue.  EG, when I convert to executables, what about other languages, etc.
If there is a 'universal' encoding for all characters, will that slow down the program?"""
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from FileObject import FileObject
from pathlib import Path


class Search_Store():
    def __init__(self):
        self.keyword_set = set({})
        self.search_all = False
        self.rating_set = set({})
        self.search_by_keyword = False


# create the root window
root = tk.Tk()
root.title('Tkinter Open File Dialog')
root.resizable(False, False)
root.geometry('300x150')


def load_all_files():
    file_arr = []
    with open("./FileInfo/FileNums/paths.txt",'r') as f:
        line = True
        while line:
            line = f.readline()
            file_arr.append(line[line.find(":")+1:-1])
    return set(file_arr[:-1])

file_set = load_all_files()
print(file_set)

def complete_add_keywords(filenames,keyword):
    global file_set
    obj = None

    for file_path in filenames:
        loaded = file_path in file_set
        obj = FileObject(file_path, loaded)
        obj.add_keyword(keyword)
        if not loaded:
            file_set.add(file_path)
    obj = None

def add_keywords(filenames,str_filenames):

    add_window = tk.Tk()
    label = tk.Label(add_window, text=f'{str_filenames}Type a keyword to add to the above files')
    label.pack(expand=True)
    e = tk.Entry(add_window,borderwidth=6)
    e.pack()
    add_button = tk.Button(add_window,text="Add the keyword to the file(s)",\
                           command= lambda:complete_add_keywords(filenames,e.get()))
    add_button.pack()
    print("keywords",filenames)
    close_button = tk.Button(add_window,text="Done adding keywords",command=add_window.destroy)
    close_button.pack()

def complete_remove_keywords(filenames,keyword):
    global file_set
    obj = None

    for file_path in filenames:
        loaded = file_path in file_set
        obj = FileObject(file_path, loaded)
        obj.remove_keyword(keyword)
        if not loaded:
            file_set.add(file_path)
    obj = None

def remove_keywords(filenames,str_filenames):

    remove_window = tk.Tk()
    label = tk.Label(remove_window, text=f'{str_filenames}Type a keyword to remove to the above files')
    label.pack(expand=True)
    e = tk.Entry(remove_window,borderwidth=6)
    e.pack()
    remove_button = tk.Button(remove_window,text="remove the keyword to the file(s)",\
                           command= lambda:complete_remove_keywords(filenames,e.get()))
    remove_button.pack()
    close_button = tk.Button(remove_window,text="Done removing keywords",command=remove_window.destroy)
    close_button.pack()


def complete_rating_files(filenames,rating):
    global file_set
    obj = None
    if rating!="unrated":
        rating = int(rating)

    for file_path in filenames:
        loaded = file_path in file_set
        obj = FileObject(file_path, loaded)
        obj.change_rating(rating)
        if not loaded:
            file_set.add(file_path)
    obj = None


def rate_file(filenames,str_filenames):
    rate_window = tk.Tk()
    label = tk.Label(rate_window, text=f'{str_filenames}Rate the files from 0-10 or unrated')
    label.pack(expand=True)
    clicked = tk.StringVar()
    answer_choices = ["unrated"]+[str(i) for i in range(11)]
    print(answer_choices)
    clicked.set(answer_choices[0])
    drop = ttk.OptionMenu(rate_window,clicked,*answer_choices)
    drop.pack(expand=True)


    rate_button = tk.Button(rate_window, text="Rate the file(s)", \
                           command=lambda: complete_rating_files(filenames, clicked.get()))
    rate_button.pack()
    close_button = tk.Button(rate_window, text="Done rating files", command=rate_window.destroy)
    close_button.pack()



def file_explorer():
    filetypes = (
        ('All files', '*.*')
    )
    filenames = fd.askopenfilenames(
        title='Open a file',
        initialdir='/')



    if filenames == '':
        return None

    window = tk.Tk()
    strfilenames = str(filenames).replace(",","\n").replace("(","").replace(")","").replace("'","")
    label = tk.Label(window,text=f'Files:\n{strfilenames}')
    label.pack(expand=True)

    # rate button
    rate_button = tk.Button(
        window,
        text=f'Rate the File',
        command=lambda:rate_file(filenames,strfilenames)
    )
    add_keyword_button = tk.Button(
        window,
        text=f'Add keywords',
        command=lambda:add_keywords(filenames,strfilenames)
    )
    remove_keyword_button = tk.Button(
        window,
        text=f'Remove keywords',
        command=lambda: remove_keywords(filenames,strfilenames)
    )
    finished_button = tk.Button(
        window,
        text=f'Finished with these files',
        command=window.destroy
    )

    remove_keyword_button.pack(expand=True)
    add_keyword_button.pack(expand=True)
    rate_button.pack(expand=True)
    finished_button.pack(expand=True)

    window.mainloop()

def keyword_frame(window,keyword_var,search_store):

    if (keyword_var):
        print("keyword checked")
    else:
        print("unchecked")
    search_store.search_by_keyword = keyword_var
    print(search_store.search_by_keyword)


def add_remove_keyword(var,keyword_set,keyword,search_store):
    var.set(not var.get())
    if var.get():
        keyword_set.add(keyword)
    else:
        keyword_set.remove(keyword)


    search_store.keyword_set = keyword_set
    print(keyword_set)

def create_keyword_check_lambda(var,keyword_set,keyword,search_store):
    return lambda: add_remove_keyword(var,keyword_set,keyword,search_store)


def create_keywords_frame(window,search_store):
    keywords_frame = tk.Frame(window)
    keywords_frame.grid(row=1, column=0)
    #######
    checked_keywords_set = set({})
    keyword_path_str = "./FileInfo/Associations/KeywordAssociations/"

    path_pointer = Path(keyword_path_str)
    pointer_contents = os.scandir(path_pointer)
    root.title("File Searcher")
    check_boxes = []
    pc = list(pointer_contents)
    paths = [i.path for i in pc]
    lambdas = []
    keyword_checked_vars = []
    keywords = []

    for i in range(len(paths)):
        v = tk.BooleanVar()
        keyword_checked_vars.append(v)
        p = paths[i]
        this_keyword = p[len(keyword_path_str) - 2:p.find('.txt')]
        keywords.append(this_keyword)
        lambdas.append(create_keyword_check_lambda(v, checked_keywords_set, this_keyword,search_store))

    for i in range(len(pc)):
        b = tk.Checkbutton(keywords_frame, text=keywords[i], \
                           command=lambdas[i], \
                           variable=keyword_checked_vars[i], \
                           onvalue=True, offvalue=False)
        b.var = keyword_checked_vars[i]
        b.pack()
        check_boxes.append(b)

    #######
    keyword_var = tk.BooleanVar()

    def change_keyword_var(window, keyword_var,search_store):
        keyword_var.set(not keyword_var.get())
        keyword_frame(window, keyword_var.get(),search_store)

    keyword_check = tk.Checkbutton(window, text="Search by Keywords", \
                                   command=lambda: change_keyword_var(window, keyword_var,search_store), \
                                   variable=keyword_var, \
                                   onvalue=True, offvalue=False)

    keyword_check.var = keyword_var
    keyword_check.grid(row=0, column=0)

def search(search_store):
    file_set = set({})
    if search_store.search_all == False:
        if search_store.search_by_keyword:
            for keyword in search_store.keyword_set:
                with open(f'./FileInfo/Associations/KeywordAssociations/{keyword}.txt','r') as f:
                    for line in f.readlines():
                        file_set = file_set.union(line[1:-2])
    paths = []
    for num in list(file_set):
        with open(f'./FileInfo/FileNums/{num}.txt', 'r') as f:
            paths.append(f.readline()[5:-1])
    print(paths)

def file_searcher():
    print("searching")
    window = tk.Tk()
    search_store = Search_Store()
    create_keywords_frame(window,search_store)

    search_button = tk.Button(window,text="Search",command=lambda:search(search_store))
    search_button.grid(row = 2, column=0)



    window.mainloop()


# file_explorer button
file_explorer_button = ttk.Button(
    root,
    text='Open File Explorer',
    command=file_explorer
)

file_explorer_button.pack(expand=True)

file_searcher_button = ttk.Button(
    root,
    text='Search For a File',
    command=file_searcher
)

file_searcher_button.pack(expand=True)

close_button = ttk.Button(
    root,
    text='End Program',
    command=root.destroy#doesnt actually end the program.  Use something else?
)

close_button.pack(expand=True)


# run the application
root.mainloop()
'''
root = Tk()
root.title('Codemy.com Image Viewer')



def open():
	global my_image
	root.filename = filedialog.askopenfilename(initialdir=".", title="Select A File")
	my_label = Label(root, text=root.filename).pack()
	my_image = ImageTk.PhotoImage(Image.open(root.filename))
	my_image_label = Label(image=my_image).pack()


explore_btn = Button(root, text="File explorer", command=open).pack()
search_btn = Button(root, text="Search Files", command=open).pack()


root.mainloop()
'''