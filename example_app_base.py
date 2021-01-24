from tkinter import *
from pygenerategui import *
# This would be any module(s) you import
import example_module

root = Tk()
# Change this to whatever you want the window title to be
root.title('PGGUI')
modules = []
# You can pass in a module, class, or class instance
for x in (example_module, example_module.StaticClassExample, example_module.InstanceClassExample(12)):
    modules += load_funcs(x)
app = PGGUI_App(master=root, function_list=modules)
app.mainloop()