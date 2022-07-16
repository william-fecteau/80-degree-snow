import pygame
import numpy

from sprites.projectile import Projectile

class Attack:
    eventCounter = 0

    def __init__(self, projectileImg: pygame.Surface, nbProjectiles: int, projectileSpeed: int, rotateSpeed: float, initialRotation: float, shotCooldownMs: int):
        self.projectileImg = projectileImg
        self.nbProjectiles = nbProjectiles
        self.projectileSpeed = projectileSpeed
        self.rotateSpeed = rotateSpeed
        self.initialRotation = initialRotation
        self.shotCooldownMs = shotCooldownMs


    def createShotTimer(self) -> int:
        eventId = pygame.USEREVENT + 10000 + Attack.eventCounter
        Attack.eventCounter += 1
        pygame.time.set_timer(eventId, self.shotCooldownMs)
        return eventId


    def removeShotTimer(self, eventId: int) -> None:
        pygame.time.set_timer(eventId, 0)


    def performAttack(self, casterRect: pygame.Rect, projectileGroup: pygame.sprite.Group) -> None:
        rotation = self.initialRotation
        for _ in range(self.nbProjectiles):
            speed = pygame.math.Vector2(self.projectileSpeed*numpy.cos(rotation), self.projectileSpeed*numpy.sin(rotation))
            projectile = Projectile(self.projectileImg, speed, centerx=casterRect.centerx, bottom=casterRect.bottom)
            projectileGroup.add(projectile)

            rotation += self.rotateSpeed