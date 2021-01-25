from tkinter import *
from pygenerategui import *
# This would be any module(s) you import
import example_module

# Components can be module, class, or class instance
components = [example_module, example_module.ClassExample, example_module.ClassInstanceExample(12)]
# Title can be whatever you want
app = PGGUI_App(title='My App Title', components=components)
app.mainloop()