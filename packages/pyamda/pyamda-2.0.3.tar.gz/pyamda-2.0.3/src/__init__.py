import inspect
from src.pyamda import core

for name, obj in inspect.getmembers(core, inspect.isfunction):
    if obj.__module__ == "pyamda.core":
        globals()[name] = obj

from src.pyamda import clss
from src.pyamda import strs
from src.pyamda import bools
from src.pyamda import dicts
from src.pyamda import iters
from src.pyamda import lists
from src.pyamda import maths
