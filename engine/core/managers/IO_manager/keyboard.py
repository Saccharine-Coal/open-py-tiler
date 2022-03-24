import logging

import pygame as pg
import pygame_gui

from devices import device


COMMON_TYPES = [pg.KEYDOWN, pg.KEYUP]
COMMON_KEYS = (pg.K_BACKSPACE, pg.K_SPACE, pg.K_LCTRL, pg.K_LSHIFT, pg.K_TAB,
    pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT)


class Keyboard(device.Device):
    def __init__(self, mutable: bool = True, disabled=False) -> None:
        event_keys = COMMON_KEYS
        super().__init__(event_keys, mutable, disabled=disabled)
    
    def _name(self, key: int) -> str:
        return pg.key.name(key)

    def handle_events(self, event: pg.event.Event) -> None:
        if self.disabled: return # device is not active

        if event.type == pg.KEYDOWN:
            self._new_key(event.key)
            if event.key in self._key_to_button.keys():
                self.press_key(event.key)
                logging.debug(f"key={self._name(event.key)} pressed down.")
        elif event.type == pg.KEYUP:
            if event.key in self._key_to_button.keys():
                self.release_key(event.key)
                logging.debug(f"key={self._name(event.key)} pressed up.")


class VirtualKeyboard(device.Device):
    """Handles pygame_gui elements."""
    def __init__(self) -> None:
        event_keys = []
        mutable = True
        disabled = False
        super().__init__(event_keys, mutable, disabled)

    def _name(self, key: int) -> str:
        return f"uniqueID={key}. Pygame GUI element."

    def handle_events(self, event: pg.event.Event) -> None:
        if self.disabled: return # device is not active

        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            # start button press
            key = id(event.ui_element)
            if key in self._key_to_button.keys():
                self.press_key(key)
                logging.debug(f"key={self._name(key)} pressed down.")

        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            # button released
            key = id(event.ui_element)
            if key in self._key_to_button.keys():
                self.release_key(key)
                logging.debug(f"key={self._name(key)} pressed up.")

    def new_key_from_gui_element(self, element) -> None:
        self._new_key(id(element))

    def get_from_gui_element(self, element) -> device.PygameButton:
        return self.get(id(element))