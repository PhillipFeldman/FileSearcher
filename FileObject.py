import os
import sys
class FileObject:
    def __init__(self, path):
        self.num = self.count_files()
        self.path = path
        self.keyword = []
        self.category = {}
        self.rating = "unrated"
        self.change_rating("unrated")
        self.password = None
        self.name = ""
        self.description = ""
        self.hash = ""
        self.associations = {"category_associations.txt":self.category,\
                             "keyword_associations.txt":self.keyword,\
                             "name_associations.txt":self.name}#,\
                             #"rating_associations.txt":self.rating}
        #need to fix the various
        self.store_file()

    def store_file_num(self):
        path_str = f"./FileInfo/FileNums/{self.num}.txt"
        with open(path_str, 'w') as f:
            f.write(self.path)

    def store_file_path(self):
        path_str = f"./FileInfo/FileNums/paths.txt"
        with open(path_str, 'a') as f:
            f.write(f'{self.num}:{self.path}\n')


    def store_file(self):
        self.store_file_num()
        self.store_file_path()


    """#does length really belong in media_type?
    self.catogery ={
    "media_type":{"video":{"file_type":["mp4","wav","webm"],"length":["long","short"]}}},
    "
    }
    """


    def add_keyword(self,keyword):
        self.keyword.append(keyword)
        keyword_path_str = f"./FileInfo/Associations/KeywordAssociations/{keyword}.txt"
        file_arr = []
        try:
            with open(keyword_path_str, 'r') as f:
                file_arr = f.readlines()
        except FileNotFoundError:
            with open(keyword_path_str, 'w') as f:
                f.write(f'-{self.num}-\n')
                return

        with open(keyword_path_str, 'a') as f:
            if f'-{self.num}-\n' not in file_arr:
                f.write(f'-{self.num}-\n')

    def remove_keyword(self,keyword):
        self.keyword.append(keyword)
        keyword_path_str = f"./FileInfo/Associations/KeywordAssociations/{keyword}.txt"
        file_arr = []
        try:
            with open(keyword_path_str, 'r') as f:
                file_arr = f.readlines()
        except FileNotFoundError:
                return

        with open(keyword_path_str, 'w') as f:
            try:
                file_arr.remove(f'-{self.num}-\n')
                for line in file_arr:
                    f.write(line)

            except ValueError:
                return

    def change_rating(self,rating):
        assert rating == "unrated" or (type(rating) == int and 0 <= int(rating) <= 100)
        self.rating = rating
        rating_path_str = "./FileInfo/Associations/rating_associations.txt"
        file_arr = []
        with open(rating_path_str, 'r') as f:
            file_arr = f.readlines()
        with open(rating_path_str, 'w') as f:
            checked = False
            for line_idx in range(len(file_arr)):
                line = file_arr[line_idx]
                match = line[:line.find(":")]
                if match == str(rating):
                    checked = True
                    if f'-{self.num}-' not in line:
                        file_arr[line_idx] = line[:-1] + f'-{self.num}-\n'
                else:
                    if f'-{self.num}-' in line:
                        place = line.find(f'-{self.num}-')
                        size = len(f'-{self.num}-')
                        file_arr[line_idx] = line[:place] + line[place+size:]
            if not checked:
                file_arr.append(f'{rating}:-{self.num}-\n')
            for line in file_arr:
                f.write(line)



#save file should probably not be used
    def save_file(self):
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