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

import tkinter as tk
from tkinter import ttk
from typing import Union, get_args, get_origin
from enum import EnumMeta, Enum, IntEnum, Flag, IntFlag
from dataclasses import dataclass
import inspect
import re

class ParamInputFrame(ttk.Frame):
    def __init__(self, parent: ttk.Frame, entry_description: str):
        super().__init__(parent)
        # Base Frame
        self.frame = ttk.Frame(parent)
        # Entry Label
        self.lbl = ttk.Label(self.frame, text=entry_description, anchor='nw', wraplength=450)

    def place(self, row=0, column=0, padx=5, pady=5, sticky='w'):
        self.frame.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)

    def get_value(self):
        raise NotImplementedError('Derived class must override')

    def set_value(self, value):
        raise NotImplementedError('Derived class must override')

    @staticmethod
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


class ComboBoxBlock(ParamInputFrame):
    def __init__(self, parent: ttk.Frame, entry_description: str,
                 source: Union[dict, EnumMeta, list], on_select = None, default = None):
        """
        Combo Box input frame.
        :param parent: Parent Frame
        :param entry_description: Text to display at top of frame
        :param source: A dictionary, enum, or list to generate items from
        :param on_select: f(c: ComboBoxBlock) to call when selection is updated
        """
        super().__init__(parent, entry_description)
        # ComboBox
        self.selection = tk.StringVar()
        if type(source) in (list, tuple):
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
        try:
            assert type(self._source) is dict, f'Could not convert source to dict: {type(self._source)}'
        except AssertionError:
            raise
        self.combobox = ttk.Combobox(self.frame, textvariable=self.selection)
        self.on_select = on_select
        self.combobox.bind('<<ComboboxSelected>>', self._on_select)
        # Set up default values and whether to allow manual entry
        self.combobox['values'] = [x for x in self._source if x != '_manual']
        if '_manual' not in self._source:
            self.combobox.state(['readonly'])
            keys = list(self._source.keys())
            self.selection.set(keys[0])
            for key in keys:
                if self._source[key] == default:
                    self.selection.set(key)
        else:
            self.combobox.bind('<FocusOut>', self._on_select)
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

    def set_value(self, value: str):
        if not '_manual' in self._source:
            assert value in self._source, 'Invalid Setting'
        self.selection.set(value)

    def _on_select(self, e):
        if self.on_select is not None:
            try:
                self.on_select(self.get_value())
            except ValueError:
                self.on_select('INVALID ENTRY')


class TextInputBlock(ParamInputFrame):
    def __init__(self, parent: ttk.Frame, entry_description: str, entry_default: str = '', entry_type: type = None):
        super().__init__(parent, entry_description)
        # Entry
        self.entry_text = tk.StringVar()
        self.entry_text.set(entry_default)
        self.entry_type = entry_type
        self.entry = ttk.Entry(self.frame, width=60, textvariable=self.entry_text)

        self.grid_items()

    def grid_items(self):
        self.lbl.grid(row=0, sticky='w')
        self.entry.grid(row=1, column=0, columnspan=2, sticky='w')

    def get_value(self):
        return self.entry_type(self.entry_text.get())

    def set_value(self, value):
        return self.entry_text.set(value)


class BoolInputBlock(ParamInputFrame):
    def __init__(self, parent: ttk.Frame, entry_description: str, entry_default: bool = False):
        super().__init__(parent, entry_description)
        # Checkbox
        self.checked = tk.BooleanVar()
        self.checked.set(entry_default)
        self.check_box = ttk.Checkbutton(self.frame, variable=self.checked)

        self.grid_items()

    def get_value(self) -> bool:
        return self.checked.get()

    def set_value(self, value: bool):
        self.checked.set(value)

    def grid_items(self):
        self.lbl.grid(row=0, sticky='w')
        self.check_box.grid(row=1, column=0, sticky='w')


