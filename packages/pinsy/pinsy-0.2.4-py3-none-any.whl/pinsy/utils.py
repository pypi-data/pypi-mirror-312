"""
### Utils
A simple module that provides utility functions related to ANSI functionality.

#### Functions include:
- `read_key`: Read a single keypress supporting Up/Down arrow keys (platform independent)
- `read_key_windows`: Read a single keypress supporting Up/Down arrow keys (windows)
- `read_key_unix`: Read a single keypress supporting Up/Down arrow keys (linux/macos)
- `clear_line`: clear current line
- `clear_lines_above`: clear n lines above
- `clear_screen`: clear screen (only visible part)
- `clear_terminal`: clear terminal session
- `move_cursor_up`: move cursor n lines up
- `move_cursor_down`: move cursor n lines down
- `get_cursor_position`: get cursor's current position `(x, y)`
- `get_terminal_size`: get terminal's size `(width, height)`
- `type_match`: similar to `isinstance()` but handles more complex types
- `typecheck`: a decorator which enforces types using type hints

"""

from __future__ import annotations

import sys
import os
from shutil import get_terminal_size
import re

if os.name == "nt":  # Windows
    import msvcrt
    import ctypes
    from ctypes import wintypes
else:  # Unix (mac/linux)
    import tty
    import termios

from inspect import signature
from functools import wraps
from typing import (
    get_origin,
    get_args,
    get_type_hints,
    List,
    Tuple,
    Dict,
    Set,
    Union,
    Optional,
    Literal,
    Any,
    AnyStr,
)
from collections.abc import Iterable


def clear_lines_above(n):
    """Clears `n` lines above and including (current line).
    (only erase `n` lines that are is display)"""
    move_cursor_up(n)
    sys.stdout.write(f"\x1b[J")
    sys.stdout.flush()


def clear_lines_below():
    """Clears all lines below cursor. (erases lines that are is display only)"""
    sys.stdout.write(f"\x1b[0J")
    sys.stdout.flush()


def move_cursor_right(columns: int = 1):
    """Move cursor `columns` characters to the right  >> (stops if hits the end of line)"""
    sys.stdout.write(f"\x1b[{columns}C")
    sys.stdout.flush()


def move_cursor_left(columns: int = 1):
    """Move cursor `columns` characters to the left << (stops if hits the end of line)"""
    sys.stdout.write(f"\x1b[{columns}D")
    sys.stdout.flush()


def move_cursor_to(column: int):
    """Move cursor to `column` in current line, starting from `1` (stops if hits the end of line)"""
    sys.stdout.write(f"\x1b[{column+1}G")
    sys.stdout.flush()


def clear_line():
    """Clears current line"""
    sys.stdout.write("\x1b[2K\r")
    sys.stdout.flush()


def clear_screen():
    """Clear the visible screen"""
    sys.stdout.write("\033[H\033[J")
    sys.stdout.flush()


def clear_terminal():
    """Clear the terminal session"""
    os.system("cls" if os.name == "nt" else "clear")


def move_cursor_up(n=None):
    """Move cursor n lines up. (in visible screen)"""
    n = n if n and n > 0 else None
    sys.stdout.write(f"\x1b[{n}A")
    sys.stdout.flush()


def move_cursor_down(n=None):
    """Move cursor n lines down. (in visible screen)"""
    n = n if n and n > 0 else None
    sys.stdout.write(f"\x1b[{n}B")
    sys.stdout.flush()


