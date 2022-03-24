import os
from tabnanny import verbose

import pygame as pg
from pygame_gui.ui_manager import UIManager

from core.abstract import sprites
from core.utils import file_manager

SET_FULLSCREEN = False

HALF = SET_FULLSCREEN
if HALF:
    WIDTH, HEIGHT = 1920, 1080
else:
    WIDTH, HEIGHT = int(1920/2), int(1080/2)

FPS = 30


class Game:
    """This class handles initialization of the pygame object, pygame events, game updates, and pygame drawing."""

    def __init__(self, fullscreen: bool=False):
        self._init_pygame() # pygame init
        self._init_extras()
        self._running = True
        # TODO add fullscreen to game object
        self._FULLSCREEN = fullscreen

    # UNMUTABLE LOOP ---------------------------------------

    def run(self):
        """Runs pygame."""
        while self._running:
            # ACTUAL GAME LOOP
            self._dt = self._clock.tick(FPS) / 1000
            self._events()
            self._update()
            self._render()
        pg.display.quit()
        pg.quit()

    # MUTABLE LOOPS ------------------------------------

    def _init_pygame(self):
        """Initialize pygame characteristics, programs, and attributes here.
        Iniitialize starting scene here."""
        pg.init()
        if SET_FULLSCREEN: flags = pg.DOUBLEBUF | pg.FULLSCREEN# | pg.HWSURFACE
        else: flags = pg.DOUBLEBUF
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), flags)
        self._clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)

    def _init_extras(self):
        path_to_theme = os.path.join("data", "theme.json")
        self._ui_manager: UIManager = UIManager(self.screen.get_rect().size, path_to_theme, enable_live_theme_updates=True)
        self._file_manager = file_manager.FileManager(True) 
        self.sprites: list[sprites.AbstractActiveSprite] = []
        import keyboard
        self.keyboard = keyboard.Keyboard(mutable=True, verbose=False)
        
        return
        load.load_font(self._ui_manager)
        self._keyboard = Keyboard(verbose=True, repeat=0)
        self._scene_manager: SceneManager = SceneManager(self.screen.get_rect().size, self._ui_manager, self._keyboard)

    def add_sprite(self, sprite: sprites.AbstractActiveSprite) -> None:
        if not isinstance(sprite, sprites.AbstractActiveSprite): raise TypeError(f"Not type={sprites.AbstractActiveSprite}")
        self.sprites.append(sprite)

    def _events(self):
        """Catch all pygame events here."""
        events = pg.event.get()
        for event in events:
            for sprite in self.sprites:
                sprite.handle_events(event)
            self.keyboard.handle_events(event)
        #     self._keyboard.handle_events(event)
        #     self._scene_manager.handle_events(event)
        #     self._ui_manager.process_events(event)
        self._running = self._process_quitting(events, True) # check if quitting after
        if self.keyboard.get(pg.K_DOWN, pg.K_LEFT):
            print("down + left")

    def _update(self):
        """Update active scene here."""
        self._ui_manager.update(self._dt)
        for sprite in self.sprites:
            sprite.update(self._dt)
        # self.keyboard._reset()
        return
        self._scene_manager.update(self._dt)
        

    def _render(self):
        """
        Render directly to the pygame window or 'screen' here.
        """
        pg.display.set_caption(f"fps={round(self._clock.get_fps())}")
        self.screen.fill((0, 0, 0))
        # self._scene_manager.render(self.screen)
        for sprite in self.sprites:
            sprite.draw(self.screen)
        self._ui_manager.draw_ui(self.screen)
        pg.display.flip()


    @staticmethod
    def _process_quitting(events, escape_to_quit=False) -> bool:
        running = True
        for event in events:
            if event.type == pg.QUIT:
                running = False
            if escape_to_quit and event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
        return running
