raise NotImplementedError
import math

from PygameObjects.math.linear_transformations import LinearTransformation



class XRotationMatrix(LinearTransformation):
    """Rotation around the X axis about (0, 0, 0)."""
    def __init__(self, degrees=0):
        """@param degrees to rotate"""
        rad = (degrees / 180) * math.pi
        std_matrix_repr = [
                           [1, 0, 0],
                           [0, math.cos(rad), -math.sin(rad)],
                           [0, math.sin(rad), math.cos(rad)]
                           ]
        super().__init__(std_matrix_repr)


class YRotationMatrix(LinearTransformation):
    """Rotation around the Y axis about (0, 0, 0)."""
    def __init__(self, degrees=0):
        """@param degrees to rotate"""
        rad = (degrees / 180) * math.pi
        std_matrix_repr = [
                           [math.cos(rad), 0, math.sin(rad)],
                           [0, 1, 0],
                           [-math.sin(rad), 0, math.cos(rad)]
                           ]
        super().__init__(std_matrix_repr)


class ZRotationMatrix(LinearTransformation):
    """Rotation around the Z axis about (0, 0, 0)."""
    def __init__(self, degrees=0):
        """@param degrees to rotate"""
        rad = (degrees / 180) * math.pi
        std_matrix_repr = [
                           [math.cos(rad), -math.sin(rad), 0],
                           [math.sin(rad), math.cos(rad), 0],
                           [0, 0, 1]
                           ]
        super().__init__(std_matrix_repr)


class SphericalRotation(LinearTransformation):
    def __init__(self, theta, phi) -> None:
        cos = math.cos
        sin = math.sin
        theta = (theta / 180) * math.pi
        phi = (phi / 180) * math.pi
        # https://math.stackexchange.com/q/162177
        # sphere to cart
        std_matrix_repr = [
                           [sin(theta)*cos(phi), cos(theta)*cos(phi), -sin(theta)*sin(phi)],
                           [sin(theta)*sin(phi), cos(theta)*sin(phi), sin(theta)*cos(phi)],
                           [cos(theta), -sin(theta), 0]
                           ]
        # cart to sphere
        # std_matrix_repr = [
        #                    [sin(theta)*cos(phi), sin(theta)*sin(phi), cos(theta)],
        #                    [cos(theta)*cos(phi), cos(theta)*sin(phi), -sin(theta)],
        #                    [-sin(phi), cos(phi), 0]
        #                    ]
        super().__init__(std_matrix_repr)