import pygame

class EnemyMove:
    def __init__(self, destX: int, destY: int, duration: int):
        self.destX = destX
        self.destY = destY
        self.duration = duration