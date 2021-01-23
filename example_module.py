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

from pygenerategui import pggui

@pggui(name="MyFunc", z={'a':17.3, 'b':12.1})
def example_func(x: str = 'Hello', y: bool = True, z: float = 12.1) -> str:
    """
    A test function
    :param x: The exxxx param
    :param y: The whyyyyyyy param
    :return: The string 'Heya!'
    """
    return f'x is: {x}, y is: {str(y)}, and z is: {str(z)}'

@pggui
def example_func2(x: str = 'Purple', y: bool = False, z: float = 99.9) -> str:
    """
    A test function
    :param x: The exxxx param
    :param y: The whyyyyyyy param
    :return: The string 'Heya!'
    """
    return f'x is: {x}, y is: {str(y)}, and z is: {str(z)}'