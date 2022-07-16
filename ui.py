import pygame
import pygame_menu
from anim.spritesheet import SpriteSheet
from constants import WIDTH, HEIGHT


class UI:
    def __init__(self) -> None:
        self.pixelFont = pygame.font.Font(pygame_menu.font.FONT_MUNRO, 48)
        self.frostMeterSprite = SpriteSheet("res/frostometer.png", 64, 512)
        # get dices
        pass

    def draw(self, surface: pygame.Surface, frostAmount: int) -> None:
        rightUi = pygame.Surface((WIDTH/4, HEIGHT))
        rightUiRect = rightUi.get_rect(topright=(WIDTH, 0))

        frostMeter = self.frostMeterSprite.image_at(frostAmount - 1, 0, -1)
        frostMeterRect = frostMeter.get_rect()
        frostMeterRect.centery = rightUiRect.centery
        frostMeterRect.left += 25

        frostText = self.pixelFont.render(
            str(frostAmount), True, (255, 255, 255))
        frostTextRect = frostText.get_rect()
        frostTextRect.centerx = frostMeterRect.centerx
        frostTextRect.top = frostMeterRect.bottom + 25

        rightUi.blit(frostText, frostTextRect)

        rightUi.blit(frostMeter, frostMeterRect)

        surface.blit(rightUi, rightUiRect)
