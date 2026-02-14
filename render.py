from utils import enable_true_color, Wrapper
import re
enable_true_color()

renderer = Wrapper()





file = "Index.page" #TODO, this is just for now trust trust


# Here we load the file,
# In the actual code, we download the .page file into %TEMP%/*.page and load it from there
with open(file) as f:
    vars = {}
    for line in f:
        text = renderer(line)
        print(text, end="")
        



