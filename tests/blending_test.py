
import pygame as pg

from core import game
from core.image import animated




class Game2(game.Game):
    def __init__(self, fullscreen: bool = False):
        super().__init__(fullscreen)
        self.SPRITE = animated.Animation(100, "assets", "animations", "plant")
        self.SPRITE.scale(self.SPRITE._unit_size)
        self.time = 0


    def _render(self):
        self.time += self._dt * 10
        self.SPRITE.update(self._dt*10)
        self.screen.fill((100, 100, 50))
        DARKTINT = pg.Surface(self.screen.get_rect().size)
        DARKTINT.fill((0, 0, 0))
        val = self.time % 255
        DARKTINT.set_alpha(val)
        print(val)
        # self._scene_manager.render(self.screen)
        for sprite in self.sprites:
            sprite.draw(self.screen)
        self._ui_manager.draw_ui(self.screen)
        self.SPRITE.draw(self.screen, (100, 100))
        self.screen.blit(DARKTINT, (0, 0), special_flags=pg.BLEND_ALPHA_SDL2)
        
        pg.display.flip()




app = Game2()
app.run()

# import math
# i = 0
# j = i
# while 1:
#     i += .01
#     j = i
#     j = j % 5
#     print(i, math.floor(j))