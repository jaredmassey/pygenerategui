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
    :param component: A module or an instance of a class, containing functions or methods to be potentially tuned into GUIs
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
        self.create_widgets()
        self.bcount = 1

    def add_button(self, text, command):
        btn = ttk.Button(self, text=text, command=command)
        btn.pack(side="top")

    def add_cbutton(self):
        # self.add_button(str(self.bcount) * 10, self.add_cbutton)
        self.add_button(str(self.ti.get_value()) * 10, self.add_cbutton)
        self.bcount += 1

    def create_widgets(self):
        self.hi_there = ttk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there.grid(row=0, column=0)
        self.quit = ttk.Button(self, text="QUIT", command=self.master.destroy)
        self.btn_run = ttk.Button(self, text='RUN', command=None)
        self.ti = TextInputSection(self, 'blah')
        self.ti.grid(row=1, column=0)
        self.btn_run.grid(row=998, column=999)
        self.quit.grid(row=999, column=999)


    def say_hi(self):
        print("hi there, everyone!")


class TextInputSection(ttk.Frame):
    def __init__(self, parent: ttk.Frame, text: str):
        super().__init__(parent)
        self.frame = ttk.Frame(parent)
        self.frame.grid(padx=5, pady=5)
        self.lbl = ttk.Label(self.frame, text=text, anchor='nw', wraplength=600)
        self.entry = ttk.Entry(self.frame, width=80)
        self.grid_items()

    def grid_items(self):
        self.lbl.grid(row=0, sticky='w')
        self.entry.grid(row=1, column=0, columnspan=2, sticky='w')

    def get_value(self):
        return self.entry.get()

root = Tk()
app = Application(master=root)
app.mainloop()