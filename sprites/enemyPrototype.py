import pygame

from attack import Attack

class EnemyPrototype:
    def __init__(self, image: pygame.Surface, health: int, attack: Attack, playerProjectileGroup: pygame.sprite.Group, enemyProjectileGroup: pygame.sprite.Group):
        self.image = image
        self.health = health
        self.attack = attack
        self.playerProjectileGroup = playerProjectileGroup
        self.enemyProjectileGroup = enemyProjectileGroup