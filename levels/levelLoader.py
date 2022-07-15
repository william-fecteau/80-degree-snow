from .level import Level
import pygame

def loadLevel(screen: pygame.Surface, levelNum: int) -> Level:
    background = pygame.image.load("res/pepi.png")
    level = Level(screen, background)
    return level
