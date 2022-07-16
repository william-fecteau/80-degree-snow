import queue
import pygame
from attack import Attack
import pygame_menu
from constants import BLACK, WIDTH, HEIGHT
from enemyMove import EnemyMove
from enemySpawn import EnemySpawn
from sprites import Player
from sprites.BackgroundObject import BackgroundObject
from sprites.enemy import Enemy
import numpy
import random
from sprites.enemyPrototype import EnemyPrototype
import json
import os

from states.payloads import InGameStatePayload

E_NEXT_SPAWN = pygame.USEREVENT + 5


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

    def __init__(self, game, num: int, screen: pygame.Surface, gameWorldSurf: pygame.surface, dicEnemyPrototypes: dict, dicEnemySpawns: dict) -> None:
        self.game = game
        self.num = num
        self.screen = screen
        self.dicEnemyPrototypes = dicEnemyPrototypes
        self.gameWorldSurf = gameWorldSurf
        self.dicEnemySpawns = dicEnemySpawns
        self.time = pygame.time.get_ticks()
        self.ui_font = pygame.font.Font(pygame_menu.font.FONT_MUNRO, 50)

        # Setting up groups
        self.playerProjectileGroup = pygame.sprite.Group()
        self.enemyProjectileGroup = pygame.sprite.Group()
        self.backgroundObjectsGroup = pygame.sprite.Group()
        self.backgroundTilesGroup = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        # Setting up player
        self.player = Player(self.playerProjectileGroup, self.enemyProjectileGroup,
                             self.gameWorldSurf.get_rect(), centerx=0, bottom=HEIGHT)

        # enemy = Enemy(dicEnemyPrototypes["shnake"], self.playerProjectileGroup, self.enemyProjectileGroup, topleft=(0, 0))
        # self.enemies.add(enemy)
        # self.enemyProjectileGroup.add(enemy)  # Enemy will count as a projectile cuz if it collides with player it will kill him

        for _ in range(self.CLOUDS):
            self.backgroundObjectsGroup.add(self.generateCloud(True))

        # Generate initial bg
        for i in range(self.NB_WIDTH_TILES):
            for j in range(int(HEIGHT/self.SIZE_TILE)+2):
                self.backgroundTilesGroup.add(BackgroundObject(self.BG, pygame.Vector2(
                    0, -2), self.SIZE_TILE, center=(WIDTH/4 - 25 + self.SIZE_TILE * i,  250 + self.SIZE_TILE * j)))
                self.NB_TOT_TILES += 1

        # Check for first enemy spawn
        self.nextSpawnTimeMs = list(self.dicEnemySpawns.keys())[0]
        if (self.nextSpawnTimeMs == 0):
            self.spawnEnemies()
        else:
            pygame.time.set_timer(E_NEXT_SPAWN, self.nextSpawnTimeMs)

    def spawnEnemies(self):
        for enemySpawn in self.dicEnemySpawns[self.nextSpawnTimeMs]:
            prototype = enemySpawn.enemyPrototype
            spawn = enemySpawn.spawnPosition
            enemy = Enemy(prototype, self.playerProjectileGroup,
                          self.enemyProjectileGroup, center=(spawn.x, spawn.y))
            self.enemies.add(enemy)
            self.enemyProjectileGroup.add(enemy)

        del self.dicEnemySpawns[self.nextSpawnTimeMs]

        if (len(self.dicEnemySpawns) > 0):
            self.nextSpawnTimeMs = list(self.dicEnemySpawns.keys())[0]
            pygame.time.set_timer(E_NEXT_SPAWN, self.nextSpawnTimeMs)
        else:
            pygame.time.set_timer(E_NEXT_SPAWN, 0)

    def generateCloud(self, randomY=False):
        # Pick a random sprite
        img = self.CLOUDSIMG[random.randint(0, len(self.CLOUDSIMG)-1)]
        # Pick a random size
        width = random.randint(int(WIDTH/10), int(WIDTH))
        # Pick a random X position
        randomX = random.randint(-int(width/2), WIDTH+int(width/2))
        # Pick a randon Y position or top of the screen
        Y = random.randint(
            0 - HEIGHT/2, HEIGHT) if randomY else 0 - img.get_height()
        # Pick a speed calculated by size of image
        speed = pygame.Vector2(0, -(width*2.5 / WIDTH)*10)
        return BackgroundObject(img, speed, width, center=(randomX,  Y))

    def update(self, game, events, keys) -> None:
        self.pollInput(events, keys)
        self.enemies.update(events=events, keys=keys)
        self.enemyProjectileGroup.update()
        self.playerProjectileGroup.update()
        self.player.update(events, keys)
        self.backgroundObjectsGroup.update()
        self.backgroundTilesGroup.update()
        if(len(self.backgroundObjectsGroup.sprites()) < self.CLOUDS):
            self.backgroundObjectsGroup.add(self.generateCloud())
        if(len(self.backgroundTilesGroup.sprites()) < self.NB_TOT_TILES):
            for i in range(self.NB_WIDTH_TILES):
                self.backgroundTilesGroup.add(
                    BackgroundObject(self.BG, pygame.Vector2(
                        0, -2), self.SIZE_TILE, center=(WIDTH/4 - 25 + self.SIZE_TILE * i, self.SIZE_TILE))
                )

        if not self.player.isAlive:
            game.switchState("MenuState")

        # Spawn enemies
        for event in events:
            if event.type == E_NEXT_SPAWN:
                self.spawnEnemies()
                break

    def draw(self) -> None:
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
        for event in events:
            if event.type == pygame.KEYUP and event.key == pygame.K_r:
                self.game.switchState(
                    "InGameState", InGameStatePayload(self.num))

    def drawUI(self) -> None:
        # Draw left UI rectangle
        pygame.draw.rect(self.screen, BLACK, (0, 0, WIDTH/4, HEIGHT))
        # Draw right UI rectangle
        pygame.draw.rect(self.screen, BLACK,
                         (WIDTH/4 * 3, 0, WIDTH/4, HEIGHT))

        # Draw time
        time = numpy.floor(
            (pygame.time.get_ticks() - self.time) / 1000)  # in seconds
        self.screen.blit(self.ui_font.render("Time : " + str(time),
                                             True, (255, 255, 255)), (50, 0))


