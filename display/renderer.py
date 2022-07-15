import pygame

class Renderer:
    WIDTH = 1600
    HEIGHT = 900
    SURFACE_SIZE = (WIDTH, HEIGHT)
    BACKGROUND_COLOR = (74, 74, 74)


    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((Renderer.WIDTH, Renderer.HEIGHT), pygame.HWSURFACE|pygame.DOUBLEBUF)


    def fill(self, color: tuple[int, int, int]) -> None:
        self.screen.fill(color)


    def drawSurface(self, surface: pygame.Surface, position: tuple[int, int] = (0, 0)) -> None:
        self.screen.blit(surface, position)


    def render(self) -> None:
        self.screen.blit(self.screen, (0, 0))
        pygame.display.flip()