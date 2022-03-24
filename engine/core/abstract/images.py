from dataclasses import dataclass
from abc import abstractmethod, abstractproperty

import pygame as pg


from core.abstract import sprites


class AbstractImage(sprites.AbstractSprite):
    
    @abstractproperty
    def factor(self) -> float:
        pass

    @abstractproperty
    def _active_surface(self) -> pg.Surface:
        """Wrapper function to reduce transform calls."""
        pass

    @abstractproperty
    def mask(self) -> pg.mask.Mask:
        pass

    @abstractproperty
    def _tint(self) -> pg.Surface:
        """Really expensive image "tinting"."""
        pass

    @abstractmethod
    def collidepoint(self, img_topleft: tuple, xy: tuple) -> bool:
        pass

    @abstractmethod
    def scale(self, factor: float):
        pass

    @abstractmethod
    def center(self, xy: tuple) -> tuple[int, int]:
        pass

    @abstractmethod
    def set_tint(self, color: pg.Color) -> None:
        pass

    @abstractmethod
    def draw(self, surface: pg.Surface, xy: tuple, alpha=255) -> None:
        pass


@dataclass
class AbstractAnimatedImage(AbstractImage):
    @abstractmethod
    def _load_frames(self) -> tuple:
        pass

    @abstractproperty
    def _frame_number(self) -> int:
        pass
