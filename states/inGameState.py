from collections import namedtuple
from re import T
from typing import NamedTuple
import pygame
from constants import TARGET_FPS
from sprites.player import Player
from states.payloads import InGameStatePayload

from .state import State

class InGameState(State):
    def __init__(self, game, screen: pygame.Surface):
        super().__init__(game, screen)

    def update(self) -> None:
        for event in self.game.events:
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                self.game.switchState("MenuState")
        
        self.player.update()

        


    def draw(self) -> None:
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.player.image, self.player.rect)


    def onEnterState(self, payload: InGameStatePayload) -> None:
        self.background = pygame.image.load("res/pepi.png")
        self.player = Player(pygame.image.load("res/player.png"), x=100, y=100)


    def onExitState(self) -> None:
        self.background = None
        self.player = None

