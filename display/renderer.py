import pygame

from sprites import CameraGroup

class Renderer:
    ASPECT_RATIO = (16, 9)
    WIDTH = 1280
    HEIGHT = 720
    SURFACE_SIZE = (WIDTH, HEIGHT)
    BACKGROUND_COLOR = (74, 74, 74)


    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((Renderer.WIDTH, Renderer.HEIGHT), pygame.HWSURFACE|pygame.DOUBLEBUF)
        self.initialScreen = self.screen.copy()
        self.target = None


    def resizeDisplay(self, newSize: tuple[int, int]) -> None:
        # Currently, the display is not resizable. This function is never called
        height = Renderer.ASPECT_RATIO[1] * newSize[0] // Renderer.ASPECT_RATIO[0]
        self.screen = pygame.display.set_mode((newSize[0], height), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)


    def fill(self, color: tuple[int, int, int]) -> None:
        self.initialScreen.fill(color)


    def computeCameraOffset(self) -> pygame.math.Vector2:
        targetPos = self.initialScreen.get_rect().center if self.target is None else self.target
        return pygame.math.Vector2(targetPos) - pygame.math.Vector2(self.initialScreen.get_size()) / 2


    def drawCameraGroup(self, spriteGroup: CameraGroup) -> None:
        cameraOffset = self.computeCameraOffset()
        spriteGroup.customDraw(self.initialScreen, cameraOffset)


    def drawCameraSurface(self, surface: pygame.Surface, position: tuple[int, int] = (0, 0)) -> None:
        cameraOffset = self.computeCameraOffset()
        offsetPos = position - cameraOffset
        self.initialScreen.blit(surface, offsetPos)


    def drawSurface(self, surface: pygame.Surface, position: tuple[int, int] = (0, 0)) -> None:
        self.initialScreen.blit(surface, position)


    def setCameraTarget(self, target: tuple[int,int]) -> None:
        self.target = target


    def render(self) -> None:
        scaledScreen = pygame.transform.scale(self.initialScreen, self.screen.get_size())
        self.screen.blit(scaledScreen, (0, 0))
        pygame.display.flip()