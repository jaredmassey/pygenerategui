import tkinter as tk
from tkinter import ttk
import inspect
from typing import Union, get_args, get_origin
from enum import EnumMeta, Enum, IntEnum, Flag, IntFlag
import re

import pygenerategui.gui_component as gui


def pggui(name = None, **kwargs):
    """
    Add _pggui_name to a routine so it will be identified as a pggui function
    :param name: The name it should appear as in the function list. Will use func name if none supplied.
    :param kwargs: Overrides for function params - dict, list, tuple, enum, or callable
    """
    if inspect.isroutine(name):
        return pggui()(name)
    def decorator(func):
        for kwarg in kwargs:
            kwarg_name = f'_pggui_{kwarg}'
            kwarg_value = kwargs[kwarg]
            setattr(func, kwarg_name, kwarg_value)
        func._pggui_name = func.__name__ if name is None else name
        return func
    return decorator


class PGGUI_App(ttk.Frame):
    """
    Builds and runs the main app
    Layout is:
    - Header: Combobox with available functions
    - Function GUI
    - Footer: Run + Quit buttons
    """
    def __init__(self, components: list, title: str = 'PGGUI App'):
        root = tk.Tk()
        root.title = title
        super().__init__(root)
        self.pggui_functions = {}
        function_list = []
        for components in components:
            function_list += self.load_funcs(components)
        for func in function_list:
            self.pggui_functions[func._pggui_name] = func
        self.grid(row=0, column=0)
        self.init_gui()

    def load_funcs(self, component):
        """
        Modeled loosely off of robotlibcore's add_library_components
        :param component: A module, class, or an instance of a class, containing routines to be potentially turned into GUIs
        :return: A list containing any functions which are flagged to be turned into a GUI
        """
        pggui_funcs = []

        def _get_members(c):
            if not inspect.isclass(c):
                result = [m[1] for m in inspect.getmembers(c) if inspect.isroutine(m[1])]
                return result
            else:
                members = []
                im = dict(inspect.getmembers(c))
                for m in im:
                    if inspect.isroutine(im[m]):
                        # Only returns True on bound methods
                        if inspect.ismethod(im[m]):
                            members.append(im[m])
                        elif m in c.__dict__ and type(c.__dict__[m]) is staticmethod:
                            members.append(im[m])
                return members

        for member in _get_members(component):
            if hasattr(member, '_pggui_name'):
                pggui_funcs.append(member)
        return pggui_funcs

    def init_gui(self):
        # Header
        self.header = gui.ComboBoxBlock(self, entry_description='Select A Function To Run', source=self.pggui_functions,
                                        on_select=self.combobox_selection_changed)
        self.header.place(row=1)

        # Function GUI
        self.function_frame = ttk.Frame(self)
        self.function_frame.grid(row=5, column=0, columnspan=999, sticky='w')
        self.fgui = gui.FunctionGUI.build_function_gui(self.function_frame, self.header.get_value())
        self.fgui.place()

        # Footer
        # Result Display:
        self.result_frame = ttk.Frame(self)
        self.result_frame.grid(row=997, column=0, columnspan=999, sticky='w')
        self.rgui = None
        # Run Button
        self.btn_run = ttk.Button(self, text='RUN', command=self.run_function)
        self.btn_run.grid(row=998, column=999)
        # Quit Button
        self.quit = ttk.Button(self, text="QUIT", command=self.master.destroy)
        self.quit.grid(row=999, column=999)

    def combobox_selection_changed(self, value):
        self.fgui.remove()
        self.fgui = gui.FunctionGUI.build_function_gui(self.function_frame, value)
        # self.btn_run['command'] = self.fgui.run_function
        self.fgui.place()

    def run_function(self):
        try:
            result = self.fgui.run_function()
        except Exception as e:
            result =  None, f'ERROR: {str(e)}'
        result_gui = gui.ReturnLabelBlock(self.result_frame, result[1], result[0])
        if self.rgui is not None:
            self.rgui.remove()
        self.rgui = result_gui
        self.rgui.place()
