import math
import queue
from ui import UI
from math import ceil
import pygame
from attack import Attack
import pygame_menu
from constants import BLACK, WIDTH, HEIGHT, HEATWAVE_INTERVAL_SEC
from enemyMove import EnemyMove
from enemySpawn import EnemySpawn
from sprites import Player
from sprites import enemyPrototype
from sprites.BackgroundObject import BackgroundObject
from sprites.enemy import Enemy
import numpy
import random
from sprites.enemyPrototype import EnemyPrototype
import jstyleson
import os

from states.payloads import InGameStatePayload

E_NEXT_SPAWN = pygame.USEREVENT + 5
E_HEATWAVE = pygame.USEREVENT + 6
E_INVINCIBILITY_FRAME = pygame.USEREVENT + 7
E_INVINCIBILITY_FLASH = pygame.USEREVENT + 8
E_END_LEVEL = pygame.USEREVENT + 9

INVINCIBLE_TIME_MS = 2000
INVINCIBLE_FLASH_MS = 100

class Level:
    MAX_FROST = 10

    def __init__(self, game, num: int, screen: pygame.Surface, gameWorldSurf: pygame.surface, dicEnemyPrototypes: dict, dicEnemySpawns: dict, levelEndMs: int) -> None:
        self.game = game
        self.num = num
        self.screen = screen
        self.dicEnemyPrototypes = dicEnemyPrototypes
        self.gameWorldSurf = gameWorldSurf
        self.dicEnemySpawns = dicEnemySpawns
        self.frostLevel = self.MAX_FROST/2

        # Setting up groups
        self.playerProjectileGroup = pygame.sprite.Group()
        self.enemyProjectileGroup = pygame.sprite.Group()
        self.backgroundObjectsGroup = pygame.sprite.Group()
        self.backgroundTilesGroup = pygame.sprite.Group()
        self.iceCubes = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        # Setting up player
        self.player = Player(self.playerProjectileGroup, self.enemyProjectileGroup,
                             self.gameWorldSurf, centerx=self.gameWorldSurf.get_width() / 2, bottom=HEIGHT)
        self.drawPlayer = True

        # enemy = Enemy(dicEnemyPrototypes["shnake"], self.playerProjectileGroup, self.enemyProjectileGroup, topleft=(0, 0))
        # self.enemies.add(enemy)
        # self.enemyProjectileGroup.add(enemy)  # Enemy will count as a projectile cuz if it collides with player it will kill him

        self.playerInvincible = False

        # Check for first enemy spawn
        self.nextSpawnTimeMs = list(self.dicEnemySpawns.keys())[0]
        if (self.nextSpawnTimeMs == 0):
            self.spawnEnemies()
        else:
            pygame.time.set_timer(E_NEXT_SPAWN, self.nextSpawnTimeMs)

        # Setup UI
        self.ui = UI()

        # Heatwave setup
        self.diceCount = self.num if self.num <= 3 else 3
        self.nextHeatWave = [0 for _ in range(self.diceCount)]
        pygame.time.set_timer(E_HEATWAVE, HEATWAVE_INTERVAL_SEC * 1000)
        self.lastHeatwaveTime = pygame.time.get_ticks()

        # End level timer
        pygame.time.set_timer(E_END_LEVEL, levelEndMs)


    def spawnEnemies(self):
        for enemySpawn in self.dicEnemySpawns[self.nextSpawnTimeMs]:
            prototype = enemySpawn.enemyPrototype
            spawn = enemySpawn.spawnPosition
            width = prototype.width if(hasattr(prototype, "width")) else None
            enemy = Enemy(self.gameWorldSurf, prototype, self.playerProjectileGroup,
                          self.enemyProjectileGroup, self.iceCubes, center=(spawn.x, spawn.y), width=width)
            self.enemies.add(enemy)
            self.enemyProjectileGroup.add(enemy)

        del self.dicEnemySpawns[self.nextSpawnTimeMs]

        if (len(self.dicEnemySpawns) > 0):
            oldSpawn = self.nextSpawnTimeMs
            self.nextSpawnTimeMs = list(self.dicEnemySpawns.keys())[0]
            pygame.time.set_timer(
                E_NEXT_SPAWN, self.nextSpawnTimeMs - oldSpawn)
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
            0 - HEIGHT/2, HEIGHT) if randomY else -img.get_height()*1.75
        # Pick a speed calculated by size of image
        speed = pygame.Vector2(0, self.BG_SPEED + (width*2.5 / WIDTH) * self.CLOUD_SPEED)
        return BackgroundObject(img, speed, width, topleft=(randomX,  Y))

    def rollDices(self, diceCount: int):
        for i in range(diceCount):
            self.nextHeatWave[i] = random.randint(1, 6)

        self.lastHeatwaveTime = pygame.time.get_ticks()

    def applyHeatwave(self):

        # If its the first heatwave, just roll dice
        if self.nextHeatWave[0] == 0:
            self.rollDices(self.diceCount)
            return

        frostLeft = self.frostLevel - sum(self.nextHeatWave)

        if (frostLeft <= 0):
            # ur dead lol remove a life here
            self.player.die()
            pass
        else:
            self.frostLevel = frostLeft

        self.rollDices(self.diceCount)  # Roll dices for next heatwave

    def update(self, game, events, keys) -> None:
        self.pollInput(events, keys)
        self.enemies.update(events=events, keys=keys)
        self.iceCubes.update()
        self.enemyProjectileGroup.update()
        self.playerProjectileGroup.update()
        self.player.update(events, keys, self.frostLevel)
        self.backgroundObjectsGroup.update()
        self.backgroundTilesGroup.update()


        # Check if player collects ice cube
        for iceCube in self.iceCubes:
            if self.player.rect.colliderect(iceCube.rect):
                self.addFrost(iceCube.nbIce)
                iceCube.kill()
                break

        if(len(self.backgroundObjectsGroup.sprites()) < self.CLOUDS):
            self.backgroundObjectsGroup.add(self.generateCloud())
        if(len(self.backgroundTilesGroup.sprites()) < self.NB_TOT_TILES):
            for i in range(self.NB_WIDTH_TILES):
                self.backgroundTilesGroup.add(
                    BackgroundObject(self.BG, pygame.Vector2(
                        0, self.BG_SPEED), self.SIZE_TILE, topleft=(self.SIZE_TILE * i, self.OFFSET-self.SIZE_TILE))
                )

        if not self.player.isAlive and not self.playerInvincible:
            self.playerInvincible = True
            
            if self.player.lives <= 0:
                self.game.switchState("InGameState", InGameStatePayload(self.num))

            # Frost loss, reset frost to 5
            if self.frostLevel <= 0:
                pygame.time.set_timer(E_HEATWAVE, 0)
                pygame.time.set_timer(E_HEATWAVE, HEATWAVE_INTERVAL_SEC * 1000)
                self.frostLevel = 5 
            
            pygame.time.set_timer(E_INVINCIBILITY_FRAME, INVINCIBLE_TIME_MS)
            pygame.time.set_timer(E_INVINCIBILITY_FLASH, INVINCIBLE_FLASH_MS)

        # Spawn enemies
        for event in events:
            if event.type == E_NEXT_SPAWN:
                self.spawnEnemies()
            elif event.type == E_HEATWAVE:
                self.applyHeatwave()
            elif event.type == E_INVINCIBILITY_FLASH:
                self.drawPlayer = not self.drawPlayer
            elif event.type == E_INVINCIBILITY_FRAME:
                self.player.isAlive = True
                self.playerInvincible = False
                self.drawPlayer = True
                pygame.time.set_timer(E_INVINCIBILITY_FRAME, 0)
                pygame.time.set_timer(E_INVINCIBILITY_FLASH, 0)
            elif event.type == E_END_LEVEL:
                self.game.switchState(
                    "InGameState", InGameStatePayload(self.num + 1))


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

        # Ice cubes
        for sprite in self.iceCubes.sprites():
            self.gameWorldSurf.blit(sprite.image, sprite.rect)

        # Enemy projectiles
        for sprite in self.enemyProjectileGroup.sprites():
            self.gameWorldSurf.blit(sprite.image, sprite.rect)

        # Player
        if self.drawPlayer:
            self.gameWorldSurf.blit(self.player.image, self.player.rect)

        pygame.draw.rect(self.gameWorldSurf, "red", self.player.hitbox, 1)

        self.screen.blit(self.gameWorldSurf, (WIDTH/4, 0))

        self.ui.draw(self.screen, self.frostLevel,
                     self.nextHeatWave, self.lastHeatwaveTime, self.player.lives)

    def pollInput(self, events, keys) -> None:
        for event in events:
            if event.type == pygame.KEYUP and event.key == pygame.K_r:
                self.game.switchState(
                    "InGameState", InGameStatePayload(self.num))


    def addFrost(self, amount: int) -> None:
        if self.frostLevel + amount <= self.MAX_FROST:
            self.frostLevel += amount
        else:
            overFrost = self.frostLevel + amount - self.MAX_FROST
            self.frostLevel = self.MAX_FROST
            # Lower the dice value function by overfrost
            self.overFrostDice(overFrost)

    def overFrostDice(self, overFrost: int) -> None:
        # Get last dice thats not 0
        lastDiceIndex = self.diceCount - 1
        while lastDiceIndex >= 0 and self.nextHeatWave[lastDiceIndex] == 0:
            lastDiceIndex -= 1

        if (lastDiceIndex >= 0):
            newDiceValue = self.nextHeatWave[lastDiceIndex] - overFrost

            if (newDiceValue < 0):
                overFrost -= self.nextHeatWave[lastDiceIndex]
                self.nextHeatWave[lastDiceIndex] = 0
                self.overFrostDice(overFrost)
            else:
                self.nextHeatWave[lastDiceIndex] = int(newDiceValue)

        # If there are no dices left, just return
        pass


