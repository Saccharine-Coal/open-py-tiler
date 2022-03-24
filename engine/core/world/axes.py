import pygame as pg

from core.math import points, functions


class Axes:
    def __init__(self, unit_size: int) -> None:
        self.r_vector = points.RVECTOR.mult(unit_size)
        self.q_vector = points.QVECTOR.mult(unit_size)
        self.s_vector = points.SVECTOR.mult(unit_size)
        self.z_vector = points.ZVECTOR.mult(unit_size)
        OFFSET = points.PointQRSZ(0, 0, 0, .5)  # z is mapped directly to screen y
        self.origin = points.PointQRSZ(0, 0, 0, 0)
        (self.origin, self.r_vector, self.q_vector, self.s_vector, self.z_vector) = tuple(
            functions.add_qrsz(point, OFFSET) for point in (self.origin, self.r_vector, self.q_vector, self.s_vector, self.z_vector)
        )
        self.vectors = {key: val for key, val in zip(("origin", "+r", "+q", "+s", "+z"), (self.origin, self.r_vector, self.q_vector, self.s_vector, self.z_vector))}

    def project(self, a, *b):
        for vector in self.vectors.values():
            vector.project(a, *b)


    def draw(self, surface: pg.Surface):
        COLORS = ((0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255))
        origin = self.origin
        i = 0
        for key, vector in self.vectors.items():
            tail = origin.projection
            tip = vector.projection
            pg.draw.line(surface, COLORS[i], tail, tip, 2)
            i += 1

