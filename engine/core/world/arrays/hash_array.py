"""Base hash array"""
from __future__ import annotations

import pygame as pg

from core.sprites.sprite import Sprite
from core.world import tiles


class HashArray:
    """Most basic hash array."""
    def __init__(self, indices: list, key_type):
        # this is solely for type hinting
        global KEYS_TYPE, VALS_TYPE, DICT_TYPE
        KEYS_TYPE = key_type
        VALS_TYPE = Sprite
        DICT_TYPE = dict[KEYS_TYPE: VALS_TYPE]

        self._dict: DICT_TYPE = {index: None for index in indices}

    @property
    def _keys(self) -> list[KEYS_TYPE]:
        return self._dict.keys()

    @property
    def _vals(self) -> list[VALS_TYPE]:
        return self._dict.values()

    def __repr__(self) -> str:
        name = self.__class__.__name__
        return name + "(" + f"len(keys)={len(self._keys)}, len(vals)={len(self._vals)}" + ")"

    def get(self, index: KEYS_TYPE, default=None, verbose: bool=False) -> VALS_TYPE:
        """Get an item from the hash array with given index."""
        if verbose:
            print(f"getting {index}. Got {self._dict.get(index)}")
        return self._dict.get(index, default)

    def get_from_iter(self, indices: list[KEYS_TYPE], default=None, verbose: bool=False) -> list[VALS_TYPE]:
        """Gets items from hash array from a iterable of valid indices."""
        items = []
        for index in indices:
            item = self.get(index, default=default, verbose=verbose)
            if item is not None:
                items.append(item)
        return items

    def get_all(self) -> list[VALS_TYPE]:
        """Get all the values in the array."""
        return self._vals

    def set(self, index: KEYS_TYPE, new_item: VALS_TYPE) -> None:
        """This is meant to replace a value for an existing key."""
        if index in self._keys:
            self._dict.update({index: new_item})
        else:
            print(list(self._keys))
            raise KeyError(f"No key exists for {index}!")

    def new(self, new_index: KEYS_TYPE, new_item: VALS_TYPE) -> None:
        """Create new key value pair."""
        if new_index in list(self._keys):
            self.set(new_index, new_item)
        else:
            # update dimensions
            self._dict.update({new_index: new_item})

    def populate(self, tile_cls: tiles.Tile, surface: pg.Surface) -> None:
        for index in self._keys:
            self._dict[index] = tile_cls(self, index, surface)
