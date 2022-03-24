import logging

import pygame as pg

from devices import device


class Mouse(device.Device):
    def __init__(self, disabled=False) -> None:
        mutable = False
        event_keys = [1, 2, 3, 4, 5]
        super().__init__(event_keys, mutable, disabled=disabled)
        self.wheel_states = (False, False)

    @property
    def wheel_in(self) -> bool:
        return self.wheel_states[0]

    @property
    def wheel_out(self) -> bool:
        return self.wheel_states[1]

    def _name(self, key: int) -> str:
        MOUSE_CONSTANTS = {1: "mouse_left", 2: "mouse_middle", 3: "mouse_right", 4: "mouse_wheel_down", 5: "mouse_wheel_up"}
        return MOUSE_CONSTANTS.get(key, "None")

    def handle_events(self, event: pg.event.Event) -> None:
        if self.disabled: return # device is not active
        # mouse types = [pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP, pg.MOUSEMOTION, pg.MOUSEWHEEL]
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button in self._key_to_button.keys():
                if event.button != 4 and event.button != 5:
                    self._new_key(event.button)
                    self.press_key(event.button)
        
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button in self._key_to_button.keys():
                if event.button != 4 and event.button != 5:
                    self.release_key(event.button) 
        elif event.type == pg.MOUSEWHEEL:
            if event.y == 1:
                self.wheel_states = (True, False)
            if event.y == -1:
                self.wheel_states = (False, True)