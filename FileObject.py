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
                             "name_associations.txt":self.name}#,\
                             #"rating_associations.txt":self.rating}
        #need to fix the various


    def store_file(self):
        path_str = "./FileInfo/Associations/"
        for file_name in self.associations.keys():
            file_arr = []
            association_arr = self.associations[file_name]
            with open(path_str+file_name,'r') as f:
                file_arr = f.readlines()
            with open(path_str+file_name,'w') as f:
                for association in association_arr:
                    checked = False
                    for line_idx in range(len(file_arr)):
                        line = file_arr[line_idx]
                        match = line[:line.find(":")]
                        if match==association:
                            checked = True
                            if f'-{self.num}-' not in line:
                                file_arr[line_idx] = line + f'-{self.num}-'
                            break
                    if not checked:
                        file_arr.append(f'{association}:-{self.num}-')
                for line in file_arr:
                    f.write(line)



    def add_association(self,association_type,association):
        self.associations[association_type].append(association)

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