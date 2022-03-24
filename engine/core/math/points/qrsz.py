from __future__ import annotations
from collections import namedtuple
from typing import Union

from core.math import constants
from core.math.points import point_functions, xy, xyz


class PointQRSZ(namedtuple("Point4", "q r s z")):

    def project(self, projection_matrix, *linear_transformations) -> xy.PointXY:
        xyz = self.xyz
        """Applies transformation matrices to given an xyz. R^3 => R^3 """
        for linear_transformation in linear_transformations:
            xyz = linear_transformation.transform(xyz)
        """Multiply a projection matrix to an xyz. R^3 => R^2"""
        xy = projection_matrix.transform(xyz)
        self.projection = PointXY(*xy)
        return xy.PointXY(*xy)

    @property
    def xyz(self) -> xyz.PointXYZ:
        """(q, r, s, z) -> (x, y, z)"""
        # dirty "matrix"
        ROOT_3 = constants.ROOT_3
        (q, r, s, z) = self
        #r = -(q + s)
        x = ROOT_3 * q + (ROOT_3/2) * r
        y =                     1.5 * r
        return xyz.PointXYZ(x, y, z)

    def _round(self, val) -> Union[float, int]:
        # is int
        if isinstance(val, int): return val
        # is float
        EPSILON = 1 * pow(10, -9)
        rounded = round(val)
        rounding_needed = False if (abs(val - rounded) > EPSILON) else True
        if rounding_needed: return rounded
        else: return val

    def add(self, other: Union[tuple, PointQRSZ]) -> PointQRSZ:
        if point_functions.operation_conditions_met(self, other):
            return PointQRSZ(*points.add(self, other))
        """Not sure why I am rounding below"""
        #if isinstance(other, tuple) and len(other) == len(self):
            #tup = tuple(a + b for a, b in zip(self, other))
            #tup = tuple(self._round(val) for val in tup)
            #return PointQRSZ(*tup)
        #else: raise ValueError

    def mult(self, factor: Union[float, int]) -> PointQRSZ:
        return PointQRSZ(*point_functions.mult(self, factor))

# (q, r, s, z)
QVECTOR = PointQRSZ(+1, -1, 0, 0)
RVECTOR = PointQRSZ(0, +1, -1, 0)
SVECTOR = PointQRSZ(-1, 0, +1, 0)
ZVECTOR = PointQRSZ(0, 0, 0, +1)

