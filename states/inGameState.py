from collections import namedtuple
from re import T
from typing import NamedTuple
import pygame
from constants import TARGET_FPS

from display import Renderer
from states.payloads import InGameStatePayload

from .state import State

class InGameState(State):
    CELL_SIZE = 32

    def __init__(self, game, renderer: Renderer):
        super().__init__(game, renderer)

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

