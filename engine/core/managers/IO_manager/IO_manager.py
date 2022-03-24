import logging

import pygame as pg
import pygame_gui

import devices


class IOManager:
    """Handles all input and output for the game."""
    __slots__ = ("root", "keyboard", "mouse", "ui_manager", "virtual_keyboard")
    def __init__(self, root, ui_manager, keyboard=True, mouse=True) -> None:
        self.root = root
        self.keyboard: devices.Keyboard = devices.Keyboard(not keyboard)
        self.mouse: devices.Mouse = devices.Mouse(not mouse)
        self.ui_manager: pygame_gui.UIManager = ui_manager
        self.virtual_keyboard: devices.VirtualKeyboard = devices.VirtualKeyboard() 
        logging.debug(f"keyboard_active={keyboard}, mouse_active={mouse}")

    def update(self, dt: float) -> None:
        self.ui_manager.update(dt)

    def handle_events(self, event: pg.event.Event) -> None:
        self.keyboard.handle_events(event)
        self.mouse.handle_events(event)
        self.virtual_keyboard.handle_events(event)
        self.ui_manager.process_events(event)

    def draw(self, surface: pg.Surface) -> None:
        self.ui_manager.draw_ui(surface)
        # manaul wheel resetting. TODO fix this issue
        self.mouse.wheel_states = (False, False)

if __name__ == "__main__":
    IOManager()