from abc import ABC, abstractmethod, abstractproperty

import pygame as pg

from core import abstract


class AbstractSprite(ABC):
    """Most basic sprite object. Is an abstract sprite to force consistent sprite instantiation for any class that subclass this base class."""

    @abstractmethod
    def update(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def collidepoint(self, xy: tuple[float, float]) -> bool:
        pass
