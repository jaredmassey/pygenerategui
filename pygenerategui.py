# MIT License
#
# Copyright (c) 2021 Jared Massey
# jared@jaredmasey.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from tkinter import *
from tkinter import ttk
import inspect
from typing import Union, get_args, get_origin
from enum import EnumMeta, Enum, IntEnum, Flag, IntFlag
import re

import gui_component as gui


def pggui(name=None):
    if callable(name):
        return pggui()(name)
    def decorator(func):
        func._pggui_name = name if name is not None else func.__name__
        return func
    return decorator


def load_funcs(component):
    """
    Modeled loosely off of robotlibcore's add_library_components
    :param component: A module, class, or an instance of a class, containing callables to be potentially tuned into GUIs
    :return: A list containing any functions which are flagged to be turned into a GUI
    """
    pggui_funcs = []

    def _get_members(c):
        if not inpsect.isclass(c):
            return [m for m in inspect.getmembers(c) if inspect.isroutine(m)]
        else:
            members = []
            for m in inspect.getmembers(c):
                if inspect.ismethod(m):
                    members.append(m)
                elif type(c.__dict__(m.__name__)) is staticmethod:
                    members.append(m)
            return members

    for member in _get_members(component):
        if hasattr(member, _pggui_name):
            funcs.append(member)
    return pggui_funcs


    def param_is_correct_type(value, anno) -> bool:
        """
        Identify if the given param is of the type indicated by anno
        :param param: The value passed in to the function
        :param anno: inspect.getfullargspec(func).annotations['<param>']
        :return: True if it is the right type, else False
        """
        if get_origin(anno) is Union:
            anno = get_args(anno)
        return isinstance(param, anno)

class PGGUI_App(ttk.Frame):
    def __init__(self, function_list, master=None):
        super().__init__(master)
        self.master = master
        self.function_list = function_list
        self.grid(row=0, column=0)
        self.init_gui()

    def init_gui(self):
        # Header
        self.header = gui.ComboBoxBlock(self, 'Select A Function To Run',
                                        {'One': 1, 'Two': 2, 'Three': 3, '_manual': int},
                                        on_select=self.combobox_selection_changed)
        self.header.place(row=1)
        self.lbl = ttk.Label(self, text='entry_description', anchor='nw', wraplength=450)
        self.lbl.grid(row=0, column=0, sticky='w')

        # Function GUI
        self.function_frame = ttk.Frame(self)
        self.function_frame.grid(row=5, column=0, columnspan=999)
        self.ti = gui.TextInputBlock(self.function_frame, 'blah')
        self.ti.place(row=0, column=0)
        self.ti = gui.TextInputBlock(self.function_frame, 'blah2')
        self.ti.place(row=1, column=0)
        self.chk = gui.BoolInputBlock(self.function_frame, 'CHK')
        self.chk.place(row=2, column=0)

        # Footer
        # Quit Button
        self.quit = ttk.Button(self, text="QUIT", command=self.master.destroy)
        self.quit.grid(row=999, column=999)
        # Run Button
        self.btn_run = ttk.Button(self, text='RUN', command=None)
        self.btn_run.grid(row=998, column=999)

    def update_label_text(self, label: Label, text: str):
        label['text'] = text

    def combobox_selection_changed(self, value):
        self.update_label_text(self.lbl, value)

    def insert_function_gui(self, f):
        # param_pattern = f':param x:(.*?)\s+[:|$]'
        fas = inspect.getfullargspec(f)
        description = '<No Description>' if f.__doc__ is None else f.__doc__


root = Tk()
app = PGGUI_App([], master=root)
app.mainloop()