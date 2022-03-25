from core.world.arrays.hash_array import HashArray
from core.math.points.qrsz import PointQRSZ


class HashArrayXY(HashArray):
    def __init__(dictionary):
        super().__init__(dictionary, PointQRSZ)
