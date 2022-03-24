import math

from core.math.transformations import linear_transformations
from core.math import constants

# changing the angle changes the type of parallel projection
_ISO_RADIANS = tuple(constants.ANGLE_TO_RADS_CONVERSION * angle for angle in (150, 30, -90))


class IsometricProjection(linear_transformations.LinearTransformation):
    """Isometric projection of xyz on xy.
    https://en.wikipedia.org/wiki/Isometric_projection#Mathematics"""
    def __init__(self, unit_size: int):
        """@param int: effective scaling up/down of the projection"""
        (X_RADIANS, Y_RADIANS, Z_RADIANS) = _ISO_RADIANS
        # construct projection matrix: matrix * 3-tuple => 2-tuple
        std_matrix_repr = (
                           (math.cos(X_RADIANS)*unit_size, math.cos(Y_RADIANS)*unit_size, math.cos(Z_RADIANS)*unit_size),
                           (math.sin(X_RADIANS)*unit_size, math.sin(Y_RADIANS)*unit_size, math.sin(Z_RADIANS)*unit_size)
                           )
        super().__init__(std_matrix_repr)




