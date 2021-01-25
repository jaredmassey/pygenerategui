# pygenerategui
Utility for generating simple GUI to execute Python code

This was originally a hobby project, but I realized it could be useful at work. I'm an SDET, and I think this could be a handy way to e.g. expose an existing automation library's functionality to people uncomfortable with scripting. I'm sure it could be valuable in any number of other cases.

I've chosen the painful option of tkinter for the sake of maximum portability. You shouldn't need any modules that don't come in a typical python install.

Run `python example_app_base.py` for examples

Most functionality is demonstrated in `example_module.py`

### Basic Usage
- Decorate functions with `@pggui`. Make an app launcher file modeled after `example_app_base.py`, then run it with python (or maybe make a shell script to do so, so that your target users just have to double-click a file. :)
  - Function args should have type hinting or be overridden (see advanced section)
  - Param / return info from docstring is shown in UI
  - Default values are set
  - Return or error are displayed
    
### Advanced Usage
- Function name can be replaced in ui by specifing `name` argument of decorator
- Arguments can be limited to a predefined set using dict, enum, or list by overriding the arg in decorator args
  - This is also useful if the argument is not a basic type (bool, string, number)
- Example: @pggue(name='MyFunc', arg2=some_dict)

### TODO
- Add ability for args to be overridden with another function, and nest that function's args in UI
- Add ability for returned values to be stored and passed in to some other function
- Better error messaging
- Scrollbars (if anybody knows good doc / practical example of tkinter scrollbars, hmu!)

Send me a note if you're using this, I'm curious!
