from __future__ import annotations
import logging

import pygame as pg

import points


class Device:
    __slots__ = ("_key_to_button", "_mutable", "disabled", "__dict__")
    def __init__(self, event_keys: list[int], mutable: bool=True, disabled=False) -> None:
        self._key_to_button: dict[int: PygameButton]  = {key: PygameButton() for key in event_keys}
        self._mutable = mutable
        self.disabled = disabled
        
    def handle_events(self, event: pg.event.Event) -> None:
        raise NotImplementedError

    def get(self, key: int, modifier=None) -> PygameButton:
        # if modifier:
        #     mods = pg.key.get_mods()
        #     return self._key_to_button[key] and (mods & modifier) # bitwise operation
        if self._check_type(key):
            return self._key_to_button.get(key, None)

    @staticmethod
    def _check_type(key) -> bool:
        """To force all keys for devices to be integers."""
        if isinstance(key, int): return True
        else: raise TypeError(f"current_type={type(key)}")
    # def set(self, key: int) -> None:
    #     if self._mutable:
    #         self._key_to_button.setdefault(key, False)

    def press_key(self, key: int) -> None:
        button = self._key_to_button.get(key, None)
        button.down = True
        button.up = False
        logging.debug(f"key={self._name(key)} pressed down.") 

    def release_key(self, key: int) -> None:
        button = self._key_to_button.get(key, None)
        button.down = False
        button.up = True
        logging.debug(f"key={self._name(key)} released.") 
    # def reset(self) -> None:
    #     """Reset all values for event keys. Call after events are processed."""
    #     for key, value in self._key_to_button.items():
    #         value.

    def _new_key(self, event_key: int) -> None:
        """Set a new key for a pygame event."""
        if self._check_type(event_key):
            if event_key not in self._key_to_button.keys():
                if self._mutable:
                    self._key_to_button[event_key] = PygameButton()    
                else: 
                    logging.warn(f"{self.__class__.__name__}() new key={event_key} is being set with None")
        return None

    def _name(self, key: int) -> str:
        raise NotImplementedError


class PygameButton:
    def __init__(self) -> None:
        self.up = True
        self.down = self.held = False
        self.initial = self.final = points.PointXY(0, 0)

    @property
    def up(self) -> bool:
        return self._up

    @up.setter
    def up(self, val: bool) -> None:
        self._up = val
        if val:
            self.final = points.PointXY(*pg.mouse.get_pos())

    @property
    def down(self) -> bool:
        return self._down

    @down.setter
    def down(self, val: bool) -> None:
        self._down = val
        if val:
            self.initial = points.PointXY(*pg.mouse.get_pos())

    def __repr__(self) -> str:
        name = self.__class__.__name__
        return name + f"(up={self.up}, down={self.down}, held={self.held})"

# class MouseButton(PygameButton):
#     def __init__(self) -> None:
#         super().__init__()