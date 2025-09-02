import os


DIRECTORIES = ["./data/futures", "./data/metals", "./final"]

def make_dirs():
    for dir in DIRECTORIES:
        if not os.path.exists(dir):
            os.makedirs(dir)

        print("DIRECTORY EXSISTS " + dir)