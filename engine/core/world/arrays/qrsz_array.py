from __future__ import annotations

from core.sprites.sprite import Sprite
from core.world.arrays.hash_array import HashArray
from core.math.points.qrsz import PointQRSZ, QVECTOR, RVECTOR, SVECTOR, ZVECTOR



class HashArrayQRSZ(HashArray):
    """Hash array for hexagonal tiles."""
    def __init__(self, qrz_dimensions: tuple):
        q, r, z = qrz_dimensions
        # s is a combination of q and r
        self.dimensions = PointQRSZ(q, r, 0, z)
        # this is solely for type hinting
        global KEYS_TYPE, VALS_TYPE, DICT_TYPE
        KEYS_TYPE = PointQRSZ
        VALS_TYPE = Sprite
        DICT_TYPE = dict[KEYS_TYPE: VALS_TYPE]
        super().__init__(self._get_indices(), KEYS_TYPE)

    def _get_indices(self) -> list[VALS_TYPE]:
        indices = []
        for z in self.z_range():
            for r in self.r_range():
                for q in self.q_range():
                    s = self._get_s(r, q)
                    index = PointQRSZ(q, r, s, z)
                    indices.append(index)
        return indices

    def get_from_vector(self, origin, vector, vector_range: int) -> list:
        """Get list of values that lie on a given vector from origin that terminates at end vector
        range."""
        indices = []
        for i in range(0, vector_range):
            index = origin.add(vector.mult(i))
            indices.append(index)
        return self.get_from_iter(indices)

    def q_range(self, reverse=False) -> range:
        q_dim = self.dimensions.q
        START, STOP, STEP = -q_dim, q_dim + 1, 1
        generator = reversed(range(START, STOP, STEP)) if reverse else range(START, STOP, STEP)
        return generator

    def r_range(self, reverse=False) -> range:
        r_dim = self.dimensions.r
        START, STOP, STEP = -r_dim, r_dim + 1, 1
        generator = reversed(range(START, STOP, STEP)) if reverse else range(START, STOP, STEP)
        return generator

    def s_range(self, reverse=False) -> range:
        r_dim, q_dim = self.dimensions.r + 1, self.dimensions.q + 1
        min_s = self._get_s(r_dim, q_dim)
        max_s = - min_s
        START, STOP, STEP = min_s, max_s + 1, 1
        generator = reversed(range(START, STOP, STEP)) if reverse else range(START, STOP, STEP)
        return generator

    def z_range(self, reverse=False) -> range:
        min_z = 0
        max_z = self.dimensions.z
        START, STOP = min_z, max_z
        STEP = 1
        # z is 0 or greater than 0 ie z is nonnegative
        generator = reversed(range(START, STOP, STEP)) if reverse else range(START, STOP, STEP)
        return generator

    @staticmethod
    def _get_s(r: int, q: int) -> int:
        return -q-r
'''
    def _tiles_from_vector(self, target_qrsz: points.PointQRSZ, VECTOR: points.PointQRSZ, radius: int) -> list[tiles.Tile]:
        """Get tiles along the given axis vector radius units away."""
        tiles = []
        for i in range(-radius, radius+1, 1):
            vector = VECTOR.mult(i)
            new_point = target_qrsz.add(vector)
            if new_point == target_qrsz:
                # ignore when target qrsz is gotten
                continue
            val = self.get(new_point, verbose=False)
            if val is not None:
                tiles.append(val)
        return tiles

    def get_q_tiles(self, target_qrsz: points.PointQRSZ, radius: int) -> list[tiles.Tile]:
        """Get tiles along the r axis radius units away."""
        return self._tiles_from_vector(target_qrsz, points.QVECTOR, radius)

    def get_r_tiles(self, target_qrsz: points.PointQRSZ, radius: int) -> list[tiles.Tile]:
        """Get tiles along the r axis radius units away."""
        return self._tiles_from_vector(target_qrsz, points.RVECTOR, radius)

    def get_s_tiles(self, target_qrsz: points.PointQRSZ, radius: int) -> list[tiles.Tile]:
        """Get tiles along the r axis radius units away."""
        return self._tiles_from_vector(target_qrsz, points.SVECTOR, radius)

    def get_z_tiles(self, target_qrsz: points.PointQRSZ, radius: int) -> list[tiles.Tile]:
        """Get tiles along the r axis radius units away."""
        return self._tiles_from_vector(target_qrsz, points.ZVECTOR, radius)

    def get_radial_tiles(self, target_qrsz: points.PointQRSZ, radius: int, plane_only=False) -> list[tiles.Tile]:
        tiles = []
        tiles.extend(self.get_r_tiles(target_qrsz, radius))
        tiles.extend(self.get_q_tiles(target_qrsz, radius))
        tiles.extend(self.get_s_tiles(target_qrsz, radius))
        if not plane_only:
            tiles.extend(self.get_z_tiles(target_qrsz, radius))
        return list(tiles)

    @staticmethod
    def _sort_indices(indices: list, axis: int, descending=False) -> list[points.PointQRSZ]:
        ALLOWEDINDICES = (0, 1, 2, 3)
        if not axis in ALLOWEDINDICES: raise ValueError(f"axis={axis} not in allowed_indices={ALLOWEDINDICES}")
        return sorted(indices, key=lambda point: point[axis], reverse=descending)

    def _bound_sprites_in_rect(self, rect: pg.Rect) -> list[points.PointQRSZ]:
        indices_in_rect = []
        for index, sprite in self._hashtable.items():
            if sprite != None and rect.collidepoint(sprite.projection):
                indices_in_rect.append(index)
        return indices_in_rect

    def painters_draw_order(self, bounding_rect: pg.Rect) -> list[tiles.Tile]:
        indices = self._bound_sprites_in_rect(bounding_rect)
        indices = self._sort_indices(indices, 2, descending=True)   # -s sort
        indices = self._sort_indices(indices, 0, descending=False)  # +r sort
        indices = self._sort_indices(indices, 1, descending=False)  # +q sort
        indices = self._sort_indices(indices, 3, descending=False)  # +z sort
        tiles = tuple(self.get(index, default=None) for index in indices)
        return filter(None, tiles) # remove None vals
    '''