def get_cursor_pos() -> tuple[int, int]:
    """Returns the cursor location on visible terminal screen `(x, y)`"""
    if sys.platform == "win32":
        # For Windows
        oldstdin_mode = ctypes.wintypes.DWORD()
        oldstdout_mode = ctypes.wintypes.DWORD()
        kernel32 = ctypes.windll.kernel32

        kernel32.GetConsoleMode(kernel32.GetStdHandle(-10), ctypes.byref(oldstdin_mode))
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 0)
        kernel32.GetConsoleMode(
            kernel32.GetStdHandle(-11), ctypes.byref(oldstdout_mode)
        )
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    else:
        # For Unix-like systems (Mac|Linux)
        oldstdin_mode = termios.tcgetattr(sys.stdin)
        _ = termios.tcgetattr(sys.stdin)
        _[3] = _[3] & ~(termios.ECHO | termios.ICANON)
        termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, _)

    try:
        temp = ""
        # Request cursor position using ANSI
        sys.stdout.write("\x1b[6n")
        sys.stdout.flush()
        # Read the response (keep reading until 'R')
        while not (temp := temp + sys.stdin.read(1)).endswith("R"):
            pass

        # Extract X, Y from response
        res = re.match(r".*\[(?P<y>\d*);(?P<x>\d*)R", temp)
    finally:
        if sys.platform == "win32":
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), oldstdin_mode)
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), oldstdout_mode)
        else:
            termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, oldstdin_mode)

    if res:
        return (res.group("x"), res.group("y"))

    # If cursor pos not found
    return (-1, -1)


def type_match(value: Any, expected_type: Any) -> bool:
    """
    ### Type Match
    Checks if a value is an instance of the expected type, supporting complex
    types from the typing module.

    Similar to built-in `isintance()` but handles more complex types as well.

    #### ARGS:
    - `value`: the value to type check
    - `expected_type`: the expected type to match with...

    #### Supported Types:
    It supports simple types like:
    - `int`,`float`,`str`,`bool`,`None`,`list`,`tuple`,`dict`,`bytes`

    As well as complex types (from `typing` module) like:
    - `Any` a value of any type (skips type checking)
    - `Dict[str, int]`
    - `Iterable[int]`
    - `List[int]`
    - `Optional[int]` indicates an optional value that can either be int or None
    - `Set[int]`
    - `Tuple[str, int]`
    - `Union[int, str]`

    #### Example:
    ```
    >> type_match(4, int)
    True
    >> type_match([1, 2, 3], List[int])
    True
    >> type_match({5, 4, 1}, Dict[str, int])
    False
    ```
    """
    # Get the origin of the type (list, tuple, etc.)
    origin_type = get_origin(expected_type)

    # Handle None
    if expected_type is None:
        return isinstance(value, type(None))

    # Handle Any
    if expected_type is Any:
        return True

    # Handle Basic types (int, float etc.)
    if origin_type is None:
        # Ints are valid floats
        if expected_type is float and type(value) is int:
            return True

        return type(value) == expected_type

    if type(value) == bool:  # Cannot be bool below this point
        return False

    # If value is None, return False, (cannot be None below this point)
    if value == None and origin_type is not Union:  # Union check for 'Optional'
        return False

    # Get the arguments inside the type (e.g int in List[int])
    type_args = get_args(expected_type)

    # Handle List
    if origin_type is list:
        if type_args:
            items_check = all(type_match(item, type_args[0]) for item in value)
            return isinstance(value, list) and items_check
        return isinstance(value, list)

    # Handle Tuple
    if origin_type is tuple:
        if type_args and isinstance(value, tuple):
            if len(type_args) == len(value):
                return all(
                    type_match(item, type_arg)
                    for item, type_arg in zip(value, type_args)
                )
            elif len(type_args) == 1:
                return all(type_match(item, type_args[0]) for item in value)
            return False
        return isinstance(value, tuple)

    # Handle Dict
    if origin_type is dict:
        if type_args and isinstance(value, dict):
            key_type, value_type = type_args
            key_check = all(type_match(k, key_type) for k in value.keys())
            value_check = all(type_match(v, value_type) for v in value.values())
            return key_check and value_check
        return isinstance(value, dict)

    # Handle Set
    if origin_type is set:
        if type_args and isinstance(value, set):
            return all(type_match(item, type_args[0]) for item in value)
        return isinstance(value, set)

    # Handle Union
    if origin_type is Union:
        return any(type_match(value, arg) for arg in type_args)

    # Handle Optional (equivalent to Union[Any, None])
    if origin_type is Union and type(None) in type_args:
        actual_type = type_args[0] if type_args[1] is type(None) else type_args[1]
        return value is None or type_match(value, actual_type)

    # Handle Iterable
    if origin_type is Iterable:
        if not isinstance(value, Iterable):
            return False
        items_check = all(type_match(item, type_args[0]) for item in value)
        return items_check

    # TODO: Handle these too...
    # Callable[[ArgTypes], ReturnType]
    # ...

    # Fallback: if type doesn't match with any of above
    return False


