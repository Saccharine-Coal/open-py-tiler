from random import randint

import pygame as pg

from elements.world import hash_array, tiles, axes
from core.math import points, projections, translations
from core.abstract import sprites
import elements.sprites


class HexagonalWorld(sprites.AbstractActiveSprite):
    """Holds grids, projection, and translation matrices."""
    def __init__(self, game, surface, origin: tuple, dimensions: tuple, unit_size: int, file_manager):
        self._game = game
        self.unit_size = unit_size
        self.set_bounding_rect(surface.get_rect())
        self.ZOOM_LEVELS = ZOOM_LEVELS = (5, 10, 40, 70, 150)
        self.zoom_i = 0
        self.update_zoom = True
        self.projector = projections.IsometricProjector(self.get_level())
        self.translator = translations.Translator(origin)
        self.updated = True
        self.array = hash_array.AxialHashArray(*dimensions, unit_size)
        file_manager.add("basic.png", ["assets", "sprites"])
        file_manager.add("uniform_lighting.png", ["assets", "sprites"])
        self.array.populate(tiles.Tile, file_manager.get("uniform_lighting.png", ["assets", "sprites"]))
        self.axis = axes.Axes(unit_size)
        # self.player = elements.sprites.AnimatedSprite((0, 0, 0, 0), unit_size)
        self.direction = points.PointQRSZ(0, 0, 0, 0)
        self.update(dt=0)



    def __repr__(self) -> str:
        return self.__class__.__name__

    # PUBLIC ----------------------------------------------------------------------------------------------

    def set_bounding_rect(self, bounding_rect: pg.Rect):
        PADDING = .5
        inflated_size = tuple(element * PADDING for element in bounding_rect.size)
        self.rect = bounding_rect.inflate(inflated_size)
        self.surface = pg.Surface(bounding_rect.size)

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            self.updated = True
        if event.type == pg.MOUSEBUTTONDOWN:
            self.updated = True
            if event.button == 1:
                pass
            if event.button == 4:
                self.set_i(self.zoom_i + 1)
                print("zoom in")
            if event.button == 5:
                self.set_i(self.zoom_i - 1)

        # (x, y) = tuple(val/500 for val in self.mouse.right_button.drag_line.relsize())
        # self.translator.translate(dx=-x, dy=y)



    def set_i(self, i):

        MIN, MAX = 0, len(self.ZOOM_LEVELS) - 1
        i = min(max(i, MIN), MAX)
        if i != self.zoom_i:
            self.zoom_i = i
            self.update_zoom = True

    def get_level(self) -> int:
        return self.ZOOM_LEVELS[self.zoom_i]

    def get_ratio(self) -> float:
        MAX = self.ZOOM_LEVELS[-1]
        unit_length = self.get_level()
        return MAX / unit_length

    def _update_matrices(self):
        if self.update_zoom:
            self.projector.set_scale(self.get_level())
            self.projector.update()
        self.translator.update()

    def update(self, dt=0):
        # TODO
        self.updated = True
        MOVE = 0.1
        if self._game.keyboard.get(pg.K_LEFT):
            self.direction = self.direction.add(points.QVECTOR)
        if self._game.keyboard.get(pg.K_RIGHT):
            self.direction = self.direction.add(points.QVECTOR.mult(-1))
        if self._game.keyboard.get(pg.K_UP):
            self.direction = self.direction.add(points.RVECTOR.mult(-1))
        if self._game.keyboard.get(pg.K_DOWN):
            self.direction = self.direction.add(points.RVECTOR)
        # self.player.move(*self.direction, scale=MOVE)
        # self.player.update(dt)
        if self.updated:
            self.updated = False
            self._update_matrices()
            self.axis.project(self.projector.matrix, self.translator.matrix)

            # self.player.project(self.projector.matrix, self.translator.matrix)
            # self.player.scale(self.get_level())
            for tile in self.array._hashtable.values():
                tile.project(self.projector.matrix, self.translator.matrix)
                tile.scale(self.get_level())


    def draw(self, surface: pg.Surface):
        for tile in self.array.painters_draw_order(self.rect):
            tile.set_tint(pg.Color(0, 0, 0, 0))
            tile.draw(surface)
        # self.axis.draw(surface)
        # self.player.draw(surface)
        return
        def frame_update():
            from time import sleep
            # return
            TIME = 0.05
            self.surface.blit(self._surface, (0, 0))
            pg.display.flip()
            sleep(TIME)
            self.handle_events(pg.event.get())

        planes = self.array.painters_draw_order()
        trimmed_planes = self.get_tiles_in_surface(planes)
        if self.updated:
            print('drawing')
            self.surface.fill((0, 0, 0))

            # print(f"Number of items drawn in {self} = {sum(len(plane) for plane in trimmed_planes)}.")
            for plane in trimmed_planes:
                for tile in plane:
                    # top
                    tile.render(self.surface)

            #self.axes.draw(self._surface)

            # for value in self.array.hashtable.values():
            # I SPENT HOURSE TRYING TO FIGURE OUT THE ERROR AND IT WAS THIS SINGLE LINE OF CODE!!!!!!!
            self.updated = False
