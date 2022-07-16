from math import ceil
import pygame
from attack import Attack
from constants import WIDTH, HEIGHT
from sprites import Player
from sprites.BackgroundObject import BackgroundObject
from sprites.enemy import Enemy
import numpy
import random
from sprites.enemyPrototype import EnemyPrototype

class Level:
    CLOUDS = 20
    CLOUDSIMG = [
        pygame.image.load("res/cloud-1.png"),
        pygame.image.load("res/cloud-2.png"),
        pygame.image.load("res/cloud-3.png"),
        pygame.image.load("res/cloud-4.png"),
        pygame.image.load("res/cloud-5.png"),
    ]

    BG = pygame.image.load("res/sea-2.jpg")
    NB_HEIGHT_TILES = 4 # note: must be higher than 1
    SIZE_TILE = int(HEIGHT/(NB_HEIGHT_TILES-1))
    NB_WIDTH_TILES = ceil(WIDTH/(2*SIZE_TILE))
    NB_TOT_TILES = NB_WIDTH_TILES * NB_HEIGHT_TILES
    LOADING_TILES = False
    BG_SPEED = 1
    OFFSET = 2 # tweek if you see gaps in the textures (this shit is black magic)

    def __init__(self, num: int, screen: pygame.Surface, background: pygame.Surface) -> None:
        self.num = num
        self.screen = screen
        self.gameWorldSurf = pygame.Surface((WIDTH/2, HEIGHT))
        self.background = self.BG

        # Loading images
        playerImg = pygame.image.load("res/player.png")
        schnakeImg = pygame.image.load("res/shnake.png")
        projectileImg = pygame.image.load("res/intro_ball.gif")


        # Setting up groups
        self.playerProjectileGroup = pygame.sprite.Group()
        self.enemyProjectileGroup = pygame.sprite.Group()
        self.backgroundObjectsGroup = pygame.sprite.Group()
        self.backgroundTilesGroup = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        # Prototypes
        basicAttack = Attack(projectileImg, 4, 5, numpy.pi/4, 0)
        schnakePrototype = EnemyPrototype(schnakeImg, 10, basicAttack, self.playerProjectileGroup, self.enemyProjectileGroup)

        # Setting up player
        self.player = Player(playerImg, self.playerProjectileGroup, self.enemyProjectileGroup, self.gameWorldSurf.get_rect(), centerx=WIDTH / 2, bottom=HEIGHT)

        # Generating some ennemies
        for _ in range(0):
            randomX = random.randint(schnakeImg.get_width(), self.gameWorldSurf.get_width() - schnakeImg.get_width())
            randomY = random.randint(schnakeImg.get_height(), self.gameWorldSurf.get_height() - schnakeImg.get_height() - self.player.image.get_height())
            enemy = Enemy(schnakePrototype, center=(randomX, randomY))

            self.enemies.add(enemy)
            self.enemyProjectileGroup.add(enemy) # Enemy will count as a projectile cuz if it collides with player it will kill him
        
        # Generate initial clouds
        for _ in range(self.CLOUDS):
            self.backgroundObjectsGroup.add(self.generateCloud(True))

        # Generate initial bg
        for i in range(self.NB_WIDTH_TILES):
            for j in range(self.NB_HEIGHT_TILES):
                #print(int(WIDTH/4 + self.SIZE_TILE * i), int(self.SIZE_TILE * j))
                self.backgroundTilesGroup.add(
                    BackgroundObject(self.BG, pygame.Vector2(0, -self.BG_SPEED), self.SIZE_TILE, topleft=(self.SIZE_TILE * i, self.SIZE_TILE *j))
                )
                # print("BG: " +  str(int(self.SIZE_TILE * i)) +", " + str(self.SIZE_TILE * (j-1)))

    def generateCloud(self, randomY = False):
            img = self.CLOUDSIMG[random.randint(0, len(self.CLOUDSIMG)-1)]                  # Pick a random sprite
            width = random.randint(int(WIDTH/10), int(WIDTH))                               # Pick a random size 
            randomX = random.randint(-int(width/2), WIDTH+int(width/2))                     # Pick a random X position
            Y = random.randint(0 - HEIGHT/2, HEIGHT) if randomY else -img.get_height()*1.75   # Pick a randon Y position or top of the screen
            speed =  pygame.Vector2(0, -(width*2.5 / WIDTH)*12)                             # Pick a speed calculated by size of image
            return BackgroundObject(img, speed, width, topleft=(randomX,  Y))
        
    def update(self, game, events, keys) -> None:
        self.pollInput(events, keys)
        self.enemies.update()
        self.enemyProjectileGroup.update()
        self.playerProjectileGroup.update()
        self.player.update(events, keys)
        self.backgroundObjectsGroup.update()
        self.backgroundTilesGroup.update()
        if(len(self.backgroundObjectsGroup.sprites()) < self.CLOUDS): self.backgroundObjectsGroup.add(self.generateCloud())
        if(len(self.backgroundTilesGroup.sprites()) < self.NB_TOT_TILES):
            # print(self.NB_TOT_TILES)
            # print(len(self.backgroundTilesGroup.sprites()))
            for i in range(self.NB_WIDTH_TILES):
                self.backgroundTilesGroup.add(
                    BackgroundObject(self.BG, pygame.Vector2(0, -self.BG_SPEED), self.SIZE_TILE, topleft=(self.SIZE_TILE * i, self.OFFSET-self.SIZE_TILE))
                )
                # print("BG: " +  str(int(self.SIZE_TILE * i)) +", " + str(-self.SIZE_TILE))


        if not self.player.isAlive:
            game.switchState("MenuState")


    def draw(self) -> None:
        self.gameWorldSurf.blit(self.background, (0, 0))

        # Background tiles
        for sprite in self.backgroundTilesGroup.sprites():
            self.gameWorldSurf.blit(sprite.image, sprite.rect)

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
