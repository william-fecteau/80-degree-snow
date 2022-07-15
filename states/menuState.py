from pkg_resources import EGG_DIST
import pygame
import pygame_menu
import numpy
from math import floor
from constants import BLACK, EGGPLANT, EMERALD, GREEN_COLOR, HONEYDEW, ZOMP

from display import Renderer

from .payloads import InGameStatePayload
from .state import State


class MenuState (State):

    def __init__(self, game, renderer: Renderer):
        super().__init__(game, renderer)
        self.surf = pygame.Surface(Renderer.SURFACE_SIZE)
        self.setupMenu()

    def draw(self) -> None:
        self.menu.draw(self.surf)
        self.surf.blit(self.bigSnakeFont.render(
            "Schhhnake", True, GREEN_COLOR), (150, 50))
        self.surf.blit(self.smolSnakeFont.render(
            "A game where a snake eats balls", True, GREEN_COLOR), (150, 125))
        self.surf.blit(self.smolSnakeFont.render("Centering text is hard",
                       True, GREEN_COLOR), (Renderer.WIDTH-450, Renderer.HEIGHT-50))

        for i in range(10):
            self.surf.blit(self.cool_snake, (numpy.random.randint(
                0, Renderer.WIDTH - 100), numpy.random.randint(0, Renderer.HEIGHT - 100)))

        self.surf.blit(self.cool_snake, (900, 150))

        self.renderer.drawSurface(self.surf)

    def update(self) -> None:
        self.menu.update(self.game.events)

    def menuAction(self) -> None:
        self.game.switchState(
            "InGameState", InGameStatePayload(self.rows, self.columns, self.appleSpawn, self.delay, 2))

    def setupMenu(self) -> None:
        cool_theme = pygame_menu.themes.THEME_GREEN.copy()
        cool_theme.background_color = BLACK
        cool_theme.widget_font = self.bigSnakeFont
        cool_theme.widget_font_color = EMERALD
        cool_theme.selection_color = GREEN_COLOR
        cool_theme.widget_offset = (0, 200)

        self.menu = pygame_menu.Menu(
            '', Renderer.WIDTH, Renderer.HEIGHT, theme=cool_theme, center_content=False)
        self.menu.get_menubar().hide()

        self.menu.add.button('Play', self.menuAction)
        self.menu.add.range_slider(
            'Row', default=17, range_values=(5, 25), increment=1, onchange=self.setRow, range_text_value_enabled=False)
        self.menu.add.range_slider(
            'Column', default=17, range_values=(5, 25), increment=1, onchange=self.setColumn, range_text_value_enabled=False)
        self.menu.add.range_slider(
            'Nb Apple', default=1, range_values=(0, 25), increment=1, onchange=self.setAppleSpawn, range_text_value_enabled=False)
        self.menu.add.range_slider(
            'Delay', default=6, range_values=(6, 12), increment=1, onchange=self.setDelay, range_text_value_enabled=False)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)

    def setRow(self, value: int) -> None:
        self.rows = floor(value)

    def setColumn(self, value: int) -> None:
        self.columns = floor(value)

    def setAppleSpawn(self, value: int) -> None:
        self.appleSpawn = floor(value)

    def setDelay(self, value: int) -> None:
        self.delay = floor(value)
