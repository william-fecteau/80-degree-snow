from tkinter import Widget
import pygame
import os
from anim.spritesheet import SpriteSheet

from constants import WIDTH, BLACK, HEIGHT, WHITE
from utils import resource_path
from .state import State


class EndGameState(State):
    def __init__(self, game, renderer: pygame.Surface):
        super().__init__(game, renderer)
        self.pixelFontBig = pygame.font.Font(
            resource_path(os.path.join("res", "fonts", 'PressStart2P.ttf')), 48)
        self.pixelFont = pygame.font.Font(
            resource_path(os.path.join("res", "fonts", 'PressStart2P.ttf')), 24)
        self.pixelFontSmall = pygame.font.Font(
            resource_path(os.path.join("res", "fonts", 'PressStart2P.ttf')), 18)

        self.frostoSpritesheet = SpriteSheet(
            resource_path(os.path.join('res', 'frosto-idle.png')), 512, 512)

        self.heartSpritesheet = SpriteSheet(
            resource_path(os.path.join('res', 'iceHeart.png')), 128, 128)

    def update(self, events, keys) -> None:
        for event in events:
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                self.game.switchState("MenuState")

    def draw(self) -> None:
        self.screen.fill(BLACK)

        animationFrame = int(pygame.time.get_ticks() / 250 % 4)

        creditsTitle = self.pixelFontBig.render(
            "You beat the demo!", True, WHITE)
        creditsTitleRect = creditsTitle.get_rect()
        creditsTitleRect.centerx = WIDTH / 2
        creditsTitleRect.centery = 200
        self.screen.blit(creditsTitle, creditsTitleRect)

        frosto = self.frostoSpritesheet.image_at(animationFrame, 0, -1)
        smallerFrosto = pygame.transform.scale(frosto, (256, 256))
        frostoRect = smallerFrosto.get_rect()
        frostoRect.centerx = WIDTH/2
        frostoRect.centery = HEIGHT/2 + 100
        self.screen.blit(smallerFrosto, frostoRect)

        heart = self.heartSpritesheet.image_at(0, 0, -1)
        heartRect = heart.get_rect()
        heartRect.centery = HEIGHT/2 + 100

        leftHeartRect = heartRect.copy()
        leftHeartRect.centerx = WIDTH/4

        heartRect.centerx = WIDTH - WIDTH/4

        self.screen.blit(heart, heartRect)
        self.screen.blit(heart, leftHeartRect)

        creditsFuture = self.pixelFont.render(
            'Play again later to defeat your arch nemisis, the sun!', True, WHITE)
        creditsFutureRect = creditsFuture.get_rect()
        creditsFutureRect.centerx = WIDTH / 2
        creditsFutureRect.centery = creditsTitleRect.bottom + 100
        self.screen.blit(creditsFuture, creditsFutureRect)

        creditsEscape = self.pixelFont.render(
            'Press ESC to return to the menu', True, WHITE)
        creditsEscapeRect = creditsEscape.get_rect()
        creditsEscapeRect.centerx = WIDTH / 2
        creditsEscapeRect.centery = HEIGHT - 50
        self.screen.blit(creditsEscape, creditsEscapeRect)

        pass
