import os
import pathlib
os.system("Start converting dot files to svg")

directory = './'
 
# iterate over files in
# that directory
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        file_extension = pathlib.Path(f).suffix
        if(file_extension != ".svg" and file_extension != ".py"):
            print("Converting file : ", filename)
            os.system("dot -Tsvg " + filename + " > " + filename + ".svg")
            os.remove(filename) 