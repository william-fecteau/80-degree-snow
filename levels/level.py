import pygame
from attack import Attack
from constants import TARGET_FPS, WIDTH, HEIGHT
from enemyMove import EnemyMove
from sprites import Player
from sprites.BackgroundObject import BackgroundObject
from sprites.enemy import Enemy
import numpy
import random
from sprites.enemyPrototype import EnemyPrototype

class Level:
    CLOUDS = 25
    CLOUDSIMG = [
        pygame.image.load("res/cloud-1.png"),
        pygame.image.load("res/cloud-2.png"),
        pygame.image.load("res/cloud-3.png"),
        pygame.image.load("res/cloud-4.png"),
        pygame.image.load("res/cloud-5.png"),
    ]

    BG = pygame.image.load("res/sea-2.jpg")
    NB_TOT_TILES = 0
    NB_WIDTH_TILES = 4
    SIZE_TILE = WIDTH/(2*NB_WIDTH_TILES)
    LOADING_TILES = False

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
        self.backgroundTilesGroup = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        # Prototypes
        basicAttack = Attack(projectileImg, 4, 5, numpy.pi/4, 0)
        moveSet = [EnemyMove(self.gameWorldSurf.get_width(), self.gameWorldSurf.get_height(), 5),
                   EnemyMove(0, self.gameWorldSurf.get_height(), 10),
                   EnemyMove(self.gameWorldSurf.get_width(), 0, 10)]
        schnakePrototype = EnemyPrototype(schnakeImg, 10, basicAttack, moveSet, self.playerProjectileGroup, self.enemyProjectileGroup)

        # Setting up player
        self.player = Player(playerImg, self.playerProjectileGroup, self.enemyProjectileGroup, self.gameWorldSurf.get_rect(), centerx=0, bottom=HEIGHT)

        enemy = Enemy(schnakePrototype, topleft=(0, 0))
        self.enemies.add(enemy)
        self.enemyProjectileGroup.add(enemy)  # Enemy will count as a projectile cuz if it collides with player it will kill him
        
        # # Generating some ennemies
        # for _ in range(5):
        #     randomX = random.randint(schnakeImg.get_width(), self.gameWorldSurf.get_width() - schnakeImg.get_width())
        #     randomY = random.randint(schnakeImg.get_height(), self.gameWorldSurf.get_height() - schnakeImg.get_height() - self.player.image.get_height())
        #     enemy = Enemy(schnakePrototype, center=(randomX, randomY))

        for _ in range(self.CLOUDS):
            self.backgroundObjectsGroup.add(self.generateCloud(True))

        # Generate initial bg
        for i in range(self.NB_WIDTH_TILES):
            for j in range(int(HEIGHT/self.SIZE_TILE)+2):
                self.backgroundTilesGroup.add(BackgroundObject(self.BG, pygame.Vector2(0, -2), self.SIZE_TILE, center=(WIDTH/4 - 25 + self.SIZE_TILE * i,  250 + self.SIZE_TILE * j)))
                self.NB_TOT_TILES += 1

    def generateCloud(self, randomY = False):
            img = self.CLOUDSIMG[random.randint(0, len(self.CLOUDSIMG)-1)]                  # Pick a random sprite
            width = random.randint(int(WIDTH/10), int(WIDTH))                               # Pick a random size 
            randomX = random.randint(-int(width/2), WIDTH+int(width/2))                     # Pick a random X position
            Y = random.randint(0 - HEIGHT/2, HEIGHT) if randomY else 0 - img.get_height()   # Pick a randon Y position or top of the screen
            speed =  pygame.Vector2(0, -(width*2.5 / WIDTH)*10)                             # Pick a speed calculated by size of image
            return BackgroundObject(img, speed, width, center=(randomX,  Y))
        
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
            print(self.NB_TOT_TILES)
            for i in range(self.NB_WIDTH_TILES):
                self.backgroundTilesGroup.add(
                    BackgroundObject(self.BG, pygame.Vector2(0, -2), self.SIZE_TILE, center=(WIDTH/4 - 25 + self.SIZE_TILE * i, self.SIZE_TILE))
                )

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
