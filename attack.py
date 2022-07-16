import pygame
import numpy
import math

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
            cosTheta = round(math.cos(rotation), 2)
            sinTheta = round(math.sin(rotation), 2)

            speed = pygame.math.Vector2(cosTheta, sinTheta) * self.projectileSpeed
            
            projectileSpeed = speed * round(speed.magnitude(), 2)

            projectile = Projectile(self.projectileImg, projectileSpeed, centerx=casterRect.centerx, bottom=casterRect.bottom)
            projectileGroup.add(projectile)

            rotation += self.rotateSpeed