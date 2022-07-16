import pygame
import numpy

from sprites.projectile import Projectile

class Attack:
    def __init__(self, projectileImg: pygame.Surface, nbProjectiles: int, projectileSpeed: int, rotateSpeed: float, initialRotation: float):
        self.projectileImg = projectileImg
        self.nbProjectiles = nbProjectiles
        self.projectileSpeed = projectileSpeed
        self.rotateSpeed = rotateSpeed
        self.initialRotation = initialRotation


    def performAttack(self, casterRect: pygame.Rect, projectileGroup: pygame.sprite.Group):
        rotation = self.initialRotation
        for _ in range(self.nbProjectiles):
            speed = pygame.math.Vector2(self.projectileSpeed*numpy.cos(rotation), self.projectileSpeed*numpy.sin(rotation))
            projectile = Projectile(self.projectileImg, speed, centerx=casterRect.centerx, right=casterRect.bottom)
            projectileGroup.add(projectile)

            rotation += self.rotateSpeed