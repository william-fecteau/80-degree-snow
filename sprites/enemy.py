from pickle import FRAME
import pygame
import random
import numpy
from sprites.enemyPrototype import EnemyPrototype
from sprites.projectile import Projectile
from constants import TARGET_FPS

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemyPrototype: EnemyPrototype, **kwargs):
        pygame.sprite.Sprite.__init__(self)

        self.enemyPrototype = enemyPrototype
        self.image = enemyPrototype.image
        self.rect = self.image.get_rect(**kwargs)
        self.curMoveIndex = 0
        self.speed = pygame.Vector2(0, 0)
        self.precisePos = pygame.Vector2(0, 0) # This is needed for the enemy to move because pygame.Rect does not take into account floating point precision
        self.speed = self.computeSpeed()

        self.shotEventId = self.enemyPrototype.attack.createShotTimer()


    def die(self):
        self.kill()
        self.enemyPrototype.attack.removeShotTimer(self.shotEventId)

    def update(self, **kwargs) -> None:
        # Kill enemy if it's hit by a player projectile
        for projectile in self.enemyPrototype.playerProjectileGroup.sprites():
            if self.rect.colliderect(projectile.rect):
                self.enemyPrototype.health -= 1

                if self.enemyPrototype.health <= 0:
                    self.die()
                    return

                projectile.kill()

        # Shoot
        if "events" in kwargs:
            for event in kwargs["events"]:
                if event.type == self.shotEventId:
                    self.enemyPrototype.attack.performAttack(self.rect, self.enemyPrototype.enemyProjectileGroup)



        move = self.enemyPrototype.moves[self.curMoveIndex]

        # If move is completed
        if move.destX == numpy.ceil(numpy.round(self.precisePos.x, 2)) and move.destY == numpy.ceil(numpy.round(self.precisePos.y, 2)): # Floating point :)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
            self.curMoveIndex += 1

            # If there are no more moves, kill the sprite
            if self.curMoveIndex >= len(self.enemyPrototype.moves):
                self.die()
                return

            # Compute speed for next move
            self.speed = self.computeSpeed()
        # Else we continue the current move
        else:
            self.precisePos += self.speed
            self.rect.center = self.precisePos


    def computeSpeed(self) -> None:
        self.precisePos = pygame.Vector2(self.rect.centerx, self.rect.centery)
        move = self.enemyPrototype.moves[self.curMoveIndex]
        deltaX = (move.destX - self.rect.centerx)
        deltaY = (move.destY - self.rect.centery)

        return pygame.Vector2(deltaX, deltaY) / (TARGET_FPS * move.duration)