class ReturnLabelBlock(ttk.Frame):
    def __init__(self, parent: ttk.Frame, return_description: str, return_value = None):
        super().__init__(parent)

        self.frame = ttk.Frame(parent, borderwidth = 3, relief = 'ridge')

        self.description_lbl = ttk.Label(self.frame, text=return_description, anchor='nw', wraplength=450)

        self.return_value = return_value
        try:
            return_value_text = str(return_value)[:256]
        except Exception:
            return_value_text = '<Object>'
        self.return_text = f'{return_value_text}'[:256]
        self.return_lbl = tk.Text(self.frame, width=60, height=1 + (len(self.return_text)//60))
        self.return_lbl.insert(1.0, self.return_text)
        self.return_lbl.configure(state='disabled')
        self.grid_items()

    def grid_items(self):
        self.description_lbl.grid(row=0, sticky='w')
        self.return_lbl.grid(row=1, sticky='w')

    def place(self, row=0, column=0, padx=5, pady=5, sticky='w'):
        self.frame.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)

    def remove(self):
        self.frame.grid_forget()
        self.destroy()

    def get_value(self):
        return self.return_value


class ArgInfo:
    """Class for arg info"""
    def __init__(self, name: str = '', description: str = '', data_type: type = None, default = None, override = None):
        self.name = name
        self.description = description
        self.data_type = data_type
        self.default = default
        self.override = override


class FunctionGUI(ttk.Frame):
    def __init__(self, parent: ttk.Frame, func, func_description: str, args_info: dict[str, ArgInfo]):
        super().__init__(parent)
        self.func = func
        # Base Frame
        self.frame = ttk.Frame(parent, borderwidth = 3, relief = 'ridge')
        # Entry Label
        self.lbl_func_description = ttk.Label(self.frame, text=func_description, anchor='nw', wraplength=450)
        self.lbl_func_description.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'w')
        self.args_info = args_info
        self.arg_guis = {}  # type: dict[str, ParamInputFrame]
        for arg in args_info:
            if arg == 'return':
                continue
            arg_gui = self.get_arg_input_gui(arg, args_info[arg])
            if arg_gui is not None:
                self.arg_guis[arg] = self.get_arg_input_gui(arg, args_info[arg])

        # Place function gui + output labels
        n = 1
        for arg in self.arg_guis:
            self.arg_guis[arg].place(row=n)
            n += 1
        self.lbl_result = ttk.Label(self.frame, text='', anchor='nw', wraplength=450)
        self.lbl_result.grid(row=n, column=0, padx=5, pady=5, sticky='w')
        n += 1
        self.lbl_error = ttk.Label(self.frame, text = '', anchor='nw', wraplength = 450)
        self.lbl_error.grid(row=n, column=0, padx=5, pady=5, sticky='w')

    def get_arg_input_gui(self, arg: str, arg_info: ArgInfo):
        if arg_info.override is not None:
            if type(arg_info.override) in (dict, list, tuple, EnumMeta):
                return ComboBoxBlock(parent=self.frame, source=arg_info.override, default=arg_info.default,
                                     entry_description=f'{arg_info.name}: {arg_info.description}')
            elif callable(arg_info.override):
                return self.build_function_gui(self.frame, arg_info.override)
        elif arg_info.data_type in (int, float, complex, str):
            return TextInputBlock(parent=self.frame, entry_default=arg_info.default,
                                  entry_description=f'{arg_info.name}: {arg_info.description}',
                                  entry_type=arg_info.data_type)
        elif arg_info.data_type is bool:
            return BoolInputBlock(parent=self.frame, entry_default=bool(arg_info.default),
                                  entry_description=f'{arg_info.name}: {arg_info.description}')
        else: return None

    @staticmethod
    def build_function_gui(parent: ttk.Frame, func):
        def cleanup_string(s):
            return re.sub(r'\s{2,}', ' ', s.strip())
        # docstring_entry_pattern = f':{entry}:\s+(.*?)(?::|$)'
        fas = inspect.getfullargspec(func)
        args_info = {} # type: dict[str, gui.ArgInfo]

        # Grab function description
        if func.__doc__ is None or func.__doc__ == '':
            description = '<No Description>'
        else:
            desc_re = re.search(r'^(.*?)(?::|$)', func.__doc__, re.DOTALL | re.IGNORECASE)
            if desc_re is None:
                description = '<Description Parse Failure>'
            else:
                description = cleanup_string(desc_re[1])

        # Grab args infos
        for arg in fas.args:
            # Name
            args_info[arg] = ArgInfo(name=arg)
            # Description
            if func.__doc__ is None:
                args_info[arg].description = ''
            else:
                docstring_entry_pattern = r':param ARG:\s+(.*?)(?::|$)'.replace('ARG', arg)
                arg_docstring = re.search(docstring_entry_pattern, func.__doc__, re.DOTALL | re.IGNORECASE)
                if arg_docstring is None:
                    args_info[arg].description = ''
                else:
                    args_info[arg].description = cleanup_string(arg_docstring[1])
            # Override
            if hasattr(func, f'_pggui_{arg}'):
                ovr = getattr(func, f'_pggui_{arg}')
                args_info[arg].override = ovr

        # Default Values and Types
        args = list(fas.args)
        if fas.defaults is not None:
            # Arrange for arg list and defaults list to be same length
            defaults = list(fas.defaults)
            while len(defaults) < len(args):
                defaults.insert(0, None)
            for i in range(len(args)):
                # Skip first arg on methods
                if inspect.ismethod(func):
                    if i == 0:
                        continue
                args_info[args[i]].default = defaults[i]
        else:
            for i in range(len(args)):
                # Skip first arg on methods
                if inspect.ismethod(func):
                    if i == 0:
                        continue
                args_info[args[i]].default = None
        for i in range(len(args)):
            arg = args[i]
            if inspect.ismethod(func):
                if i == 0:
                    continue
            try:
                anno_type = fas.annotations[arg]
                if get_origin(anno_type) == Union:
                    if bool in get_args(anno_type):
                        anno_type = bool
                    else:
                        for x in (str, int, float, complex):
                            if x in get_args(anno_type):
                                anno_type = x
                                break
                args_info[arg].data_type = anno_type
            except KeyError:
                # It's okay if the annotation is missing on overridden params
                if args_info[arg].override is not None:
                    continue
                raise

        return_type = None if 'return' not in fas.annotations else fas.annotations['return']
        if func.__doc__ is None or func.__doc__ == '':
            return_desc = ''
        else:
            return_re = re.search(r':return.*?:\s+(.*?)(?::|$)', func.__doc__, re.DOTALL | re.IGNORECASE)
            return_desc = '' if return_re is None else cleanup_string(return_re[1])
        args_info['return'] = ArgInfo(name='return', description=return_desc, data_type=return_type, default=None)
        return FunctionGUI(parent=parent, func=func, func_description=description, args_info=args_info)

    def place(self, row=0, column=0, padx=5, pady=5, sticky='w'):
        self.frame.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)

    def remove(self):
        self.frame.grid_forget()
        self.destroy()

    def run_function(self):
        kwargs = {}
        for arg in self.arg_guis:
            arg_gui = self.arg_guis[arg]
            kwargs[arg] = arg_gui.get_value()
        result = self.func(**kwargs)
        if 'return' in self.args_info:
            return_info = self.args_info['return'].description
            return_text = f'Last Function Returned: {str(type(result))}\n\nReturn Desc: {return_info}'
        else:
            return_text = f'Last Function Returned: {str(type(result))}\n'
        return result, return_text

    def get_value(self):
        return self.run_function()[0]
