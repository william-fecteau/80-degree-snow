import pygame
from constants import WIDTH, HEIGHT
from sprites import Player


class Level:
    def __init__(self, num: int, screen: pygame.Surface, background: pygame.Surface) -> None:
        self.num = num
        self.screen = screen
        self.background = background
        self.player = Player(pygame.image.load("res/player.png"), center=(WIDTH / 2, HEIGHT / 2))


    def update(self, events, keys) -> None:
        self.pollInput(events, keys)
        self.player.update(events, keys)
        
        # If player goes offscreen, dont lmao
        if self.player.rect.left < 0:
            self.player.rect.left = 0
        elif self.player.rect.right > self.screen.get_width():
            self.player.rect.right = self.screen.get_width()
            
        if self.player.rect.top < 0:
            self.player.rect.top = 0
        elif self.player.rect.bottom > self.screen.get_height():
            self.player.rect.bottom = self.screen.get_height()

        

    def draw(self) -> None:
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.player.image, self.player.rect)


    def pollInput(self, events, keys) -> None:
        pass


def loadLevel(screen: pygame.Surface, levelNum: int) -> Level:
    background = pygame.image.load(f"res/{levelNum}.png")
    level = Level(levelNum, screen, background)
    return level