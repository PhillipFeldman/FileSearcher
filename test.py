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