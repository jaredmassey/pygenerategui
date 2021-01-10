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
    Modeled off of robotlibcore's add_library_components
    :param component: A module or an instance of a class, containing callables to be potentially tuned into GUIs
    :return: A list containing any functions which are flagged to be turned into a GUI
    """
    funcs = []
    if inspect.ismodule(component):
        members = inspect.getmembers(component)
    elif inspect.isclass(component):
        raise TypeError(f'Expected module or instance, got class: {component.__name__} instead')
    elif type(component) != component.__class__:
        raise TypeError(f'Expected new-style class, got old-style class: {component.__class__.__name__} instead')
    else:
        members = _get_members(component)

    def _get_members(m):
        # Prefer to get class members to avoid calling properties
        # I'm not certain this is the desired behavior in my case, since it will prefer default function definitions
        # over per-instance overrides. TBD.
        cls = type(m)
        for name in dir(instance):
            owner = cls if hasattr(cls, name) else m
            yield name, getattr(owner, name)

    for member in members:
        if inspect.isroutine(member):
            if hasattr(member, _pggui_name):
                funcs.append(member)
    return funcs


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


class Application(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(row=0, column=0)
        self.init_gui()

    def init_gui(self):
        # Header
        self.header = gui.ComboBoxBlock(self, 'Select A Function To Run', {'One': 1, 'Two': 2, 'Three': 3})
        self.header.grid(row=1, column=0)

        # Function GUI
        self.ti = gui.TextInputBlock(self, 'blah')
        self.ti.grid(row=2, column=0)
        self.ti = gui.TextInputBlock(self, 'blah2')
        self.ti.grid(row=3, column=0)
        self.chk = gui.BoolInputBlock(self, 'CHK')
        self.chk.grid(row=4, column=0)

        # Footer
        # Quit Button
        self.quit = ttk.Button(self, text="QUIT", command=self.master.destroy)
        self.quit.grid(row=999, column=999)
        # Run Button
        self.btn_run = ttk.Button(self, text='RUN', command=None)
        self.btn_run.grid(row=998, column=999)

root = Tk()
app = Application(master=root)
app.mainloop()