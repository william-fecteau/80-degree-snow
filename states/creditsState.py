import pygame
import os
from anim.spritesheet import SpriteSheet

from constants import WIDTH, BLACK, HEIGHT, WHITE
from .state import State


class CreditsState(State):
    def __init__(self, game, renderer: pygame.Surface):
        super().__init__(game, renderer)
        self.pixelFontBig = pygame.font.Font(
            os.path.join("res", "fonts", 'PressStart2P.ttf'), 72)
        self.pixelFont = pygame.font.Font(
            os.path.join("res", "fonts", 'PressStart2P.ttf'), 36)
        self.pixelFontSmall = pygame.font.Font(
            os.path.join("res", "fonts", 'PressStart2P.ttf'), 18)

        self.jordanSpriteSheet = SpriteSheet(
            os.path.join('res', 'tt.png'), 128, 128)

        self.nathanSpritesheet = SpriteSheet(
            os.path.join('res', 'saurus.png'), 128, 128)

        self.alexSpritesheet = SpriteSheet(
            os.path.join('res', 'wiisp.png'), 128, 128)

        self.williamSpritesheet = SpriteSheet(
            os.path.join('res', 'schhnake.png'), 128, 128)

        self.lambertSpritesheet = SpriteSheet(
            os.path.join('res', 'headphones.png'), 128, 128)

    def update(self, events, keys) -> None:
        for event in events:
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                self.game.switchState("MenuState")

    def draw(self) -> None:
        self.screen.fill(BLACK)

        animationFrame = int(pygame.time.get_ticks() / 1000 % 2)

        creditsTitle = self.pixelFontBig.render(
            "Credits", True, WHITE)
        creditsTitleRect = creditsTitle.get_rect()
        creditsTitleRect.centerx = WIDTH / 2
        creditsTitleRect.centery = 150
        self.screen.blit(creditsTitle, creditsTitleRect)

        creditsEscape = self.pixelFont.render(
            'Press ESC to return to the menu', True, WHITE)
        creditsEscapeRect = creditsEscape.get_rect()
        creditsEscapeRect.centerx = WIDTH / 2
        creditsEscapeRect.centery = HEIGHT - 50
        self.screen.blit(creditsEscape, creditsEscapeRect)

        gmtkText = self.pixelFontSmall.render(
            "Game made for the GMTK 2022 Game Jam : Roll of the Dice", True, WHITE)
        gmtkTextRect = gmtkText.get_rect()
        gmtkTextRect.centerx = WIDTH / 2
        gmtkTextRect.centery = creditsEscapeRect.top - 25
        self.screen.blit(gmtkText, gmtkTextRect)

        # Jordan
        jordanIcon = self.jordanSpriteSheet.image_at(animationFrame, 0, -1)
        jordanIconRect = jordanIcon.get_rect()
        jordanIconRect.centerx = WIDTH / 6
        jordanIconRect.centery = HEIGHT / 3

        jordanName = self.pixelFont.render(
            "ItsSeraphii", True, WHITE)
        jordanNameRect = jordanName.get_rect()
        jordanNameRect.centerx = jordanIconRect.centerx
        jordanNameRect.centery = jordanIconRect.bottom + 25

        jordanBio = self.pixelFontSmall.render(
            "Assets, UI,", True, WHITE)
        jordanBioRect = jordanBio.get_rect()
        jordanBioRect.centerx = jordanNameRect.centerx
        jordanBioRect.centery = jordanNameRect.bottom + 25

        jordanBio2 = self.pixelFontSmall.render(
            "Concept art, Coding", True, WHITE)
        jordanBio2Rect = jordanBio2.get_rect()
        jordanBio2Rect.centerx = jordanBioRect.centerx
        jordanBio2Rect.centery = jordanBioRect.bottom + 25

        self.screen.blit(jordanIcon, jordanIconRect)
        self.screen.blit(jordanName, jordanNameRect)
        self.screen.blit(jordanBio, jordanBioRect)
        self.screen.blit(jordanBio2, jordanBio2Rect)

        # Nathan
        nathanIcon = self.nathanSpritesheet.image_at(animationFrame, 0, -1)
        nathanIconRect = nathanIcon.get_rect()
        nathanIconRect.centerx = WIDTH - WIDTH / 6
        nathanIconRect.centery = HEIGHT / 3

        nathanName = self.pixelFont.render(
            "Hypstersaurus", True, WHITE)
        nathanNameRect = nathanName.get_rect()
        nathanNameRect.centerx = nathanIconRect.centerx
        nathanNameRect.centery = nathanIconRect.bottom + 25

        nathanBio = self.pixelFontSmall.render(
            "Assets, Coding", True, WHITE)
        nathanBioRect = nathanBio.get_rect()
        nathanBioRect.centerx = nathanNameRect.centerx
        nathanBioRect.centery = nathanNameRect.bottom + 25

        self.screen.blit(nathanIcon, nathanIconRect)
        self.screen.blit(nathanName, nathanNameRect)
        self.screen.blit(nathanBio, nathanBioRect)

        # William
        williamIcon = self.williamSpritesheet.image_at(animationFrame, 0, -1)
        williamIconRect = williamIcon.get_rect()
        williamIconRect.centerx = WIDTH / 2
        williamIconRect.centery = HEIGHT / 3

        williamName = self.pixelFont.render(
            "Aggrobane", True, WHITE)
        williamNameRect = williamName.get_rect()
        williamNameRect.centerx = williamIconRect.centerx
        williamNameRect.centery = williamIconRect.bottom + 25

        williamBio = self.pixelFontSmall.render(
            "Coding, Software architecture", True, WHITE)
        williamBioRect = williamBio.get_rect()
        williamBioRect.centerx = williamNameRect.centerx
        williamBioRect.centery = williamNameRect.bottom + 25

        self.screen.blit(williamIcon, williamIconRect)
        self.screen.blit(williamName, williamNameRect)
        self.screen.blit(williamBio, williamBioRect)

        # Alex
        alexIcon = self.alexSpritesheet.image_at(animationFrame, 0, -1)
        alexIconRect = alexIcon.get_rect()
        alexIconRect.centerx = WIDTH / 3
        alexIconRect.centery = HEIGHT - HEIGHT / 3

        alexName = self.pixelFont.render(
            "DefinitelyNotAlex", True, WHITE)
        alexNameRect = alexName.get_rect()
        alexNameRect.centerx = alexIconRect.centerx
        alexNameRect.centery = alexIconRect.bottom + 25

        alexBio = self.pixelFontSmall.render(
            "Level design, Pattern coding", True, WHITE)
        alexBioRect = alexBio.get_rect()
        alexBioRect.centerx = alexNameRect.centerx
        alexBioRect.centery = alexNameRect.bottom + 25

        self.screen.blit(alexIcon, alexIconRect)
        self.screen.blit(alexName, alexNameRect)
        self.screen.blit(alexBio, alexBioRect)

        # Lambert
        lambertIcon = self.lambertSpritesheet.image_at(animationFrame, 0, -1)
        lambertIconRect = lambertIcon.get_rect()
        lambertIconRect.centerx = WIDTH - WIDTH / 3
        lambertIconRect.centery = HEIGHT - HEIGHT / 3

        lambertName = self.pixelFont.render(
            "Parazyte", True, WHITE)
        lambertNameRect = lambertName.get_rect()
        lambertNameRect.centerx = lambertIconRect.centerx
        lambertNameRect.centery = lambertIconRect.bottom + 25

        lambertBio = self.pixelFontSmall.render(
            "Level design, Music", True, WHITE)
        lambertBioRect = lambertBio.get_rect()
        lambertBioRect.centerx = lambertNameRect.centerx
        lambertBioRect.centery = lambertNameRect.bottom + 25

        self.screen.blit(lambertIcon, lambertIconRect)
        self.screen.blit(lambertName, lambertNameRect)
        self.screen.blit(lambertBio, lambertBioRect)

        pass
