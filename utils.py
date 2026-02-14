
import os
import sys
import re

def enable_true_color():
    """
    Enables True Color on the New Windows Terminal (10/11) if not already enabled

    """
    if sys.platform == "win32":
        import ctypes
        from ctypes import wintypes
        
        # Win32 Constants
        kernel32 = ctypes.windll.kernel32
        STD_OUTPUT_HANDLE = -11
        ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
        
        handle = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        mode = wintypes.DWORD()
        
        if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            kernel32.SetConsoleMode(handle, mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING)



class Commands:
    """
    A class that phrases commands
    """
    def __init__(self):

        self.cmds = {
            "title": self.title,
            "input": self.get_input
        }

    def run(self, line: str, var:dict):
        if not line.startswith("@"):
            return

        parts = line[1:].split(" ", 1)
        cmd = parts[0]
        arg = parts[1] if len(parts) > 1 else ""

        if cmd in self.cmds:
            self.cmds[cmd](arg, var)


    def title(self, input, var=None):
        os.system(f"title {input}")


    # I had to vibe code the patch => The whole code changed. it works at least
    def get_input(self, line, var):
        try:
            var_name, prompt = line.split(" ", 1)
            var[var_name] = input(prompt + " ")
        except ValueError:
            print("[ERROR] @input usage: @input VAR_NAME prompt")


class RichText:
    """
    A class that makes text not boring I think
    """

    def __init__(self):
        self.rules = [ # so like regrex, on / off. e.g: (r"\*\*(.+?)\*\*", "[1m", "\[22m") for bolding stuff I think.
            (re.compile(r"\*\*(.+?)\*\*"), "[1m", "[22m"), #Bold
            (re.compile(r"\*(.+?)\*"), "[3m", "[23m"), #Italic
            (re.compile(r"\_(.+?)\_"), "[4m", "[24m"), #Underline
            (re.compile(r"\!\!(.+?)\!\!"), "[5m", "[25m"), #Blink
            (re.compile(r"\~(.+?)\~"), "[9m", "[29m"), #Strikethrough
            (re.compile(r"\:\:(.+?)\:\:"), "[2m", "[22m"), #Dim / Faded
            (re.compile(r"\^\^(.+?)\^\^"), "[53m", "[55m"), #Overline
        ]

    def run(self, text):
        for regex, on, off in self.rules:
            text = regex.sub(
                lambda m: on + m.group(1) + off,
                text
            )
        return text + "[0m"  # reset at end


class Colors:
    def __init__(self):
        default_fg_colors = [ #Default Colors
            # REGULAR
            ("BLACK", "[38;5;0m"),
            ("RED", "[38;5;1m"),
            ("GREEN", "[38;5;2m"),
            ("YELLOW", "[38;5;3m"),
            ("BLUE", "[38;5;4m"),
            ("MAGENTA", "[38;5;5m"),
            ("CYAN", "[38;5;6m"),
            ("WHITE", "[38;5;7m"),

            # Bright
            ("B_BLACK", "[38;5;8m"),
            ("B_RED", "[38;5;9m"),
            ("B_GREEN", "[38;5;10m"),
            ("B_YELLOW", "[38;5;11m"),
            ("B_BLUE", "[38;5;12m"),
            ("B_MAGENTA", "[38;5;13m"),
            ("B_CYAN", "[38;5;14m"),
            ("B_WHITE", "[38;5;15m"),
        ]

        default_bg_colors = [ #Default Colors
            # REGULAR
            ("BLACK", "[48;5;0m"),
            ("RED", "[48;5;1m"),
            ("GREEN", "[48;5;2m"),
            ("YELLOW", "[48;5;3m"),
            ("BLUE", "[48;5;4m"),
            ("MAGENTA", "[48;5;5m"),
            ("CYAN", "[48;5;6m"),
            ("WHITE", "[48;5;7m"),

            # Bright
            ("B_BLACK", "[48;5;8m"),
            ("B_RED", "[48;5;9m"),
            ("B_GREEN", "[48;5;10m"),
            ("B_YELLOW", "[48;5;11m"),
            ("B_BLUE", "[48;5;12m"),
            ("B_MAGENTA", "[48;5;13m"),
            ("B_CYAN", "[48;5;14m"),
            ("B_WHITE", "[48;5;15m"),
        ]




        self.color_dict = {f"FG_{color}":  a for color, a in default_fg_colors}
        self.color_dict.update({f"BG_{color}":  a for color, a in default_bg_colors}) 

    def run(self, text):

        #Regular Text e.g {FG_RED} red text {/FG_RED} or {}
        text = re.sub(r'\{(\w+)\}', lambda m: self.color_dict.get(m.group(1), m.group(0)), text)


        #Custom Colors e.g {C_BG_r_g_b}
        # 256
        text = re.sub(r'\{C_FG_(\d+)\}', r"[38;5;\1m", text)
        text = re.sub(r'\{C_BG_(\d+)\}', r"[48;5;\1m", text)
        # True
        text = re.sub(r'\{C_FG_(\d+)_(\d+)_(\d+)\}', r"[38;2;\1;\2;\3m", text)
        text = re.sub(r'\{C_BG_(\d+)_(\d+)_(\d+)\}', r"[48;2;\1;\2;\3m", text)


        #Reset color
        text = re.sub(r'\{/\w+\}', "[0m", text)

        return text
    

class Wrapper:
    """
    Wrapper for the current markdown system.

    You kinda use it like this:

    wrapper = Wrapper()
    wrapper("Text to you want to render")
    """
    def __init__(self):
        self.vars = {}

        self.cmds = Commands()
        self.richtxt = RichText()
        self.cols = Colors()
    

    def __call__(self, line):
        if line.startswith("@"):
            self.cmds.run(line, self.vars)
            
        line = re.sub(r'\$(\w+)', lambda m: str(self.vars.get(m.group(1), '$'+m.group(1))), line)
        
        line = re.sub(r';;.*$', '', line)


        text = self.cols.run(line)
        text = self.richtxt.run(text)  

        return text 