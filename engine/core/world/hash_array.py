from __future__ import annotations # annotations are strings

import pygame as pg

from core.math.points import qrsz, xyz, xy


class AxialHashArray:
    __slots__ = ("dimensions", "_hashtable", "_indices", "_unit")
    def __init__(self, q_dim: int, r_dim: int, z_dim: int, unit_size: float) -> None:
        self.dimensions: points.PointQRSZ = points.PointQRSZ(q_dim, r_dim, self._get_s(r_dim, q_dim), z_dim)
        self._indices: tuple[points.PointQRSZ] = self._get_indices()
        self._hashtable: dict[points.PointQRSZ: tiles.Tile] = {}
        self._unit_size = unit_size

    def __repr__(self) -> str:
        name = self.__class__.__name__
        return name + f"(q, r, s, z)={(len(self.q_range()), len(self.r_range()), len(self.s_range()), len(self.z_range()))}"

    def _get_indices(self) -> tuple:
        indices = []
        for z in self.z_range():
            for r in self.r_range():
                for q in self.q_range():
                    s = self._get_s(r, q)
                    index = points.PointQRSZ(q, r, s, z)
                    indices.append(index)

        print(f"size={self.r_range()}, vals={list(i for i in self.r_range())}")
        return tuple(indices)

    def populate(self, tile_cls: tiles.Tile, image) -> None:
        table = {}
        for index in self._indices:
            table[index] = tile_cls(self, index, image)
        self._hashtable = table

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

    # r + q + s = 0
    # r = -q -s = -(q+s)
    # q = -r -s = -(r+s)
    # s = -r -q = -(r+q)
    # @staticmethod
    # def r(q: int, s: int) -> int:
    #     return -(q + s)
    # @staticmethod
    # def q(r: int, s: int) -> int:
    #     return -(r + s)
    # @staticmethod
    # def s(r: int, q: int) -> int:
    #     return -(r + q)

    # # @staticmethod
    # # def get_r_indices(r_dimension: int) -> tuple:
    # #     for 
    
    # def _get_indices(self, length_dimension: int, width_dimension: int, height_dimension: int) -> tuple:
    #     indices = []
    #     for z in self.z_range():
    #         for r in self.r_range():
    #             for q in self.q_range():
    #                 s = self.s(r, q)
    #                 index = (q, r, s, z)
    #                 indices.append(index)
    #     return tuple(indices)

    # def get_painters_plane(self, z: int) -> list:
    #     # last items in the list are values with the greatest q values
    #     # largest q val last, smallest r val last, largest z value last
    #     items_in_plane = []
    #     for r in self.r_dim(reverse=False):   
    #         for q in self.q_range():   
    #             s = self.s(q, r)
    #             index = (q, r, s, z)
    #             item = self.get(index, default=None)
    #             if item is not None:
    #                 items_in_plane.append(item)
    #     return items_in_plane

    # def painters_draw_order(self):
    #     planes = []
    #     for z in self.z_range():
    #         planes.append(self.get_painters_plane(z))
    #     return planes

    # def sorted(self, axis: str, reverse=False) -> tuple:
    #     DICT = {"q": 0, "r": 1, "s": 2, "z": 3}
    #     if not axis in DICT.keys(): raise KeyError(f"axis={axis} not in AXES={DICT.keys()}!")
    #     keys = self._hashtable.keys()
    #     return tuple(sorted(keys, key=lambda tup: tup[DICT.get(axis)], reverse=reverse))

    # def get_topmost_first(self) -> list:
    #     planes = []
    #     for z in self.z_dim(reverse=True):
    #         items_in_plane = []
    #         for q in self.q_dim(reverse=True):
    #             for r in self.r_dim(reverse=True):
    #                 s = self.s(q, r)
    #                 index = (q, r, s, z)
    #                 item = self.get(index, default=None)
    #                 if item is not None:
    #                     items_in_plane.append(item)
    #         planes.append(items_in_plane)
    #     return planes

    def get(self, index: tuple, default=None, verbose: bool=False):
        """Get an item from the hash array with given index."""
        if verbose:
            print(f"getting {index}. Got {self._hashtable.get(index)}")
        return self._hashtable.get(index, default)

    def get_from_iter(self, indices: list[tuple], default=None, verbose: bool=False) -> list:
        """Gets items from hash array from a iterable of valid indices."""
        items = []
        for index in indices:
            item = self.get(index, default=default, verbose=verbose)
            if item is not None:
                items.append(item)
        return items

    def set(self, index: tuple, new_item) -> None:
        """This is meant to replace a value for an existing key."""
        if index in list(self._hashtable.keys()):
            self._hashtable.update({index: new_item})
        else:
            print(list(self._hashtable.keys()))
            raise KeyError(f"No key exists for {index}!")

    def new(self, new_index, new_item) -> None:
        """Create new key value pair."""
        if new_index in list(self._hashtable.keys()):
            self.set(new_index, new_item)
        else:
            # update dimensions
            self._hashtable.update({new_index: new_item})
