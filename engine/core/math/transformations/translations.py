import numpy as np

from core.math.transformations import linear_transformations



class TranslationMatrix3(linear_transformations.LinearTransformation):
    """Translation by a factor (dx, dy, dz) in Euclidean 3-space."""
    def __init__(self, trans_xyz: tuple):
        """@param 3-tuple of integers to translate by."""
        self.xyz_trans = trans_xyz
        trans_x, trans_y, trans_z = trans_xyz
        std_matrix_repr = [
                           [1, 0, 0, trans_x],
                           [0, 1, 0, trans_y],
                           [0, 0, 1, trans_z],
                           [0, 0, 0, 1]
                           ]
        super().__init__(std_matrix_repr)

    # DUNDER OVERIDE
    def __neg__(self):
        negative_translation = tuple(-element for element in self.trans_xyz)
        return TranslationMatrix3(negative_translation)

    # METHOD OVERIDE
    def transform(self, xyz: tuple) -> np.ndarray:
        # 3-tuple -> 4-tuple -> 3-tuple
        xyzw = np.append(xyz, 1)
        product_arr = np.dot(self.std_matrix_repr, xyzw)
        return tuple(product_arr)[0: 3]

    def translate(self, dx:int=0, dy:int=0, dz:int=0):
        x, y, z = self.xyz_trans[:]
        x += dx
        y += dy
        z += dz
        self.xyz_trans = (x, y, z)
        self.std_matrix_repr = [
                           [1, 0, 0, x],
                           [0, 1, 0, y],
                           [0, 0, 1, z],
                           [0, 0, 0, 1]
        ]

