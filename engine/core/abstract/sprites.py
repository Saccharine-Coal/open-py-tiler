from abc import ABC, abstractmethod, abstractproperty

import pygame as pg

from core import abstract


class AbstractSprite(ABC):
    """Most basic game object."""

    @abstractmethod
    def draw(self, surface: pg.Surface) -> pg.Rect:
        pass


class AbstractActiveSprite(AbstractSprite):
    """Sprite that handles events."""

    @abstractmethod
    def update(self, dt: float) -> None:
        pass
    
    @abstractmethod
    def handle_events(self, event: pg.event.Event) -> None:
        """Process single events."""
        pass


class AbstractSprite2(AbstractSprite):

    # @abstractproperty
    # def xy(self) -> tuple[float, float]:
    #     """Projection point"""
    #     pass

    # @abstractproperty
    # def bounding_rect(self) -> pg.Rect:
    #     pass
    @abstractmethod
    def set_alpha(self, alpha: int) -> None:
        return

    @abstractmethod
    def collidepoint(self, xy: tuple[float, float]) -> bool:
        pass



class AbstractSprite4(AbstractSprite2):

    @abstractproperty
    def formatted_qrsz(self) -> str:
        pass

    @abstractmethod
    def project(self, projection_matrix, *linear_matrices) -> None:
        pass

    @abstractmethod
    def move(self, dq=0, dr=0, ds=0, dz=0) -> None:
        """Move sprite by given offset."""
        pass
