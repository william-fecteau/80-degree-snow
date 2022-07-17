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
from utils import resource_path

E_NEXT_SPAWN = pygame.USEREVENT + 5
E_HEATWAVE = pygame.USEREVENT + 6
E_END_LEVEL = pygame.USEREVENT + 9
E_NEXT_TUTORIAL_PHASE = pygame.USEREVENT + 10
E_NEXT_TUTORIAL_STEP = pygame.USEREVENT + 11

INVINCIBILITY_FLASH = 300
INVINCIBILITY_TIME = 2000


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
        self.framesHeld = 0

        self.tutorialStep = -1
        self.tutorialPhase = 0 if num == 0 else 999
        # 0 - wasd + space
        # 1 - frost-o-meter
        # 2 - Dice and heatwave
        # 3 - Ice cubes

        # Setup sounds
        self.icePickup = pygame.mixer.Sound(resource_path("res/pickup.mp3"))
        self.diceRoll = pygame.mixer.Sound(resource_path("res/diceroll1.mp3"))
        self.levelEnd = pygame.mixer.Sound(resource_path("res/levelEnd.mp3"))
        self.dieScrub = pygame.mixer.Sound(resource_path("res/explosion1.mp3"))

        # Death anims
        self.deathAnims = [
            pygame.image.load(resource_path('res/explosion-1.png')),
            pygame.image.load(resource_path('res/explosion-2.png')),
            pygame.image.load(resource_path('res/explosion-3.png')),
            pygame.image.load(resource_path('res/explosion-4.png')),
        ]

        # Sound volumes
        pygame.mixer.Sound.set_volume(self.diceRoll, 0.5)

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

        self.invincibilityFrameStart = None

        if self.num > 0:  # No enemy to spawn on tutorial
            # Check for first enemy spawn
            self.nextSpawnTimeMs = list(self.dicEnemySpawns.keys())[0]
            if (self.nextSpawnTimeMs == 0):
                self.spawnEnemies()
            else:
                pygame.time.set_timer(E_NEXT_SPAWN, self.nextSpawnTimeMs)

        # Setup UI
        self.ui = UI()

        # Heatwave setup
        if self.num == 0:  # Dont start heatwave on start of tutorial
            self.diceCount = 1
            self.nextHeatWave = [0]
            self.lastHeatwaveTime = 9999999
        else: 
            self.diceCount = self.num if self.num <= 3 else 3
            self.nextHeatWave = [0 for _ in range(self.diceCount)]
            pygame.time.set_timer(E_HEATWAVE, HEATWAVE_INTERVAL_SEC * 1000)

            self.lastHeatwaveTime = pygame.time.get_ticks()

        # End level timer
        pygame.time.set_timer(E_END_LEVEL, levelEndMs)

    def spawnEnemies(self):
        if self.num != 0:
            for enemySpawn in self.dicEnemySpawns[self.nextSpawnTimeMs]:
                prototype = enemySpawn.enemyPrototype
                spawn = enemySpawn.spawnPosition
                width = prototype.width if(hasattr(prototype, "width")) else None
                enemy = Enemy(self.gameWorldSurf, prototype, self.playerProjectileGroup,
                            self.enemyProjectileGroup, self.iceCubes, center=(spawn.x, spawn.y), width=width,  deathAnimsDic = self.deathAnims)
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
        speed = pygame.Vector2(
            0, self.BG_SPEED + (width*2.5 / WIDTH) * self.CLOUD_SPEED)
        return BackgroundObject(img, speed, width, topleft=(randomX,  Y))

    def rollDices(self, diceCount: int):
        pygame.mixer.Sound.play(self.diceRoll)
        for i in range(diceCount):
            self.nextHeatWave[i] = random.randint(1, 6)

        if self.num != 0:
            self.lastHeatwaveTime = pygame.time.get_ticks()
        elif (self.tutorialPhase == 2 and self.tutorialStep == 1) or self.tutorialPhase > 2:
            self.lastHeatwaveTime = pygame.time.get_ticks()


    def applyHeatwave(self):

        # If its the first heatwave, just roll dice
        if self.nextHeatWave[0] == 0:
            self.rollDices(self.diceCount)
            return

        # This does not apply the heat wave on the player if he is on invincibility frames
        frostLeft = self.frostLevel - \
            sum(self.nextHeatWave) if self.player.isAlive else self.frostLevel

        if (frostLeft <= 0):
            # ur dead lol remove a life here
            self.player.die()
            pass
        else:
            self.frostLevel = frostLeft

        self.rollDices(self.diceCount)  # Roll dices for next heatwave

    def update(self, game, events, keys) -> None:
        self.pollInput(events, keys)
        if self.num == 0:
            self.tutorialUpdate(events)

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
                pygame.mixer.Sound.play(self.icePickup)
                iceCube.kill()
                break

        # if(len(self.backgroundObjectsGroup.sprites()) < self.CLOUDS):
        #     self.backgroundObjectsGroup.add(self.generateCloud())
        # if(len(self.backgroundTilesGroup.sprites()) < self.NB_TOT_TILES):
        #     for i in range(self.NB_WIDTH_TILES):
        #         self.backgroundTilesGroup.add(
        #             BackgroundObject(self.BG, pygame.Vector2(
        #                 0, self.BG_SPEED), self.SIZE_TILE, topleft=(self.SIZE_TILE * i, self.OFFSET-self.SIZE_TILE))
        #        )

        if self.invincibilityFrameStart is not None:
            delta = pygame.time.get_ticks() - self.invincibilityFrameStart
            if delta % INVINCIBILITY_FLASH > 100:
                self.drawPlayer = not self.drawPlayer
            if delta > INVINCIBILITY_TIME:
                self.drawPlayer = True
                self.player.isAlive = True
                self.invincibilityFrameStart = None

        if not self.player.isAlive and self.invincibilityFrameStart is None:
            if self.player.lives <= 0:
                pygame.mixer.Sound.play(self.dieScrub)
                self.game.switchState(
                    "InGameState", InGameStatePayload(self.num))

            # Frost loss, reset frost to 5
            if self.frostLevel <= 0:
                pygame.time.set_timer(E_HEATWAVE, 0)
                pygame.time.set_timer(E_HEATWAVE, HEATWAVE_INTERVAL_SEC * 1000)
                self.frostLevel = 5

            self.invincibilityFrameStart = pygame.time.get_ticks()

        # Spawn enemies
        for event in events:
            if event.type == E_NEXT_SPAWN:
                self.spawnEnemies()
            elif event.type == E_HEATWAVE:
                self.applyHeatwave()
            elif event.type == E_END_LEVEL:
                pygame.mixer.Sound.play(self.levelEnd)
                self.game.switchState(
                    "InGameState", InGameStatePayload(self.num + 1))
        if (keys[pygame.K_x] or keys[pygame.K_j]): 
            self.framesHeld %= 5
            if self.frostLevel > 0 and self.framesHeld == 0: self.addFrost(-1) # remove frost levels yourself
            self.framesHeld += 1

    def tutorialUpdate(self, events) -> None:
        # On the first frame just start a timer for the wasd + space section
        if self.tutorialPhase == 0 and self.tutorialStep == -1:
            self.tutorialStep = 0
            pygame.time.set_timer(E_NEXT_TUTORIAL_PHASE, 100, 1) # First tutorial phase duration

        for event in events:
            if event.type == E_NEXT_TUTORIAL_PHASE:
                self.tutorialPhase += 1
                self.tutorialStep = 0

                if self.tutorialPhase == 1:
                    # Phase 1 has 11 steps:
                    # 0 Introducing frost-o-meter
                    # 1 frost = 10
                    # 2 frost = 9
                    # 3 frost = 8
                    # 4 frost = ...
                    pygame.time.set_timer(E_NEXT_TUTORIAL_STEP, 100)
                if self.tutorialPhase == 2:
                    # Phase 2 has 3 steps:
                    # 0 Rolling dice
                    # 1 Start the timer
                    # 2 Heatwave hitting
                    self.rollDices(self.diceCount)
                    self.nextHeatWave = [2]
                    pygame.time.set_timer(E_NEXT_TUTORIAL_STEP, 5000, 1)
            if event.type == E_NEXT_TUTORIAL_STEP:
                # PHASE 1
                if self.tutorialPhase == 1:
                    if self.tutorialStep == 0:
                        self.tutorialStep += 1
                        self.frostLevel = 10
                        pygame.time.set_timer(E_NEXT_TUTORIAL_STEP, 100, 10)
                    elif self.frostLevel > 1:
                        self.frostLevel -= 1
                    else:
                        pygame.event.post(pygame.event.Event(E_NEXT_TUTORIAL_PHASE))
                # PHASE 2
                if self.tutorialPhase == 2:
                    if self.tutorialStep == 0:
                        self.lastHeatwaveTime = pygame.time.get_ticks() # start timer
                        pygame.time.set_timer(E_HEATWAVE, HEATWAVE_INTERVAL_SEC * 1000)
                    if self.tutorialStep == 1:
                        print("TEST")
                        pygame.event.post(pygame.event.Event(E_NEXT_TUTORIAL_PHASE))
                    self.tutorialStep += 1




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
                     self.nextHeatWave, self.lastHeatwaveTime, self.player.lives, self.tutorialPhase, self.tutorialStep, self.num)

    def pollInput(self, events, keys) -> None:
        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    self.game.switchState(
                        "InGameState", InGameStatePayload(self.num))
                if event.key == pygame.K_x or event.key == pygame.K_j:
                    self.framesHeld = 0

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
    with open(resource_path('res/enemies/images.json'), 'r') as file:
        data = jstyleson.loads(file.read())
        for key in data.keys():
            dicImages[key] = pygame.image.load(resource_path(data[key]))

    # Loading prototypes
    dicEnemyPrototypes = {}
    directory = resource_path('res/enemies/prototypes')
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
                               attack['projectileSpeed'], radianInitialRotation, radianRotate, attack['shotCooldownMs'], projectileWidth=20)

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
    with open(resource_path(f'res/levels/{levelNum}.json')) as file:
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

    level = Level(game, levelNum, screen, gameWorldSurf,
                  dicEnemyPrototypes, dicEnemySpawns, endTimeMs)

    with open(f'res/levels/{levelNum}.json') as file:
        levelData = jstyleson.loads(file.read())

        # Load Bg elems
        level.CLOUDS = levelData["bgOptions"]["CLOUDS"]
        level.CLOUD_SPEED = levelData["bgOptions"]["CLOUD_SPEED"]
        # note: must be higher than 1
        level.NB_HEIGHT_TILES = levelData["bgOptions"]["NB_HEIGHT_TILES"]
        level.BG_SPEED = levelData["bgOptions"]["BG_SPEED"]
        # tweek if you see gaps in the textures (this shit is black magic)
        level.OFFSET = levelData["bgOptions"]["OFFSET"]
        level.BG = pygame.image.load(resource_path(
            levelData["bgOptions"]["img_location"]))
        level.CLOUD_TYPE = "-" + \
            levelData["bgOptions"]["CLOUD_TYPE"] if "CLOUD_TYPE" in levelData["bgOptions"] else ""
        level.SIZE_TILE = int(HEIGHT/(level.NB_HEIGHT_TILES-1))
        level.NB_WIDTH_TILES = ceil(WIDTH/(2*level.SIZE_TILE))
        level.NB_TOT_TILES = level.NB_WIDTH_TILES * level.NB_HEIGHT_TILES

        level.background = level.BG
        level.CLOUDSIMG = [
            pygame.image.load(resource_path(os.path.join('res', f'cloud-{i}{level.CLOUD_TYPE}.png'))) for i in range(1, 6)
        ]

        # Generate initial clouds
        for _ in range(level.CLOUDS):
            level.backgroundObjectsGroup.add(level.generateCloud(True))

        # Generate initial bg
        for i in range(level.NB_WIDTH_TILES):
            for j in range(level.NB_HEIGHT_TILES):
                level.backgroundTilesGroup.add(
                    BackgroundObject(level.BG, pygame.Vector2(
                        0, level.BG_SPEED), level.SIZE_TILE, topleft=(level.SIZE_TILE * i, level.SIZE_TILE * j), randomPos=False, OFFSET=level.OFFSET)
                )

    return level
