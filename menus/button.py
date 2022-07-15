import pygame
from constants import EMERALD, HONEYDEW, ZOMP

from utils import Utils

class ButtonStyle:
    DEFAULT_FONT = './res/SnakeFont.ttf'
    DEFAULT_FONT_SIZE = 12

    def __init__(self, textColor: tuple[int, int, int] = None, bgColor: tuple[int, int, int] = None, hoverColor: tuple[int, int, int] = None, font: pygame.font.Font = None):
        self.textColor = textColor if textColor != None else HONEYDEW
        self.bgColor = bgColor if bgColor != None else ZOMP
        self.hoverColor = hoverColor if hoverColor != None else EMERALD
        self.font = font if font != None else pygame.font.Font(ButtonStyle.DEFAULT_FONT, ButtonStyle.DEFAULT_FONT_SIZE)

class Button:
    def __init__(self, rectangle: pygame.Rect, text: str, clickAction: callable, style: ButtonStyle = None):
        self.rect = rectangle
        self.text = text
        self.clickAction = clickAction
        self.style = style if style != None else ButtonStyle()

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.style.textColor, self.rect)
        if (self.isMouseOver()):
            pygame.draw.rect(screen, self.style.hoverColor, self.rect.inflate(-5, -5))
        else:
            pygame.draw.rect(screen, self.style.bgColor, self.rect.inflate(-5, -5))
        
        text = self.style.font.render(self.text, 1, self.style.textColor)
        textRect = text.get_rect()
        textRect.center = self.rect.center
        screen.blit(text, textRect)

    def isMouseOver(self):
        return self.rect.collidepoint(Utils.getMousePos())

    def update(self):
        if (Utils.checkClicked(self.rect)):
            self.clickAction()