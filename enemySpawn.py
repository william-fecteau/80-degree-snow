import pygame

from sprites import enemyPrototype

class EnemySpawn:
    def __init__(self, enemyPrototype: enemyPrototype, spawnPosition: pygame.Vector2):
        self.enemyPrototype = enemyPrototype
        self.spawnPosition = spawnPosition