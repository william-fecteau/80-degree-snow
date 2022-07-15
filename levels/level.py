import pygame
from constants import WIDTH, HEIGHT
from sprites import Player

class Level:
    def __init__(self, screen: pygame.Surface, background: pygame.Surface) -> None:
        self.screen = screen
        self.background = background
        self.player = Player(pygame.image.load("res/player.png"), center=(WIDTH / 2, HEIGHT / 2))


    def update(self, events) -> None:
        self.player.update()


    def draw(self) -> None:
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.player.image, self.player.rect)
