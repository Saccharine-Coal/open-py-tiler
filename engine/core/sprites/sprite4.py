import pygame as pg

from core.math import points

from core.sprites import images, sprite2


class Sprite4(sprite2.Sprite2):
    def __init__(self, qrsz: points.qrsz.PointQRSZ, surface: pg.Surface) -> None:
        self.qrsz = points.qrsz.PointQRSZ(*qrsz)
        super().__init__((0, 0), surface)

    @property
    def formatted_qrsz(self) -> str:
        (q, r,  s, z) = self.qrsz
        return f"(q={q}, r={r}, s={s}, z={z})"

    def project(self, projection_matrix, *linear_transformations) -> None:
        self.projection: points.xy.PointXY = self.qrsz.project(projection_matrix, *linear_transformations)

'''def move(self, dq=0, dr=0, ds=0, dz=0, scale=1) -> None:
        DIRECTIONS: dict[points.PointQRSZ: int] = {
            points.qrsz.QVECTOR: 0,
            points.qrsz.QVECTOR.mult(-1): 180,
            points.qrsz.RVECTOR: 120,
            points.qrsz.RVECTOR.mult(-1): 300,
            points.qrsz.SVECTOR: 240,
            points.qrsz.SVECTOR.mult(-1): 60,
            points.qrsz.ZVECTOR: 0,
            points.qrsz.ZVECTOR.mult(-1): 0
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
        #     # if dr ==2: self.time += dr * RANGLE - 90'''
