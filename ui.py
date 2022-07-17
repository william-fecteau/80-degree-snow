import pygame
import pygame_menu
import os
from anim.spritesheet import SpriteSheet
from constants import WIDTH, HEIGHT


class UI:
    def __init__(self) -> None:
        self.pixelFont = pygame.font.Font(
            os.path.join("res", "fonts", 'PressStart2P.ttf'), 36)
        self.diceSprite = SpriteSheet("res/dice.png", 128, 128)
        self.frostMeterSprite = SpriteSheet("res/frostometer.png", 64, 512)
        # get dices
        pass

    def draw(self, surface: pygame.Surface, frostAmount: int, heatwave: list) -> None:
        # Draw right UI
        self.rightUi = pygame.Surface((WIDTH/4, HEIGHT))
        self.rightUiRect = self.rightUi.get_rect(topright=(WIDTH, 0))

        # Draw left UI
        self.leftUi = pygame.Surface((WIDTH/4, HEIGHT))
        self.leftUiRect = self.leftUi.get_rect(topleft=(0, 0))

        self.drawFrostOMeter(frostAmount)

        self.drawDice(heatwave)

        surface.blit(self.rightUi, self.rightUiRect)
        surface.blit(self.leftUi, self.leftUiRect)

    def drawFrostOMeter(self,  frostAmount) -> None:
        frostMeter = self.frostMeterSprite.image_at(frostAmount - 1, 0, -1)
        frostMeterRect = frostMeter.get_rect()
        frostMeterRect.centery = self.rightUiRect.centery
        frostMeterRect.left += 25

        frostText = self.pixelFont.render(
            str(int(frostAmount)), True, (255, 255, 255))
        frostTextRect = frostText.get_rect()
        frostTextRect.centerx = frostMeterRect.centerx
        frostTextRect.top = frostMeterRect.bottom + 25

        self.rightUi.blit(frostText, frostTextRect)

        self.rightUi.blit(frostMeter, frostMeterRect)

    def drawDice(self, heatwave: list) -> None:
        diceYOffset = 16
        diceYStart = HEIGHT - diceYOffset

        for i in range(len(heatwave)):
            diceImage = self.diceSprite.image_at(heatwave[i], 0, -1)
            diceRect = diceImage.get_rect()
            diceRect.right = self.leftUiRect.right - 50
            diceRect.bottom = diceYStart - (i * (128 + diceYOffset))

            self.leftUi.blit(diceImage, diceRect)

        pass
