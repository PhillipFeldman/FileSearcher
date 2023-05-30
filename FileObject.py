import os
import sys
class FileObject:
    def __init__(self, path):
        self.num = self.count_files()
        self.path = path
        self.keyword = []
        self.category = []
        self.rating = "unrated"
        self.password = None
        self.name = ""
        self.description = ""
        self.hash = ""
        self.associations = {"category_associations.txt":self.category,\
                             "keyword_associations.txt":self.keyword,\
                             "name_associations.txt":self.name,\
                             "rating_associations.txt":self.rating}


    def store_file(self):
        for file_name in self.associations.keys():
            file_arr = []
            association_arr = self.associations[file_name]
            with open(file_name,'r') as f:
                file_arr = f.readlines()
            with open(file_name,'w') as f:
                for line in file_arr:



    def count_files(self):
        count = 0
        with open("./FileInfo/current_count.txt",'r') as f:
            try:
                count=int(f.read())
            except ValueError:
                count = 0
        with open("./FileInfo/current_count.txt",'w') as f:
                f.write(str(count+1))
        return count+1