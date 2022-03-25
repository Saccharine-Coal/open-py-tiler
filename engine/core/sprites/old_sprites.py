from __future__ import annotations
import imp
from re import S

import pygame as pg

from core.abstract import sprites
from core.math import points, projections
from core.image import images, animated
from core import constants



class AnimatedSprite(Sprite4):
    def __init__(self, qrsz: tuple, unit_size: int) -> None:
        # TODO: images are currently hard coded
        import os
        path_to_dir = os.path.join("assets", "animations", "walk") 
        self.time = 0
        self.animations: list[animated.Animation] = []
        for i in range(1, 7, 1):
            folder = f"a{i}"
            animation = animated.Animation(os.path.join(path_to_dir, folder), unit_size)
            self.animations.append(animation)
        image = self.animations[0].active_frame.true_surface
        super().__init__(qrsz, image, unit_size)
        self.angle = 0

    def scale(self, factor: float):
        for animation in self.animations:
            animation.scale(factor)

    def update(self, dt: float) -> None:
        SPEED = 20
        dt = dt * SPEED
        self.time += dt
        if self.moving: 
            for animation in self.animations:
                animation.update(dt)
            self.moving = False


    def collidepoint(self, xy: tuple) -> bool:
        return False
        return self.animation.collidepoint(self.projection, xy)

    def draw(self, surface: pg.Surface) -> None:
        i = round(self.angle / 60)
        active = self.animations[i]
        # print("i=", active._frame_number)
        active.draw(surface, self.projection, 255)
