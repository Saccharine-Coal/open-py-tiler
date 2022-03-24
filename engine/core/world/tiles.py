from __future__ import annotations

import pygame as pg

from core.abstract import hash_arrays
from core.math import points
from elements import sprites


class Tile(sprites.Sprite4):
    "inherit from sprite"
    def __init__(self, array: hash_arrays.AbstractAxialHashArray, index: points.PointQRSZ, image: pg.Surface) -> None:
        self._array = array
        super().__init__(index, image)
        
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.formatted_qrsz}"

    @property
    def index(self) -> points.PointQRSZ:
        return self.qrsz

    @property
    def tiles_around_self(self) -> list[Tile]:
        return self._array.get_radial_tiles(self.index, 1, plane_only=True)

    def draw(self, surface: pg.Surface) -> None:
        super().draw(surface)
        if self._verbose:
            from core.image import text
            text.render_text(surface, self.projection, str(self.index), centered=False)