def typecheck(func=None, *, skip: Iterable[str] = None, only: Iterable[str] = None):
    """
    ### Type Check
    A decorator that enforces type checking on function arguments and return values
    based on the type hints provided in the function.

    If an argument doesn't match the specified type, a `TypeError` is raised with
    a message.

    #### ARGS:
    - `func`: the function to which the decorator is applied.
    - `skip`: the arguments to skip (names should match exactly!)
    - `only`: the arguments to typecheck (`skip` and `only` are mutually exclusive! meaning, when using `skip`, DON'T use `only`, and vice versa)

    #### Supported Types:
    It supports simple types like:
    - `int`,`float`,`str`,`bool`,`None`,`list`,`tuple`,`dict`,`bytes`

    As well as complex types (from `typing` module) like:
    - `Any` a value of any type (skips type checking)
    - `Dict[str, int]`
    - `Iterable[int]`
    - `List[int]`
    - `Optional[int]` indicates an optional value that can either be int or None
    - `Set[int]`
    - `Tuple[str, int]`
    - `Union[int, str]`

    #### Example:
    ```
    @typecheck
    >> def add(a:int, b:int) -> int:
    ..    return a + b
    ..
    >> add(1, 2) # Works fine, returns 3
    >> add(1, "2") # Raises TypeError
    TypeError: Argument 'b' must be <class 'int'>, but got <class 'str'>
    ..
    @typecheck(skip=['b']) # Skips 'b', only typechecks 'a'
    >> def add(a:int, b:int) -> int:
    ..    return a + b
    ..
    >> add(1, 2.5)
    3.5
    @typecheck(only=['b']) # Only typechecks 'b'
    >> def add(a:int, b:int) -> int:
    ..    return a + b
    ..
    >> add(1.5, 2.5)
    TypeError: Argument 'b' must be <class 'int'>, but got <class 'float'>
    ```

    #### NOTE:
    This decorator does not preserve metadata of the function if used without arguments.
    ```
    # Metadata (docstring etc.) won't be preserved this way
    @typecheck
    >> def add(a:int, b:int) -> int:
    ..    return a + b
    ..
    # Simple fix, Just add parentheses
    @typecheck()
    >> def add(a:int, b:int) -> int:
    ..    return a + b
    ..
    ```

    Raises `TypeError` if argument types or return type do not match annotated type hints.
    """
    if skip or only:
        assert bool(skip) ^ bool(only), "skip and only are mutually exclusive."

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get the function signature and annotations (type hints)
            sig = signature(func)
            hints = get_type_hints(func)

            # bind the arguments to their names (mapping argument values to parameter names)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()

            # Return Prematurely, if no hints given
            if not hints:
                return func(*args, **kwargs)

            # Check the types of each argument against the type hints
            for arg_name, arg_value in bound_args.arguments.items():
                # Skip the requested args
                if skip and arg_name in skip:
                    continue

                # Typecheck Only the requested args
                if only and arg_name not in only:
                    continue

                if arg_name in hints:  # Only check if there's a type hint
                    # TODO: Normalize Hint names
                    expected_type = hints[arg_name]
                    if not type_match(arg_value, expected_type):
                        raise TypeError(
                            f"Argument '{arg_name}' must be {expected_type}, but got {type(arg_value).__name__}"
                        )

            # Execute the function and capture result
            result = func(*args, **kwargs)

            # Check return type (if there's a return type)
            if "return" in hints:
                if not type_match(result, hints["return"]):
                    raise TypeError(
                        f"Return value must be {hints['return']}, but got {type(result).__name__}"
                    )

            return result

        return wrapper

    # If 'typecheck' used without arguments
    if func:
        return decorator(func)

    # If used with arguments
    return decorator
