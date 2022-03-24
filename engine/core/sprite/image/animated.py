import math, os

import pygame as pg

from core.image import images
from core.utils import files



from core import abstract

class Animation(abstract.images.AbstractAnimatedImage):
    def __init__(self, _unit_size: float, *paths_to_dir: str) -> None:
        self._unit_size = _unit_size
        self.path = files.PathObject(*paths_to_dir)
        self.frames: tuple[images.Image] = self._load_frames()
        self._time: float = 0
        self._TOTALFRAMES: int = len(self.frames)

    def _load_frames(self) -> tuple:

        def is_png(file: str) -> bool:
            return ".png" in file

        image_dict: dict[int: images.Image] = {} 
        path = self.path.path
        for file_str in os.listdir(path):
            if is_png(file_str):
                start, end = file_str.split(".")
                image_dict[int(start)] = images.Image(file_str, True, path)
        sorted_keys = sorted(image_dict.keys())
        return tuple(image_dict.get(key) for key in sorted_keys)

    @property
    def _frame_number(self) -> int:
        return math.floor(self._time)

    @property
    def active_frame(self) -> images.Image:
        return self.frames[self._frame_number]
    
    def scale(self, factor: float) -> None:
        for frame in self.frames:
            frame.scale(factor)

    def update(self, dt: float):
        self._time += dt
        self._time = self._time % self._TOTALFRAMES # keep internal time as the smallest factor of total frames

    def draw(self, surface: pg.Surface, xy: tuple, alpha=255) -> pg.Rect:
        active_frame = self.active_frame
        active_frame.draw(surface, xy, alpha=alpha)
        # pg.draw.circle(surface, (255, 0, 0), xy, 5)
        # pg.draw.line(surface, (0, 0, 255), xy, REF)
        # pg.draw.line(surface, (0, 0, 255), xy, (dx, dy))
        # (dr, dangle) = tuple(a-b for a, b in zip(REF.as_polar(), vect.as_polar()))
        # top = REF * vect
        # denom = REF.magnitude() * vect.magnitude()
        # angle = math.acos(top/denom)
        #print(angle)

    def collidepoint(self, img_topleft: tuple, xy: tuple[float, float]) -> bool:
        return self.active_frame.collidepoint(img_topleft, xy)
