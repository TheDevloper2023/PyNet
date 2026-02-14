from utils import enable_true_color, RichText, Colors, Commands
import re
enable_true_color()
rt = RichText()
co = Colors()
cmds = Commands()






file = "Index.page" #TODO, this is just for now trust trust


# Here we load the file,
# In the actual code, we download the .page file into %TEMP%/*.page and load it from there
with open(file) as f:
    vars = {}
    for line in f:
        # 1. Check for commands first
        if line.startswith("@"):
            cmds.run(line, vars)
            continue # Don't print the @ command line
        line = re.sub(r'\$(\w+)', lambda m: str(vars.get(m.group(1), '$'+m.group(1))), line)
        
        line = re.sub(r';;.*$', '', line)


        text = co.run(line)
        text = rt.run(text)   
           # Apply Bold/Italic
              # Apply Colors to the already-styled text
        
        # 3. Print the final result once
        print(text, end="")
        



