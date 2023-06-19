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
        self.search_all = True
        self.rating_set = set({})
        self.search_by_keyword = False
        self.search_by_rating = False


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


def add_remove_rating(var,ratings_set,rating,search_store):
    var.set(not var.get())
    if var.get():
        ratings_set.add(rating)
    else:
        ratings_set.remove(rating)


    search_store.rating_set = ratings_set
    print(ratings_set)

def create_keyword_check_lambda(var,keyword_set,keyword,search_store):
    return lambda: add_remove_keyword(var,keyword_set,keyword,search_store)

def create_ratings_check_lambda(var,ratings_set,rating,search_store):
    return lambda: add_remove_rating(var,ratings_set,rating,search_store)

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


def rating_frame(window,rating_var,search_store):

    if (rating_var):
        print("keyword checked")
    else:
        print("unchecked")
    search_store.search_by_rating = rating_var
    print(search_store.search_by_keyword)

def create_ratings_frame(window,search_store):
    ratings_frame = tk.Frame(window)
    ratings_frame.grid(row=1, column=1)
    #######
    checked_ratings_set = set({})
    ratings_path_str = "./FileInfo/Associations/rating_associations.txt"

    #path_pointer = Path(ratings_path_str)#dont need to go searching every file. it's all in one
    #pointer_contents = os.scandir(path_pointer)
    root.title("File Searcher")
    check_boxes = []
    #pc = list(pointer_contents)
    lambdas = []
    ratings_checked_vars = []
    ratings = ["unrated"]+[str(i) for i in range(11)]


    for i in range(len(ratings)):
        v = tk.BooleanVar()
        ratings_checked_vars.append(v)
        this_rating = ratings[i]
        lambdas.append(create_ratings_check_lambda(v, checked_ratings_set, this_rating,search_store))

    for i in range(12):
        b = tk.Checkbutton(ratings_frame, text=ratings[i], \
                           command=lambdas[i], \
                           variable=ratings_checked_vars[i], \
                           onvalue=True, offvalue=False)
        b.var = ratings_checked_vars[i]
        b.pack()
        check_boxes.append(b)

    #######
    rating_var = tk.BooleanVar()

    def change_rating_var(window, rating_var,search_store):
        rating_var.set(not rating_var.get())
        rating_frame(window, rating_var.get(),search_store)

    rating_check = tk.Checkbutton(window, text="Search by Rating", \
                                   command=lambda: change_rating_var(window, rating_var,search_store), \
                                   variable=rating_var, \
                                   onvalue=True, offvalue=False)

    rating_check.var = rating_var
    rating_check.grid(row=0, column=1)


def create_search_all_any_frame(window,search_store):
    radio_frame = tk.Frame(window)
    radio_frame.grid(row=1, column=3)
    r = tk.BooleanVar()
    r.set(True)

    def changed_radio(value,search_store):
        print(value)
        search_store.search_all = value

    def create_lambda_any(value,search_store):
        value.set(False)
        changed_radio(value.get(),search_store)

    def create_lambda_all(value,search_store):
        value.set(True)
        changed_radio(value.get(),search_store)

    radio_button_any = tk.Radiobutton(radio_frame, text = "Search by any keyword and rating",\
                                      variable = r,value = True,command=lambda : create_lambda_any(r,search_store))
    radio_button_all = tk.Radiobutton(radio_frame, text="Search by all keywords and rating",\
                                      variable = r,value = False,command=lambda : create_lambda_all(r,search_store))
    radio_button_any.pack()
    radio_button_all.pack()


def search(search_store):
    file_set = set({})
    if search_store.search_all == False:
        if search_store.search_by_keyword:
            for keyword in search_store.keyword_set:
                with open(f'./FileInfo/Associations/KeywordAssociations/{keyword}.txt','r') as f:
                    for line in f.readlines():
                        file_set = file_set.union(line[1:-2])
        if search_store.search_by_rating:
            with open(f'./FileInfo/Associations/rating_associations.txt', 'r') as f:
                for line in f.readlines():
                    num = line[:line.find(':')]
                    if num in search_store.rating_set:
                        all_nums = line[line.find(':')+1:]
                        all_nums = all_nums.replace('--',',')
                        all_nums = all_nums.replace('-', '')
                        all_nums = all_nums.replace('\n', '')
                        all_nums = all_nums.split(',')
                        print(all_nums)
                        file_set = file_set.union(set(all_nums))

    else:
        sets = []
        if search_store.search_by_keyword:
            for keyword in search_store.keyword_set:
                this_keyword_set = set({})
                with open(f'./FileInfo/Associations/KeywordAssociations/{keyword}.txt','r') as f:
                    for line in f.readlines():
                        this_keyword_set = this_keyword_set.union(line[1:-2])
                sets.append(this_keyword_set)
        if search_store.search_by_rating:
            if len(search_store.rating_set )!= 1:
                pass
            else:
                with open(f'./FileInfo/Associations/rating_associations.txt', 'r') as f:
                    this_rating_set = set({})
                    for line in f.readlines():
                        num = line[:line.find(':')]
                        if num in search_store.rating_set:
                            all_nums = line[line.find(':')+1:]
                            all_nums = all_nums.replace('--',',')
                            all_nums = all_nums.replace('-', '')
                            all_nums = all_nums.replace('\n', '')
                            all_nums = all_nums.split(',')
                            print(all_nums)
                            this_rating_set = this_rating_set.union(set(all_nums))
                            break
                    sets.append(this_rating_set)

        try:
            file_set = sets[0]
            for s in sets:
                file_set = file_set.intersection(s)
        except IndexError:
            pass






    #results
    paths = []
    for num in list(file_set):
        with open(f'./FileInfo/FileNums/{num}.txt', 'r') as f:
            paths.append(f.readline()[5:-1])

    search_results_window(paths)



def search_results_window(paths):
    window = tk.Tk()
    labels = []
    for path in paths:
        l = tk.Label(window, text=path)
        labels.append(l)
        l.pack()

    close_button = tk.Button(window, text="Close", command=window.destroy)
    close_button.pack()
    window.mainloop()
    print(paths)




def file_searcher():
    print("searching")
    window = tk.Tk()
    search_store = Search_Store()#The object to keep the garbage collector from eating my stuff
    create_keywords_frame(window,search_store)
    create_ratings_frame(window,search_store)
    create_search_all_any_frame(window,search_store)

    search_button = tk.Button(window,text="Search",command=lambda:search(search_store))
    search_button.grid(row = 2, column=0)
    close_button = tk.Button(window, text="End Searching", command=window.destroy)
    close_button.grid(row=3,column=0)



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
    command=exit #doesnt actually end the program.  Use something else?<--like exit()...duh
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