def loadLevel(game, screen: pygame.Surface, levelNum: int) -> Level:
    worldWidth = WIDTH / 2
    worldHeight = HEIGHT
    gameWorldSurf = pygame.Surface((worldWidth, worldHeight))

    # Loading images
    dicImages = {}
    with open('res/enemies/images.json', 'r') as file:
        data = json.load(file)
        for key in data.keys():
            dicImages[key] = pygame.image.load(data[key])

    # Loading prototypes
    dicEnemyPrototypes = {}
    directory = 'res/enemies/prototypes'
    for filename in os.listdir(directory):
        filePath = os.path.join(directory, filename)
        with open(filePath, 'r') as file:
            prototypeData = json.load(file)

            # Load attack
            attack = prototypeData['attack']
            projectileImgName = attack['projectileImage']
            attackObj = Attack(dicImages[projectileImgName], attack['nbProjectiles'], attack['projectileSpeed'],
                               attack['rotateSpeedRad'], attack['initialRotationRad'], attack['shotCooldownMs'])

            # Load moves
            moves = prototypeData['moves']
            movesObj = []
            for move in moves:
                dest = move['dest']
                enemyMove = EnemyMove(dest[0], dest[1], move['durationSec'])
                movesObj.append(enemyMove)

            # Load prototype
            imageName = prototypeData['image']
            prototypeObj = EnemyPrototype(
                dicImages[imageName], prototypeData['health'], attackObj, movesObj)

            prototypeName = prototypeData['name']
            dicEnemyPrototypes[prototypeName] = prototypeObj

    # Loading enemy spawns
    dicEnemySpawns = {}
    with open(f'res/enemies/levels/{levelNum}.json') as file:
        spawnData = json.load(file)
        for spawn in spawnData:
            enemies = spawn['enemies']
            lstEnemiesSpawn = []
            for enemy in enemies:
                prototypeToSpawn = enemy['prototypeName']
                enemySpawn = EnemySpawn(
                    dicEnemyPrototypes[prototypeToSpawn], pygame.Vector2(enemy['spawnPosition']))
                lstEnemiesSpawn.append(enemySpawn)

            dicEnemySpawns[spawn['timeToSpawnMs']] = lstEnemiesSpawn

    return Level(game, levelNum, screen, gameWorldSurf, dicEnemyPrototypes, dicEnemySpawns)
