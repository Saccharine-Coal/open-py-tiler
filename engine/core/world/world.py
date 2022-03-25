import pygame as pg

from core.world.arrays.qrsz_array import HashArrayQRSZ
from core.math.transformations import projections, translations, scalers
from core.world import tiles
from core.sprites import sprite

class WorldQRSZ(sprite.Sprite):
    """Holds grids, projection, and translation matrices."""
    def __init__(self, qrz_dimensions):
        # init array
        self._array = HashArrayQRSZ(qrz_dimensions)
        path = "/home/pi/local_code/open_src_tile_engine/engine/data/assets/sprites/floor-1.png"
        surface = pg.image.load(path).convert_alpha()
        self._array.populate(tiles.Tile, surface)
        # init matrices
        self._proj_mx = projections.IsometricProjection(1)
        self._trans_mx = translations.TranslationMatrix3((10, 100, 0))
        self._scale_mx = scalers.ScalingMatrix3(50)

    def __repr__(self) -> str:
        return self.__class__.__name__

    # PUBLIC ----------------------------------------------------------------------------------------------

    def set_bounding_rect(self, bounding_rect: pg.Rect):
        PADDING = .5
        inflated_size = tuple(element * PADDING for element in bounding_rect.size)
        self.rect = bounding_rect.inflate(inflated_size)
        self.surface = pg.Surface(bounding_rect.size)

    def handle_events(self, event):
        return
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
        for tile in self._array.get_all():
            tile.project(self._proj_mx, self._scale_mx, self._trans_mx)
            tile.scale(self._scale_mx._scale)
        return
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
        for tile in self._array.get_all():
            tile.draw(surface)
            # rgb(255, 0, 0)
            pg.draw.circle(surface, (255, 0, 0), tile.projection, 1)
        return
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
