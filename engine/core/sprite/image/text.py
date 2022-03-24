from typing import Tuple

import pygame as pg
# from pygame import font
import textwrap

from pygame.font import Font


pg.font.init()
SMALL_FONT = pg.font.Font(None, 12)
FONT = pg.font.Font(None, 24)
LARGE_FONT = pg.font.Font(None, 48)

def get_text_surfaces(pg_font: pg.font.Font, string_list: list[str], font_color: Tuple[int, int, int], 
    background_color: Tuple[int, int, int]) -> tuple[pg.Surface]:
    return tuple(get_text(pg_font, string, font_color, background_color) for string 
        in string_list)

def get_text(pg_font: pg.font.Font, string: str, font_color: Tuple[int, int, int], 
    background_color: Tuple[int, int, int]=None) -> pg.Surface:
    # TODO: change name to get surfaces from text
    if background_color is not None:
        text_surface = pg_font.render(string, True, font_color, background_color)
    else:
            text_surface = pg_font.render(string, True, font_color)
    return text_surface

def blit_text(target_surface: pg.Surface, surface_to_blit: pg.Surface, xy: tuple, i :int=0,
    descending: bool=True, line_spacing: int=0, centered:bool=False):

    def center_surface_about_point(surface: pg.Surface, xy: tuple) -> tuple:
        w, h = surface.get_rect().size[:]
        x, y = xy[:]
        return (x - round(w/2), y - round(h/2))

    x, y = xy[:]
    w, h = surface_to_blit.get_rect().size[:]
    if descending:
        xy = x, y + i*(h + line_spacing)
    else:
        xy = x, y - i*(h + line_spacing)
    if centered:
        xy = center_surface_about_point(surface_to_blit, xy)
    target_surface.blit(surface_to_blit, xy)

def blit_text_surfaces(target_surface: pg.Surface, text_surfaces: list, xy: tuple, 
    descending: bool=True, line_spacing: int=0, centered: bool=False):
    for i, surface in enumerate(text_surfaces):
        blit_text(target_surface, surface, xy, i, descending, line_spacing, centered)

def render_text(target_surface: pg.Surface, xy: tuple, str_to_render: str, centered=False) -> None:
    """Render text to target surface. Dirty method."""
    text_sur = get_text(SMALL_FONT, str_to_render, (0, 0, 0), (255, 255, 255))
    blit_text(target_surface, text_sur, xy, centered=centered)

def get_text_size(text_surfaces: list[pg.Surface], line_spacing: int) -> tuple:
    """Assuming surfaces are blitted downwards along y axis."""
    if line_spacing < 0: raise ValueError
    x = y = 0
    # w = max(text_surfaces, key=lambda surface: surface.get_rect().width) # get loargest width in list
    # h = len(text_surfaces) * line_spacing
    # print(w, h)
    # return (w, h)
    for surface in text_surfaces:
        w = surface.get_rect().width
        x = max(x, w) # get max width
        y += line_spacing # every line is spaced equally
    return (x, y)

def get_wrapped_text_surfaces(pg_font: pg.font.Font, string_list: list[str], font_color: Tuple[int, int, int], 
    background_color: Tuple[int, int, int], max_char_per_line: int) -> tuple[pg.Surface]:
    surfaces = []
    for string in string_list:
        substrings = string.split("\n")
        for substr in substrings:
            if substr:
                # non-empty string
                wrapped_strings = textwrap.wrap(substr, max_char_per_line, expand_tabs=True,
                    replace_whitespace=True)
                if wrapped_strings:
                    # non-empty list
                    text_surfaces = get_text_surfaces(pg_font, wrapped_strings, font_color, background_color)
                    surfaces.extend(text_surfaces)
    return tuple(surfaces)


if __name__ == "__main__":
    import pygame
    from pygame.locals import *

    def main():
        # Initialise screen
        pygame.init()
        screen = pygame.display.set_mode((500, 500))
        pygame.display.set_caption('Basic Pygame program')

        # Fill background
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background.fill((250, 250, 250))
        font = LARGE_FONT
        text = """When your game is entering small scenes you might think that you don't need to handle events, but there is one event you should always check for: the pygame.QUIT event (sent when the user press the close button at the top corner). In your example you're not allowing the user to quit during the game over sequence (you're providing the player a button to click but a user would also expect clicking the close button would close the game as well)."""
        surfaces = get_wrapped_text_surfaces(font, [text, "HELLO WORLD!", "end"], (0, 0, 0), None, 25)
        LINESIZE = font.get_linesize()
        bounding_rect = pg.Rect((0, 0), get_text_size(surfaces, LINESIZE))
        # Blit everything to the screen
        screen.blit(background, (0, 0))
        pygame.display.flip()

        # Event loop
        while 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return

            screen.blit(background, (0, 0))
            pg.draw.rect(screen, (200, 200, 200), bounding_rect)
            
            x = y = 0
            for surface in surfaces:
                blit_text(screen, surface, (x, y))
                y += LINESIZE
            # blit_text_surfaces(screen, surfaces, (0, 0), True, line_spacing=SMALL_FONT.get_linesize())
            #blit_text(screen, surfaces[0], (0, 0))
            pygame.display.flip()





    main()