def loadLevel(game, screen: pygame.Surface, levelNum: int) -> Level:
    worldWidth = WIDTH / 2
    worldHeight = HEIGHT
    gameWorldSurf = pygame.Surface((worldWidth, worldHeight))

    # Loading images
    dicImages = {}
    with open('res/enemies/images.json', 'r') as file:
        data = jstyleson.loads(file.read())
        for key in data.keys():
            dicImages[key] = pygame.image.load(data[key])

    # Loading prototypes
    dicEnemyPrototypes = {}
    directory = 'res/enemies/prototypes'
    for filename in os.listdir(directory):
        filePath = os.path.join(directory, filename)
        with open(filePath, 'r') as file:
            prototypeData = jstyleson.loads(file.read())

            # Load attack
            attack = prototypeData['attack']
            projectileImgName = attack['projectileImage']
            radianRotate = math.radians(attack['initialRotationDeg'])
            radianInitialRotation = math.radians(attack['rotateSpeedDeg'])
            attackObj = Attack(dicImages[projectileImgName], attack['nbProjectiles'],
                               attack['projectileSpeed'], radianInitialRotation, radianRotate, attack['shotCooldownMs'])

            # Load moves
            moves = prototypeData['moves']
            movesObj = []
            for move in moves:
                delta = move['delta']
                enemyMove = EnemyMove(
                    pygame.Vector2(delta), move['durationSec'])
                movesObj.append(enemyMove)

            # Load prototype
            imageName = prototypeData['image']
            iceDrop = prototypeData['iceDrop'] if 'iceDrop' in prototypeData else 1
            width = prototypeData['width'] if 'width' in prototypeData else None
            prototypeObj = EnemyPrototype(
                dicImages[imageName], prototypeData['health'], attackObj, movesObj, iceDrop, width)

            prototypeName = prototypeData['name']
            dicEnemyPrototypes[prototypeName] = prototypeObj

    # Loading enemy spawns
    dicEnemySpawns = {}
    endTimeMs = None
    with open(f'res/levels/{levelNum}.json') as file:
        levelData = jstyleson.loads(file.read())
        endTimeMs = levelData['endTimeMs']

        for spawn in levelData['spawns']:
            enemies = spawn['enemies']
            lstEnemiesSpawn = []
            for enemy in enemies:
                prototypeToSpawn = enemy['prototypeName']

                enemySpawn = EnemySpawn(
                    dicEnemyPrototypes[prototypeToSpawn], pygame.Vector2(enemy['spawnPosition']))
                lstEnemiesSpawn.append(enemySpawn)

            dicEnemySpawns[spawn['timeToSpawnMs']] = lstEnemiesSpawn

    level = Level(game, levelNum, screen, gameWorldSurf, dicEnemyPrototypes, dicEnemySpawns, endTimeMs)

    with open(f'res/levels/{levelNum}.json') as file:
        levelData = jstyleson.loads(file.read())

        # Load Bg elems
        level.CLOUDS = levelData["bgOptions"]["CLOUDS"]
        level.CLOUD_SPEED = levelData["bgOptions"]["CLOUD_SPEED"]
        level.NB_HEIGHT_TILES = levelData["bgOptions"]["NB_HEIGHT_TILES"]     # note: must be higher than 1
        level.BG_SPEED = levelData["bgOptions"]["BG_SPEED"]
        level.OFFSET = levelData["bgOptions"]["OFFSET"]                      # tweek if you see gaps in the textures (this shit is black magic)
        level.BG = pygame.image.load(levelData["bgOptions"]["img_location"],)
        level.CLOUD_TYPE = levelData["bgOptions"]["CLOUD_TYPE"] if "CLOUD_TYPE" in levelData["bgOptions"] else "normal"
        level.SIZE_TILE = int(HEIGHT/(level.NB_HEIGHT_TILES-1))
        level.NB_WIDTH_TILES = ceil(WIDTH/(2*level.SIZE_TILE))
        level.NB_TOT_TILES = level.NB_WIDTH_TILES * level.NB_HEIGHT_TILES

        level.background = level.BG
        if level.CLOUD_TYPE == "sunset":
            level.CLOUDSIMG = [
                pygame.image.load("res/cloud-1-set.png"),
            ]
        else:
            level.CLOUDSIMG = [
                pygame.image.load("res/cloud-1.png"),
                pygame.image.load("res/cloud-2.png"),
                pygame.image.load("res/cloud-3.png"),
                pygame.image.load("res/cloud-4.png"),
                pygame.image.load("res/cloud-5.png"),
            ]

        # Generate initial clouds
        for _ in range(level.CLOUDS):
            level.backgroundObjectsGroup.add(level.generateCloud(True))

        # Generate initial bg
        for i in range(level.NB_WIDTH_TILES):
            for j in range(level.NB_HEIGHT_TILES):
                level.backgroundTilesGroup.add(
                    BackgroundObject(level.BG, pygame.Vector2(
                        0, level.BG_SPEED), level.SIZE_TILE, topleft=(level.SIZE_TILE * i, level.SIZE_TILE * j))
                )
    
    return level
