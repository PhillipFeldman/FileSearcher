"""
Found possible issue: if the filename contains a character that isn't utf-8,
Such as an accent over a vowel in Spanish,  I get the following character �.
Pycharm suggests I change encoding to  windows-1252.
I don't know if that will be an issue.  EG, when I convert to executables, what about other languages, etc.
If there is a 'universal' encoding for all characters, will that slow down the program?"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from FileObject import FileObject

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




def rate_file(filenames):
    print("rate",filenames)

def remove_keywords(filenames):
    print("remove",filenames)

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
        command=lambda:rate_file(filenames)
    )
    add_keyword_button = tk.Button(
        window,
        text=f'Add keywords',
        command=lambda:add_keywords(filenames,strfilenames)
    )
    remove_keyword_button = tk.Button(
        window,
        text=f'remove keywords',
        command=lambda: remove_keywords(filenames)
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

def file_searcher():
    print("searching")

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