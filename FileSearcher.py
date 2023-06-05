import os
from pathlib import Path

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


    pass


if __name__ == '__main__':
    main()