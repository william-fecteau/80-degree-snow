import pygame
from constants import WIDTH, HEIGHT
from sprites import Player
from sprites.enemy import Enemy
import numpy
import random


class Level:
    def __init__(self, num: int, screen: pygame.Surface, background: pygame.Surface) -> None:
        self.num = num
        self.screen = screen
        self.gameWorldSurf = pygame.Surface((WIDTH/2, HEIGHT))
        self.background = background

        # Loading images
        playerImg = pygame.image.load("res/player.png")
        schnakeImg = pygame.image.load("res/shnake.png")

        # Setting up groups
        self.playerProjectileGroup = pygame.sprite.Group()
        self.enemyProjectileGroup = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        # Setting up player
        self.player = Player(playerImg, self.playerProjectileGroup, self.enemyProjectileGroup, self.gameWorldSurf.get_rect(), centerx=WIDTH / 2, bottom=HEIGHT)

        # Generating some ennemies
        for _ in range(5):
            randomX = random.randint(schnakeImg.get_width(), self.gameWorldSurf.get_width() - schnakeImg.get_width())
            randomY = random.randint(schnakeImg.get_height(), self.gameWorldSurf.get_height() - schnakeImg.get_height() - self.player.image.get_height())
            enemy = Enemy(schnakeImg, 5, self.playerProjectileGroup, self.enemyProjectileGroup, center=(randomX, randomY))

            self.enemies.add(enemy)
            self.enemyProjectileGroup.add(enemy)  # Enemy will count as a projectile cuz if it collides with player it will kill him


    def update(self, game, events, keys) -> None:
        self.pollInput(events, keys)
        self.enemies.update()
        self.enemyProjectileGroup.update()
        self.playerProjectileGroup.update()
        self.player.update(events, keys)

        if not self.player.isAlive:
            game.switchState("MenuState")


    def draw(self) -> None:
        self.gameWorldSurf.blit(self.background, (0, 0))

        # Enemies
        for sprite in self.enemies.sprites():
            self.gameWorldSurf.blit(sprite.image, sprite.rect)

        # Player projectiles
        for sprite in self.playerProjectileGroup.sprites():
            self.gameWorldSurf.blit(sprite.image, sprite.rect)

        # Enemy projectiles
        for sprite in self.enemyProjectileGroup.sprites():
            self.gameWorldSurf.blit(sprite.image, sprite.rect)

        # Player
        self.gameWorldSurf.blit(self.player.image, self.player.rect)

        self.screen.blit(self.gameWorldSurf, (WIDTH/4, 0))

        self.drawUI()


    def pollInput(self, events, keys) -> None:
        pass


    def drawUI(self) -> None:
        # Draw left UI rectangle
        pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, WIDTH/4, HEIGHT))
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (WIDTH/4 * 3, 0, WIDTH/4, HEIGHT))


def loadLevel(screen: pygame.Surface, levelNum: int) -> Level:
    background = pygame.image.load(f"res/{levelNum}.png")
    level = Level(levelNum, screen, background)
    return level
