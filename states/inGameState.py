from collections import namedtuple
from re import T
import pygame
from .payloads import InGameStatePayload
from levels import loadLevel, Level

from .state import State


class InGameState(State):
    def __init__(self, game, screen: pygame.Surface):
        super().__init__(game, screen)

    def update(self, events, keys) -> None:
        for event in events:
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                self.game.switchState("MenuState")
            elif event.type == pygame.KEYUP and event.key == pygame.K_n:
                if (self.level.num + 1 == 5):
                    self.game.switchState("EndGameState")
                    return
                else:
                    self.game.switchState(
                        "InGameState", InGameStatePayload(self.level.num + 1))

        if (self.level.num + 1 == 5):
             self.game.switchState("EndGameState")

        self.level.update(self.game, events, keys)

    def draw(self) -> None:
        self.level.draw()

    def onEnterState(self, payload: InGameStatePayload) -> None:

        self.level: Level = loadLevel(
            self.game, self.screen, payload.levelNum)

    def onExitState(self) -> None:
        self.level = None
