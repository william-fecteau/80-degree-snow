from pickle import FRAME
import pygame
import random
import numpy
from sprites.enemyPrototype import EnemyPrototype
from sprites.projectile import Projectile
from constants import TARGET_FPS


DEFAULT_SHOT_SPEED_MS = 300
E_PLAYER_SHOT_COOLDOWN = pygame.USEREVENT + 1

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


    def update(self) -> None:
        # Kill enemy if it's hit by a player projectile
        for projectile in self.enemyPrototype.playerProjectileGroup.sprites():
            if self.rect.colliderect(projectile.rect):
                self.enemyPrototype.health -= 1

                if self.enemyPrototype.health <= 0:
                    self.kill()
                    return

                projectile.kill()

        # Shoot
        shouldShoot = random.randint(0, 1000)
        if shouldShoot > 998:
            self.enemyPrototype.attack.performAttack(self.rect, self.enemyPrototype.enemyProjectileGroup)


        move = self.enemyPrototype.moves[self.curMoveIndex]

        # If move is completed
        if move.destX == numpy.ceil(numpy.round(self.precisePos.x, 2)) and move.destY == numpy.ceil(numpy.round(self.precisePos.y, 2)): # Floating point :)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
            self.curMoveIndex += 1

            # If there are no more moves, kill the sprite
            if self.curMoveIndex >= len(self.enemyPrototype.moves):
                self.kill()
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