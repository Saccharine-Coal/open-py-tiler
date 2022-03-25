import pygame as pg

from core.math import points

from core.sprites import sprite
from core.sprites.images import image


class Sprite2(image.Image, sprite.Sprite):
    """Sprite for xy coordinates. This essentially represents every sprite."""
    def __init__(self,  xy: tuple, surface: pg.Surface) -> None:
        self.projection = points.xy.PointXY(*xy)
        CENTERED = True
        super().__init__(surface, CENTERED)
        self._verbose = False
        self.moving = False
        self.alpha = 255

    def update(self, dt : float) -> None:
        raise NotImplementedError

    def set_alpha(self, alpha: int) -> None:
        self.alpha = alpha

    def draw(self, surface: pg.Surface) -> None:
        return super().draw(surface, self.projection, alpha=255)

    def collidepoint(self, xy: tuple) -> bool:
        return super().collidepoint(self.projection, xy)

    def draw(self, surface: pg.Surface) -> None:
        return super().draw(surface, self.projection, self.alpha)
