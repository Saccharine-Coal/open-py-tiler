import os

import pygame as pg

import color


class  File:
    """A python object that represents a valid and supported file. Holds the file type and python object type."""
    __slots__ = ("__dict__", "filename", "filepath", "data", "_verbose", "_WHITE", "_RED", "_GREEN", "_ORANGE", "_BLUE", "_PURPLE")
    def __init__(self, path: str, filetype: str, data: object, _verbose=False) -> None:
        self.filetype = filetype
        self.filepath = path
        self._verbose = _verbose
        self.data = data
    @property
    def type(self):
        "Get the object type the file is holding."
        return type(self.data)

    def __repr__(self) -> str:
        name = color.color_str(self.__class__.__name__, "yellow")
        filepath = f"path={self.filepath}, "
        types = f"filetype={self.filetype}, type={self.type},
        data = f"data={self.data}"
        return name + "(" + filepath + types + data + ")"
if __name__ == "__main__":
    c = StrColorizer()
    print("white " + c.get_colored_str("hi", "red"), c.get_colored_str("green", "green"))
