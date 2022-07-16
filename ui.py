import pygame
from anim.spritesheet import SpriteSheet
from constants import WIDTH, HEIGHT


class UI:
    def __init__(self) -> None:
        self.frostLevel = 0
        self.maxFrost = 10
        self.frostMeterSprite = SpriteSheet("res/frostometer.png", 64, 512)
        pass

    def addFrost(self, frostAmount: int) -> None:
        if self.frostLevel + frostAmount <= self.maxFrost:
            self.frostLevel += frostAmount
        else:
            # Lower the dice value function
            pass

    def heatWave(self, heatwaveValue: int) -> None:
        self.frostLevel -= heatwaveValue

    def draw(self, surface: pygame.Surface) -> None:
        rightUi = pygame.Surface((WIDTH/4, HEIGHT))
        rightUiRect = rightUi.get_rect(topright=(WIDTH, 0))

        frostMeter = self.frostMeterSprite.image_at(self.frostLevel, 0, -1)
        frostMeterRect = frostMeter.get_rect()
        frostMeterRect.centery = rightUiRect.centery
        frostMeterRect.left += 25

        rightUi.blit(frostMeter, frostMeterRect)

        surface.blit(rightUi, rightUiRect)
