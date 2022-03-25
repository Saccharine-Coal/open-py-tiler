import os

import pygame as pg
ASSETDIR = 'assets'

def load_png(target_dir: str, filename: str) -> pg.Surface:
    path_to_file = os.path.join(ASSETDIR, target_dir, filename)
    if ".png" in path_to_file and os.path.isfile(path_to_file):
        with open(path_to_file, mode="r") as file:
            return pg.image.load(file, ".png")
    raise ValueError(f"path={path_to_file} DNE")