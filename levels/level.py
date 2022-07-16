import pygame
from attack import Attack
from constants import WIDTH, HEIGHT
from sprites import Player
from sprites.BackgroundObject import BackgroundObject
from sprites.enemy import Enemy
import numpy
import random
from sprites.enemyPrototype import EnemyPrototype

CLOUDS = 25
CLOUDSIMG = [
    pygame.image.load("res/cloud-1.png"),
    pygame.image.load("res/cloud-2.png"),
    pygame.image.load("res/cloud-3.png"),
]

class Level:
    def __init__(self, num: int, screen: pygame.Surface, background: pygame.Surface) -> None:
        self.num = num
        self.screen = screen
        self.gameWorldSurf = pygame.Surface((WIDTH/2, HEIGHT))
        self.background = background

        # Loading images
        playerImg = pygame.image.load("res/player.png")
        schnakeImg = pygame.image.load("res/shnake.png")
        projectileImg = pygame.image.load("res/intro_ball.gif")


        # Setting up groups
        self.playerProjectileGroup = pygame.sprite.Group()
        self.enemyProjectileGroup = pygame.sprite.Group()
        self.backgroundObjectsGroup = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        # Prototypes
        basicAttack = Attack(projectileImg, 4, 5, numpy.pi/4, 0)
        schnakePrototype = EnemyPrototype(schnakeImg, 10, basicAttack, self.playerProjectileGroup, self.enemyProjectileGroup)

        # Setting up player
        self.player = Player(playerImg, self.playerProjectileGroup, self.enemyProjectileGroup, self.gameWorldSurf.get_rect(), centerx=WIDTH / 2, bottom=HEIGHT)

        # Generating some ennemies
        for _ in range(5):
            randomX = random.randint(schnakeImg.get_width(), self.gameWorldSurf.get_width() - schnakeImg.get_width())
            randomY = random.randint(schnakeImg.get_height(), self.gameWorldSurf.get_height() - schnakeImg.get_height() - self.player.image.get_height())
            enemy = Enemy(schnakePrototype, center=(randomX, randomY))

            self.enemies.add(enemy)
            self.enemyProjectileGroup.add(enemy) # Enemy will count as a projectile cuz if it collides with player it will kill him
        
        for _ in range(CLOUDS):
            self.backgroundObjectsGroup.add(self.generateCloud(True))

    def generateCloud(self, randomY = False):
            img = CLOUDSIMG[random.randint(0, len(CLOUDSIMG)-1)]
            width = random.randint(int(WIDTH/10), int(WIDTH))
            randomX = random.randint(-int(width/2), WIDTH+int(width/2))
            Y = random.randint(0 - HEIGHT/2, HEIGHT) if randomY else 0 - img.get_height()
            speed =  pygame.Vector2(0, -(width*2.5 / WIDTH)*10)
            return BackgroundObject(img, speed, width, center=(randomX,  Y))
        
    def update(self, game, events, keys) -> None:
        self.pollInput(events, keys)
        self.enemies.update()
        self.enemyProjectileGroup.update()
        self.playerProjectileGroup.update()
        self.player.update(events, keys)
        self.backgroundObjectsGroup.update()
        if(len(self.backgroundObjectsGroup.sprites()) < CLOUDS): self.backgroundObjectsGroup.add(self.generateCloud())

        if not self.player.isAlive:
            game.switchState("MenuState")


    def draw(self) -> None:
        self.gameWorldSurf.blit(self.background, (0, 0))

        # Background elems
        for sprite in self.backgroundObjectsGroup.sprites():
            self.gameWorldSurf.blit(sprite.image, sprite.rect)

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
