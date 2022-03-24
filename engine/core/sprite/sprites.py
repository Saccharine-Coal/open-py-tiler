from __future__ import annotations
import imp
from re import S

import pygame as pg

from core.abstract import sprites
from core.math import points, projections
from core.image import images, animated
from core import constants


class Sprite2(images.Image, sprites.AbstractSprite2):
    def __init__(self, xy: tuple, image: pg.Surface) -> None:
        self.projection = points.PointXY(*xy)
        super().__init__(image, constants.CENTERED)
        self._verbose = False
        self.moving = False
        self.alpha = 255

    def update(self, dt: float) -> None:
        return

    def set_alpha(self, alpha: int) -> None:
        self.alpha = alpha

    def draw(self, surface: pg.Surface) -> None:
        return super().draw(surface, self.projection, alpha=255)

    def collidepoint(self, xy: tuple) -> bool:
        return super().collidepoint(self.projection, xy)

    def draw(self, surface: pg.Surface) -> None:
        return super().draw(surface, self.projection, self.alpha)



class Sprite4(Sprite2, sprites.AbstractSprite4):
    def __init__(self, qrsz: tuple, image: pg.Surface) -> None:
        self.qrsz = points.PointQRSZ(*qrsz)
        super().__init__((0, 0), image)
        

    @property
    def formatted_qrsz(self) -> str:
        (q, r, s, z) = self.qrsz
        return f"(q={q}, r={r}, s={s}, z={z})"

    def project(self, projection_matrix, *linear_transformations) -> None:
        self.projection: points.PointXY = self.qrsz.project(projection_matrix, *linear_transformations)

    def move(self, dq=0, dr=0, ds=0, dz=0, scale=1) -> None:
        DIRECTIONS: dict[points.PointQRSZ: int] = {
            points.QVECTOR: 0,
            points.QVECTOR.mult(-1): 180,
            points.RVECTOR: 120,
            points.RVECTOR.mult(-1): 300,
            points.SVECTOR: 240,
            points.SVECTOR.mult(-1): 60,
            points.ZVECTOR: 0,
            points.ZVECTOR.mult(-1): 0
        }
        if dq or dr or ds:
            self.angle = DIRECTIONS.get(points.PointQRSZ(dq, dr, ds, dz), 0)
            self.qrsz = self.qrsz.add(points.PointQRSZ(dq, dr, ds, dz).mult(scale))
            self.moving = True
        # if dq or ds or dr:
            
        #     REFFERENCE = pg.math.Vector2(1, 0)
        #     (x, y) = REFFERENCE
        #     (dx, dy, dz) = points.PointQRSZ(dq, dr, ds, dz).xyz
        #     vect = pg.math.Vector2(dx, dy)
        #     angle = REFFERENCE.angle_to(vect)
        #     top = REFFERENCE.dot(vect)
        #     denom = abs(REFFERENCE.magnitude()) * abs(vect.magnitude())
        #     import math
        #     print(math.acos(top/denom) * 180/math.pi, angle)
        #     if angle < 0:
        #         angle += 360
        #     angle += 60
        #     # print(math.acos(top/denom) * 180/math.pi)
        #     # else:
        #     #     angle += 45
        #     self.time = math.acos(top/denom) * 180/math.pi
        #     # print(self.qrsz, self.time)
            
        return

        if dq or dr or ds:
            (x, y, z) = self.qrsz.xyz
            REFFERENCE = pg.math.Vector2(x+1, y)
            new_qrsz = self.qrsz.add((dq, dr, ds, dz))
            (dx, dy, dz) = new_qrsz.xyz
            vect = pg.math.Vector2(x-dx, y-dy)
            angle = REFFERENCE.angle_to(vect)
            if angle <= 0:
                angle += 360
            angle = round(angle)

            print(angle)
            self.time = angle
            self.qrsz = new_qrsz
        

        # self.moving = True
        # self.qrsz = self.qrsz.add((dq, dr, ds, dz))
        # # print(f"xyz={self.qrsz.xyz}")
        # QANGLE = 0
        # RANGLE = 120
        # SANGLE = 240
        # FOO = (dq, dr, ds)
        # if dr and ds and not dq:
        #     # print(f"(dr, ds)={(dr, ds)}")
        #     if dr > 0: self.time = 135
        #     else: self.time = 270
        # elif dq or dr or ds:
        #     self.time = 0
        #     self.time += norm(dq, QANGLE)
        #     self.time += norm(dr, RANGLE)
        #     self.time += norm(ds, SANGLE)
        #     #self.time = dq * QANGLE + dr * RANGLE + ds * SANGLE
        #     # print(f"angle={self.time}, (dq, dr, ds) = {FOO}")
        #     # if dr == 1:
        #     #     self.time += dr * RANGLE + 90
        #     # if dr ==2: self.time += dr * RANGLE - 90

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
