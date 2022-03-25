import pygame as pg

from core.abstract.ABsprite import AbstractSprite


class Sprite(pg.sprite.Sprite, AbstractSprite):
    """Most basic sprite object. Subclasses pygame sprites, for group methods, and an abstract sprite to force consistent sprite instantiation."""
    def __init__(self, xy: tuple, image: pg.surface):
        self.xy = xy
        self.image = image
        self.rect = image.get_rect()

    def update(self, dt: float) -> None:
        return

    def collidepoint(self, xy: tuple[float, float]) -> bool:
        return self.rect.collidepoint(xy)
