from __future__ import annotations

import pygame as pg

#from core.world.arrays.qrsz_array import HashArrayQRSZ
from core.math.points.qrsz import PointQRSZ
from core.sprites import sprite4

class Tile(sprite4.Sprite4):
    "inherit from sprite"
    def __init__(self, array, index: PointQRSZ, image: pg.Surface):
        self._array = array
        super().__init__(index, image)
        
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.formatted_qrsz}"

    @property
    def index(self) -> PointQRSZ:
        return self.qrsz
#    @property
#    def tiles_around_self(self) -> list[Tile]:
#        return self._array.get_radial_tiles(self.index, 1, plane_only=True)
    def draw(self, surface: pg.Surface) -> None:
        super().draw(surface)
        if self._verbose:
            from core.image import text
            text.render_text(surface, self.projection, str(self.index), centered=False)
