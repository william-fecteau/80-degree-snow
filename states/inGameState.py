from collections import namedtuple
from re import T
from typing import NamedTuple
import pygame
from constants import TARGET_FPS
from states.payloads import InGameStatePayload

from .state import State

class InGameState(State):
    def __init__(self, game, screen: pygame.Surface):
        super().__init__(game, screen)

    def update(self) -> None:
        for event in self.game.events:
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                self.game.switchState("MenuState")
        


    def draw(self) -> None:
        pass


    def onEnterState(self, payload: InGameStatePayload) -> None:
        pass

    def onExitState(self) -> None:        
        pass

