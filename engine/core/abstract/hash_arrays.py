from abc import ABC, abstractmethod, abstractstaticmethod

from core.abstract import tiles
from core.math import points


class AbstractAxialHashArray(ABC):
    @abstractmethod
    def __repr__(self) -> str:
        name = self.__class__.__name__
        return name + f"(q, r, s, z)={(len(self.q_range()), len(self.r_range()), len(self.s_range()), len(self.z_range()))}"

    @abstractmethod
    def _get_indices(self) -> tuple[tuple]:
        pass

    @abstractmethod
    def populate(self, tile_cls: tiles.AbstractTile) -> None:
        pass
        
    @abstractmethod
    def q_range(self, reverse=False) -> range:
        pass     

    @abstractmethod
    def r_range(self, reverse=False) -> range:
        pass  

    @abstractmethod
    def s_range(self, reverse=False) -> range:
        pass  

    @abstractmethod
    def z_range(self, reverse=False) -> range:
        pass 

    @abstractstaticmethod
    def _get_s(r: int, q: int) -> int:
        pass

    @abstractmethod 
    def _tiles_from_vector(self, target_qrsz: points.PointQRSZ, VECTOR: points.PointQRSZ, radius: int) -> list[tiles.AbstractTile]:
        pass 

    @abstractmethod
    def get_q_tiles(self, target_qrsz: points.PointQRSZ, radius: int) -> list[tiles.AbstractTile]:
        pass

    @abstractmethod
    def get_r_tiles(self, target_qrsz: points.PointQRSZ, radius: int) -> list[tiles.AbstractTile]:
        pass

    @abstractmethod
    def get_s_tiles(self, target_qrsz: points.PointQRSZ, radius: int) -> list[tiles.AbstractTile]:
        pass

    @abstractmethod
    def get_z_tiles(self, target_qrsz: points.PointQRSZ, radius: int) -> list[tiles.AbstractTile]:
        pass

    @abstractmethod
    def get_radial_tiles(self, target_qrsz: points.PointQRSZ, radius: int, plane_only=False) -> list[tiles.AbstractTile]:
        pass