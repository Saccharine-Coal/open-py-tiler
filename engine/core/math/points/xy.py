from __future__ import annotations
from collections import namedtuple
from typing import Union

from core.math.points import point_functions

class PointXY(namedtuple("Point2", "x y")):

    @property
    def active(self) -> bool:
        # (x, y)
        elements = (self.x, self.y)
        for element in elements:
            # any None elements means the point is partially empty and thus not active
            if element is None:
                return False
        return True

    def add(self, other: Union[tuple, PointXY]) -> PointXY:
        if point_functions.operation_conditions_met(self, other):
            return PointXY(*point_functions.add(self, other))

    def mult(self, factor: Union[float, int]) -> PointXY:
        return PointXY(*point_functions.mult(self, factor))
