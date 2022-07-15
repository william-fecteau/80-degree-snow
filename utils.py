import pygame
from display import Renderer

class Utils:
    # Returns the position of the mouse in the game window
    def getMousePos() -> tuple[int, int]:
        mousePos = pygame.mouse.get_pos()
        windowSize = pygame.display.get_window_size()
        return (Utils.regleDeTroisLol(mousePos[0], windowSize[0], Renderer.WIDTH), Utils.regleDeTroisLol(mousePos[1], windowSize[1], Renderer.HEIGHT))

    # Returns a rule of three for the mouse position
    def regleDeTroisLol(currentValue, currentScreenMax, rendererScreenMax) -> int:
        return currentValue*rendererScreenMax/currentScreenMax

    def checkClicked(rectangle: pygame.Rect):
        if rectangle.collidepoint(Utils.getMousePos()) and pygame.event.peek(pygame.MOUSEBUTTONDOWN):
            pygame.event.get(pygame.MOUSEBUTTONDOWN)
            return True
        return False