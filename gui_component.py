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
from typing import Union, get_args, get_origin
from enum import EnumMeta, Enum, IntEnum, Flag, IntFlag

class ParamInputFrame(ttk.Frame):
    def __init__(self, parent: ttk.Frame, entry_description: str):
        super().__init__(parent)
        # Base Frame
        self.frame = ttk.Frame(parent)
        # Entry Label
        self.lbl = ttk.Label(self.frame, text=entry_description, anchor='nw', wraplength=450)

    def place(self, row=0, column=0, padx=5, pady=5, sticky='w'):
        self.frame.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)


class ComboBoxBlock(ParamInputFrame):
    def __init__(self, parent: ttk.Frame, entry_description: str,
                 source: Union[dict, EnumMeta, list], on_select = None):
        """
        Combo Box input frame.
        :param parent: Parent Frame
        :param entry_description: Text to display at top of frame
        :param source: A dictionary, enum, or list to generate items from
        :param on_select: f(c: ComboBoxBlock) to call when selection is updated
        """
        super().__init__(parent, entry_description)
        # ComboBox
        self.selection = StringVar()
        if type(source) is list:
            s = {}
            for item in source:
                s[str(item)] = item
            self._source = s
        elif type(source) is EnumMeta:
            s = {}
            for item in source:
                s[item.name] = item
            self._source = s
        else:
            self._source = source
        assert type(self._source) is dict, f'Could not convert source to dict: {type(self._source)}'
        self.combobox = ttk.Combobox(self.frame, textvariable=self.selection)
        self.on_select = on_select
        self.combobox.bind('<<ComboboxSelected>>', self._on_select)
        self.combobox.bind('<FocusOut>', self._on_select)
        # Set up default values and whether to allow manual entry
        self.combobox['values'] = [x for x in self._source if x != '_manual']
        if '_manual' not in self._source:
            self.combobox.state(['readonly'])
        self.grid_items()

    def grid_items(self):
        self.lbl.grid(row=0, sticky='w')
        self.combobox.grid(row=1, column=0, columnspan=2, sticky='w')

    def get_value(self):
        try:
            return self._source[str(self.selection.get())]
        except KeyError:
            try:
                return self._source['_manual'](self.selection.get())
            except ValueError:
                raise ValueError(f'Invalid Input: {self.selection.get()}')

    def _on_select(self, e):
        if self.on_select is not None:
            try:
                self.on_select(self.get_value())
            except ValueError:
                # TODO Output error or otherwise indicate bad input
                pass



class TextInputBlock(ParamInputFrame):
    def __init__(self, parent: ttk.Frame, entry_description: str, entry_default: str = ''):
        super().__init__(parent, entry_description)
        # Entry
        self.entry_text = StringVar()
        self.entry_text.set(entry_default)
        self.entry = ttk.Entry(self.frame, width=60, textvariable=self.entry_text)

        self.grid_items()

    def grid_items(self):
        self.lbl.grid(row=0, sticky='w')
        self.entry.grid(row=1, column=0, columnspan=2, sticky='w')

    def get_value(self):
        return self.entry_text.get()

    def set_value(self):
        return self.entry_text.set()


class BoolInputBlock(ParamInputFrame):
    def __init__(self, parent: ttk.Frame, entry_description: str, entry_default: bool = False):
        super().__init__(parent, entry_description)
        # Checkbox
        self.checked = BooleanVar()
        self.checked.set(entry_default)
        self.check_box = ttk.Checkbutton(self.frame, variable=self.checked)

        self.grid_items()

    def grid_items(self):
        self.lbl.grid(row=0, sticky='w')
        self.check_box.grid(row=1, column=0, sticky='w')