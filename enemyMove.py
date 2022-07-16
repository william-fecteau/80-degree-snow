import pygame

class EnemyMove:
    def __init__(self, delta: pygame.Vector2(), duration: int):
        self.delta = delta
        self.duration = duration