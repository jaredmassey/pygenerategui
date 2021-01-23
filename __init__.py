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

import inspect

def pggui(name=None, **kwargs):
    """
    Add _pggui_name to a routine so it will be identified as a pggui function
    :param name: The name it should appear as in the function list. Will use func name if none supplied.
    :param kwargs: Overrides for function params - dict, list, tuple, enum, or callable
    """
    if callable(name):
        return pggui()(name)
    def decorator(func):
        func._pggui_name = name if name is not None else func.__name__
        for kwarg in kwargs:
            setattr(func, f'_pggui_{kwarg}', kwargs[kwarg])
        return func
    return decorator


def load_funcs(component):
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
            for m in inspect.getmembers(c):
                if inspect.ismethod(m):
                    members.append(m)
                elif type(c.__dict__(m.__name__)) is staticmethod:
                    members.append(m)
            return members

    for member in _get_members(component):
        if hasattr(member, '_pggui_name'):
            pggui_funcs.append(member)
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