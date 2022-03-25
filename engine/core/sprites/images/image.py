import pygame as pg


class Image:
    """This class handles all image functions."""
    __slots__ = "_true_surface", "_true_rect", "centered", "__dict__"
    def __init__(self, surface: pg.Surface, centered: bool) -> None:
        self._true_surface = surface
        self._true_rect = surface.get_rect()
        self.surface = surface
        self.rect: pg.Rect = self._true_rect.copy()
        self.centered = centered
        self.scale(1)
        self.set_tint(pg.Color(0, 0, 0, 0))
        self.updated = False

    @property
    def factor(self) -> float:
        CORRECTION = 2.46
        RATIO = self._true_rect.width
        #return 1 / RATIO
        return CORRECTION / RATIO

    @property
    def _active_surface(self) -> pg.Surface:
        """Wrapper function to reduce transform calls."""
        if self.updated:
            self.surface = pg.transform.scale(self._true_surface, self.rect.size)
            self.updated = False
        return self.surface

    @property
    def mask(self) -> pg.mask.Mask:
        return pg.mask.from_surface(self._active_surface)
    '''
    @property
    def _tint(self) -> pg.Surface:
        """Really expensive image "tinting"."""
        tinted_surface = self.surface.copy()
        tinted_surface.fill(self._tint_color, special_flags=pg.BLEND_RGBA_MULT)
        # tinted_surface.set_alpha(self._tint_alpha)
        return tinted_surface
    '''
    def collidepoint(self, img_topleft: tuple, xy: tuple) -> bool:
        """I think this should be moved into the sprite class."""
        self.updated = True
        if self._active_surface is None: return False # tile is not being rendered
        img_topleft = self.center(img_topleft)
        rect = self.rect.move(*img_topleft)
        if rect.collidepoint(*xy):
            # in rect
            xy_in_mask = tuple(a - b for a, b in zip(xy, img_topleft))
            if self.mask.get_at(xy_in_mask) == 1:
                # in mask
                return True
        return False

    def scale(self, factor: float):
        factor = factor * self.factor
        new_w, new_h = tuple(factor * val for val in self._true_rect.size)
        if self.rect is not None:
            if (new_w, new_h) ==  self.rect.size: return None
        rect = pg.Rect(0, 0, new_w, new_h)
        self.rect = rect
        self.updated = True
        # always update image for consistent pixel perfect collision

    def center(self, xy: tuple) -> tuple[int, int]:
        if self.centered:
            x, y = xy[:]
            dw, dh = tuple(val / 2 for val in self.rect.size)
            if dw != dh:
                # no idea why this works
                return (x - dw, y - dh - dw)
            return (x - dw, y - dh)
        return xy

    def set_tint(self, color: pg.Color) -> None:
        self._tint_color = color

    def draw(self, surface: pg.Surface, xy: tuple, alpha=255) -> None:
        self._active_surface.set_alpha(alpha)
        if alpha < 1: return
        xy = self.center(xy)
        #if self._tint_color.a != 255:
        #    surface.blit(self._active_surface, xy)
        #if self._tint_color.a != 0:
        #    surface.blit(self._tint, xy)
        if self._active_surface is None:
            return # tile is not being rendered
        else:
            surface.blit(self.surface, xy)
