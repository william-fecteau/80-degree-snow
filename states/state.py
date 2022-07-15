from typing import NamedTuple
from display import Renderer
import pygame

class State:
    def __init__(self, game, renderer: Renderer):
        self.renderer = renderer
        self.game = game


    def update(self) -> None:
        pass


    def draw(self) -> None:
        pass


    def onExitState(self) -> None:
        pass


    def onEnterState(self, payload: NamedTuple) -> None:
        pass