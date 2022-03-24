from __future__ import annotations
from collections import namedtuple
from typing import Union

from core.math.points import point_functions

class PointXYZ(namedtuple("Point3", "x y z")):

    def add(self, other: Union[tuple, PointXYZ]) -> PointXYZ:
        if point_functions.operation_conditions_met(self, other):
            return PointXYZ(*point_functions.add(self, other))

    def mult(self, factor: Union[float, int]) -> PointXYZ:
        return PointXYZ(*point_functions.mult(self, factor))
