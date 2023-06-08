from FileObject import FileObject
g = FileObject("test2")
g.add_keyword("cat")
h = FileObject("test3")
h.change_rating(3)
h.add_keyword("dog")


f = FileObject("test3",True)
f.change_rating(4)
f.remove_keyword("dog")
f.add_keyword("bird")
print(f.rating,f.keyword)

def main():
    print()
    path_pointer = Path.home()
    print(path_pointer)
    FileInfoPath = os.path.abspath("FileInfo")
    print(FileInfoPath)
    pointer_contents = os.scandir(path_pointer)
    print(pointer_contents)
    for i in pointer_contents:
        print(i.path)