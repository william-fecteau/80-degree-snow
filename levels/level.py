import queue
from math import ceil
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
E_HEATWAVE = pygame.USEREVENT + 6

HEATWAVE_INTERVAL_SEC = 5
NB_DICE = 3
DICE_SIZE = 100

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
    BG_SPEED = 2
    OFFSET = 2 # tweek if you see gaps in the textures (this shit is black magic)

    def __init__(self, game, num: int, screen: pygame.Surface, gameWorldSurf: pygame.surface, dicEnemyPrototypes: dict, dicEnemySpawns: dict) -> None:
        self.game = game
        self.num = num
        self.screen = screen
        self.dicEnemyPrototypes = dicEnemyPrototypes
        self.gameWorldSurf = gameWorldSurf
        self.dicEnemySpawns = dicEnemySpawns
        self.background = self.BG

        self.diceFaces = [pygame.image.load(f"res/images/dice{i}.png") for i in range(1, 7)]
        for i in range(len(self.diceFaces)):
            self.diceFaces[i] = pygame.transform.scale(self.diceFaces[i], (DICE_SIZE, DICE_SIZE))

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
            for j in range(self.NB_HEIGHT_TILES):
                self.backgroundTilesGroup.add(
                    BackgroundObject(self.BG, pygame.Vector2(0, -self.BG_SPEED), self.SIZE_TILE, topleft=(self.SIZE_TILE * i, self.SIZE_TILE *j))
                )

        # Check for first enemy spawn
        self.nextSpawnTimeMs = list(self.dicEnemySpawns.keys())[0]
        if (self.nextSpawnTimeMs == 0):
            self.spawnEnemies()
        else:
            pygame.time.set_timer(E_NEXT_SPAWN, self.nextSpawnTimeMs)

        # Heatwave setup
        self.nextHeatWave = [0 for _ in range(NB_DICE)]
        pygame.time.set_timer(E_HEATWAVE, HEATWAVE_INTERVAL_SEC * 1000)


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
            oldSpawn = self.nextSpawnTimeMs
            self.nextSpawnTimeMs = list(self.dicEnemySpawns.keys())[0]
            pygame.time.set_timer(E_NEXT_SPAWN, self.nextSpawnTimeMs - oldSpawn)
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

    def generateCloud(self, randomY = False):
            img = self.CLOUDSIMG[random.randint(0, len(self.CLOUDSIMG)-1)]                  # Pick a random sprite
            width = random.randint(int(WIDTH/10), int(WIDTH))                               # Pick a random size 
            randomX = random.randint(-int(width/2), WIDTH+int(width/2))                     # Pick a random X position
            Y = random.randint(0 - HEIGHT/2, HEIGHT) if randomY else -img.get_height()*1.75   # Pick a randon Y position or top of the screen
            speed =  pygame.Vector2(0, -(width*2.5 / WIDTH)*12)                             # Pick a speed calculated by size of image
            return BackgroundObject(img, speed, width, topleft=(randomX,  Y))
        
    def rollDices(self):
        for i in range(NB_DICE):
            self.nextHeatWave[i] = random.randint(1, 6)

    def applyHeatwave(self):

        # If its the first heatwave, just roll dice
        if self.nextHeatWave[0] == 0:
            self.rollDices()
            return
        
        # TODO: Actually apply heatwave effect
        self.rollDices() # Roll dices for next heatwave





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
            # print(self.NB_TOT_TILES)
            # print(len(self.backgroundTilesGroup.sprites()))
            for i in range(self.NB_WIDTH_TILES):
                self.backgroundTilesGroup.add(
                    BackgroundObject(self.BG, pygame.Vector2(0, -self.BG_SPEED), self.SIZE_TILE, topleft=(self.SIZE_TILE * i, self.OFFSET-self.SIZE_TILE))
                )
                # print("BG: " +  str(int(self.SIZE_TILE * i)) +", " + str(-self.SIZE_TILE))


        if not self.player.isAlive:
            game.switchState("MenuState")

        # Spawn enemies
        for event in events:
            if event.type == E_NEXT_SPAWN:
                self.spawnEnemies()
                break
            elif event.type == E_HEATWAVE:
                self.applyHeatwave()
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
        leftUi = pygame.Surface((WIDTH/4, HEIGHT))
        leftUiRect = leftUi.get_rect(topleft=(0, 0))

        rightUi = pygame.Surface((WIDTH/4, HEIGHT))
        rightUiRect = leftUi.get_rect(topright=(WIDTH, 0))


        # If we're not on the first round, draw the dices
        if self.nextHeatWave[0] != 0:
            # Dices
            diceYOffset = 10
            diceYStart = HEIGHT - (NB_DICE * (DICE_SIZE + diceYOffset))
            centerx = leftUiRect.centerx
            for i in range(NB_DICE):
                num = self.nextHeatWave[i] - 1
                leftUi.blit(self.diceFaces[num], (centerx - DICE_SIZE / 2, diceYStart + i * (DICE_SIZE + diceYOffset)))

        self.screen.blit(leftUi, leftUiRect)
        self.screen.blit(rightUi, rightUiRect)
        








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
