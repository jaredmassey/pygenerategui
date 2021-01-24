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

from pygenerategui import load_funcs
import pygenerategui.gui_component as gui

import example_module

class PGGUI_App(ttk.Frame):
    """
    Builds and runs the main app
    Layout is:
    - Header: Combobox with available functions
    - Function GUI
    - Footer: Run + Quit buttons
    """
    def __init__(self, master, function_list):
        super().__init__(master)
        self.master = master
        self.pggui_functions = {}
        for func in function_list:
            self.pggui_functions[func._pggui_name] = func
        self.grid(row=0, column=0)
        self.init_gui()

    def init_gui(self):

        # Header
        self.header = gui.ComboBoxBlock(self, entry_description='Select A Function To Run', source=self.pggui_functions,
                                        on_select=self.combobox_selection_changed)
        self.header.place(row=1)

        # Function GUI
        self.function_frame = ttk.Frame(self)
        self.function_frame.grid(row=5, column=0, columnspan=999)
        self.fgui = self.build_function_gui(self.header.get_value())
        self.fgui.place()

        # Footer
        # Quit Button
        self.quit = ttk.Button(self, text="QUIT", command=self.master.destroy)
        self.quit.grid(row=999, column=999)
        # Run Button
        self.btn_run = ttk.Button(self, text='RUN', command=self.fgui.run_function)
        self.btn_run.grid(row=998, column=999)

    def combobox_selection_changed(self, value):
        self.fgui.remove()
        self.fgui = self.build_function_gui(value)
        self.btn_run['command'] = self.fgui.run_function
        self.fgui.place()

    def build_function_gui(self, f):
        def cleanup_string(s):
            return re.sub(r'\s{2,}', ' ', s.strip())
        # docstring_entry_pattern = f':{entry}:\s+(.*?)(?::|$)'
        fas = inspect.getfullargspec(f)
        args_info = {} # type: dict[str, gui.ArgInfo]

        # Grab function description
        if f.__doc__ is None:
            description = '<No Description>'
        else:
            desc_re = re.search(r'^(.*?)(?::|$)', f.__doc__, re.DOTALL | re.IGNORECASE)
            if desc_re is None:
                description = '<Description Parse Failure>'
            else:
                description = cleanup_string(desc_re[1])

        # Grab args infos
        for arg in fas.args:
            # Name
            args_info[arg] = gui.ArgInfo(name=arg)
            # Description
            if f.__doc__ is None:
                args_info[arg].description = ''
            else:
                docstring_entry_pattern = r':param ARG:\s+(.*?)(?::|$)'.replace('ARG', arg)
                arg_docstring = re.search(docstring_entry_pattern, f.__doc__, re.DOTALL | re.IGNORECASE)
                if arg_docstring is None:
                    args_info[arg].description = ''
                else:
                    args_info[arg].description = cleanup_string(arg_docstring[1])
            # Override
            if hasattr(f, f'_pggui_{arg}'):
                args_info[arg].override = getattr(f, f'_pggui_{arg}')

        # Default Values and Types
        if fas.defaults is not None:
            # Arrange for arg list and defaults list to be same length
            defaults = list(fas.defaults)
            args = list(fas.args)
            while len(defaults) < len(args):
                defaults.insert(0, None)
            for i in range(len(args)):
                # Skip first arg on methods
                if inspect.ismethod(f):
                    if i == 0:
                        continue
                args_info[args[i]].default = defaults[i]
                try:
                    args_info[args[i]].data_type = fas.annotations[args[i]]
                except KeyError:
                    # It's okay if the annotation is missing on overridden params
                    if args_info[args[i]].override is not None:
                        continue
                    raise

        return_type = None if 'return' not in fas.annotations else fas.annotations['return']
        return_re = re.search(r':return.*?:\s+(.*?)(?::|$)', f.__doc__, re.DOTALL | re.IGNORECASE)
        return_desc = '' if return_re is None else cleanup_string(return_re[1])
        args_info['return'] = gui.ArgInfo(name='return', description=return_desc, data_type=return_type, default=None)
        return gui.FunctionGUI(parent=self.function_frame, func=f, func_description=description, args_info=args_info)


root = Tk()
root.title('PGGUI')
modules = []
for x in (example_module, example_module.StaticClassExample, example_module.InstanceClassExample(12)):
    modules += load_funcs(x)
app = PGGUI_App(master=root, function_list=modules)
app.mainloop()
