import os, json

import pygame as pg

import files
import color

class FileManager:
    """Handles all loading and saving of files for the game."""
    #_verbose: bool = field(default=False, repr=False)
    #paths: dict[str: files.File] = field(init=False, repr=True)
    def __init__(self):
        self._type_to_func = {
            "json": self._load_json,
            "png": self._load_image,
            "bmp": self._load_image,
            "jpg": self._load_image
        }
        self._supported_types = self._type_to_func.keys()
        self.paths: dict[str: files.File] = {}

    def add(self, path: str, file: files.File) -> None:
        """Add file and load data into Python object file from given path."""
        #filepath = os.path.join(*list(paths + [filename]))
        if path in self.paths.keys():
            print(f"fp={filepath} already exists!")
        else:
            self.paths[path] = file

    def get(self, path: str) -> files.File:
        """Get Python object data from file with given path."""
        #filepath = os.path.join(*list(paths + [filename]))
        if path in self.paths.keys():
            file: files.File = self.paths.get(path)
            return file
        else:
            raise KeyError

    def load(self, path: str) -> files.File:
        """Path = /path/to/file."""
        filetype = self._get_filetype(path)
        if self._is_supported_and_exists(path, filetype):
            if path in self.paths.keys():
                return self.get(path)
            else:
                load_func = self._type_to_func.get(filetype)
                data = load_func(path)
                file = files.File(path, filetype, data, _verbose=True)
                self.add(path, file)
                return file
        else:
            self._get_path_stack(path)
            raise TypeError("Type is not supported")

    def _get_path_stack(self, path: str) -> None:
        "Debugging tool. Print valid and invalid paths from given path."
        invalid = True
        invalid_dirs: list[str] = []
        truncated_path = path
        while invalid:
            (truncated_path, invalid_dir) = os.path.split(truncated_path)
            invalid_dirs.append(invalid_dir)
            if os.path.exists(truncated_path) or not truncated_path:
                # path is valid
                invalid = False
            invalid_dirs.reverse()
        print(f"""{color.color_str("Path", "yellow")}(valid path={color.color_str(truncated_path, "green")}, invalid dirs={color.color_str(os.path.join(*invalid_dirs), "red")})""")
        raise ValueError

    def _is_supported_and_exists(self, path: str, filetype: str) -> bool:
        result = os.path.exists(path)
        return (os.path.exists(path)) and (filetype in self._supported_types)

    @staticmethod
    def _get_filetype(path: str) -> str:
        SEP = "."
        if SEP in path:
            return path.split(".")[-1]
        else: return ""

    # def load_json(self, filename: str) -> dict:
    #     filepath = self._join(filename)
    #     with open(filepath, mode="r") as file:
    #         return json.load(file)
    @staticmethod
    def _load_json(path: str) -> dict:
        with open(path, mode="r") as file:
            return json.load(file)

    @staticmethod
    def _load_image(path: str) -> pg.Surface:
        with open(self.filepath, mode="r") as file:
            return  pg.image.load(file).convert_alpha()
if __name__ == "__main__":
    f = FileManager()
    f.load("f.json")
    print(f.get("f.json"))
