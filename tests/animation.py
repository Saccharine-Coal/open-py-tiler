from dataclasses import dataclass, field
import os, math

import pygame as pg


import image


@dataclass
class Animation:
    path_to_dir: str
    scale: float = field(default=1)
    frames: tuple[image.Image] = field(init=False, repr=True)
    time: float = field(init=False)

    def __post_init__(self):
        self.frames = self._load_frames()
        self.time = 0

    def _load_frames(self) -> tuple:

        def is_bmp(file: str) -> bool:
            return ".bmp" in file

        def is_png(file: str) -> bool:
            return ".png" in file

        def scale(surface: pg.Surface, scale_ratio: float) -> pg.Surface:
            return

        surfaces = []
        images = []
        if os.path.isdir(self.path_to_dir):
            for file_str in os.listdir(self.path_to_dir):
                file_str = os.path.join(self.path_to_dir, file_str)
                if os.path.isfile(file_str) and is_png(file_str):
                    with open(file_str, mode="r") as file:
                        print("loading", file_str)
                        surface = pg.image.load(file, ".png").convert_alpha()
                        surfaces.append(surface)
        for surface in surfaces:
            rect = surface.get_rect()
            frame_img = image.Image(surface, rect, centered=False)
            images.append(frame_img)
        return tuple(images)

    @property
    def _frame_number(self) -> int:
        TOTAL_FRAME_NUMBER = len(self.frames)
        return math.floor(self.time) % TOTAL_FRAME_NUMBER 

    def update(self, dt: float):
        self.time += dt

    def draw(self, surface: pg.Surface):
        active_frame = self.frames[self._frame_number]
        xy = (0, 0)
        active_frame.draw(surface, xy)
