from typing import NamedTuple
import pygame

class State:
    def __init__(self, game, screen: pygame.Surface):
        self.screen = screen
        self.game = game


    def update(self, events, keys) -> None:
        pass


    def draw(self) -> None:
        pass


    def onExitState(self) -> None:
        pass


    def onEnterState(self, payload: NamedTuple) -> None:
        pass