import sys, pygame
from typing import NamedTuple
from constants import TARGET_FPS

from display import Renderer
from states import InGameState, MenuState, State

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        # Registering services
        self.renderer = Renderer()

        # States
        self.dicStates = {
            InGameState.__name__: InGameState(self, self.renderer),
            MenuState.__name__: MenuState(self, self.renderer)
        }
        self.curState = MenuState.__name__
        self.nextState = None
        self.nextStatePayload = None

        self.clock = pygame.time.Clock()


    def gameLoop(self) -> None:
        while True:
            if (pygame.event.peek(pygame.QUIT)):
                pygame.quit()
                sys.exit()

            self.events = pygame.event.get()

            if self.nextState is not None:
                self.dicStates[self.curState].onExitState()
                self.curState = self.nextState
                self.dicStates[self.curState].onEnterState(self.nextStatePayload)
                self.nextState = None
                self.nextStatePayload = None

            self.renderer.fill(Renderer.BACKGROUND_COLOR)

            self.dicStates[self.curState].update()
            self.dicStates[self.curState].draw()

            self.renderer.render()
            self.clock.tick(TARGET_FPS)


    def switchState(self, newStateStr: str, payload: NamedTuple = None) -> None:
        if self.nextState is None and newStateStr in self.dicStates:
            self.nextState = newStateStr
            self.nextStatePayload = payload


if __name__ == "__main__":
    Game().gameLoop()
