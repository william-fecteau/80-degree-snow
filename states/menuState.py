from re import S
import pygame
import pygame_menu
import numpy
import os
from math import floor
from anim.spritesheet import SpriteSheet
from constants import BLACK, DARK_BLUE, WHITE, BLUE, SURFACE_SIZE, WIDTH, HEIGHT
from utils import resource_path

from .payloads import InGameStatePayload
from .state import State


class MenuState (State):

    def __init__(self, game, renderer: pygame.Surface):
        super().__init__(game, renderer)
        self.surf = pygame.Surface(SURFACE_SIZE)
        self.playerSpritesheet = SpriteSheet(
            os.path.join('res', 'frosto.png'), 64, 64)
        self.frosto = self.playerSpritesheet.image_at(0, 0, -1)
        self.frosto = pygame.transform.scale(self.frosto, (512, 512))
        self.frostoRect = self.frosto.get_rect()
        self.frostoRect.centerx = WIDTH/6
        self.frostoRect.centery = HEIGHT/2

        # Add other sprite to the right, maybe animate it NTH

        self.bigSnakeFont = pygame.font.Font(
            resource_path(os.path.join("res", "fonts", 'PressStart2P.ttf')), 36)

        self.setupMenu()

        # Setup sounds
        self.menuBoop = pygame.mixer.Sound(resource_path("res/menu2.mp3"))
        self.menuBip = pygame.mixer.Sound(resource_path("res/menu3.mp3"))

        # Sound volumes

        # Setup Music
        self.pourquoiPapillon = pygame.mixer.music.load("res\songs\everythingGoesToShitAgain.mp3")
        pygame.mixer.music.set_volume(0.22)
        pygame.mixer.music.play(0,0,1000)
        pygame.mixer.music.queue("res\songs\pourquoiYaUnPapillon.mp3")
        
        

    def draw(self) -> None:
        self.menu.draw(self.surf)
        logo = pygame.image.load(resource_path(os.path.join('res', 'title.png')))
        logoRect = logo.get_rect()
        logoRect.centerx = WIDTH/2
        logoRect.centery = 150

        self.surf.blit(logo, logoRect)

        self.surf.blit(self.frosto, self.frostoRect)

        self.screen.blit(self.surf, (0, 0))

    def update(self, events, keys) -> None:
        self.menu.update(events)

    def menuAction(self) -> None:
        pygame.mixer.Sound.play(self.menuBoop)
        self.game.switchState("InGameState", InGameStatePayload(1))

    def creditsAction(self) -> None:
        pygame.mixer.Sound.play(self.menuBoop)
        self.game.switchState("CreditsState")

    def setupMenu(self) -> None:
        cool_theme = pygame_menu.themes.THEME_GREEN.copy()
        cool_theme.background_color = BLACK
        cool_theme.widget_font = self.bigSnakeFont
        cool_theme.widget_font_color = WHITE
        cool_theme.selection_color = DARK_BLUE
        cool_theme.widget_font_size = 36
        cool_theme.widget_offset = (0, HEIGHT/2)

        self.menu = pygame_menu.Menu(
            '', WIDTH, HEIGHT, theme=cool_theme, center_content=False)
        self.menu.get_menubar().hide()

        self.menu.add.button('Play', self.menuAction)
        self.menu.add.button('Credits', self.creditsAction)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)
