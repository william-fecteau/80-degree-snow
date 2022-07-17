import pygame

from attack import Attack
from enemyMove import EnemyMove

class EnemyPrototype:
    def __init__(self, image: pygame.Surface, health: int, attack: Attack, moves: list[EnemyMove], iceDrop: int, width: int):
        self.image = image
        self.health = health
        self.attack = attack
        self.moves = moves
        self.iceDrop = iceDrop
        self.width = width