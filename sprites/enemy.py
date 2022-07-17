from pickle import FRAME
import pygame
import random
import numpy
from iceCube import IceCube
from sprites.enemyPrototype import EnemyPrototype
from sprites.projectile import Projectile
from constants import TARGET_FPS

class Enemy(pygame.sprite.Sprite):
    def __init__(self, gameWorldSurf: pygame.Surface, enemyPrototype: EnemyPrototype, playerProjectileGroup: pygame.sprite.Group, enemyProjectileGroup: pygame.sprite.Group, iceCubes: pygame.sprite.Group, **kwargs):
        pygame.sprite.Sprite.__init__(self)

        self.gameWorldSurf = gameWorldSurf

        self.playerProjectileGroup = playerProjectileGroup
        self.enemyProjectileGroup = enemyProjectileGroup
        self.iceCubes = iceCubes

        self.enemyPrototype = enemyPrototype
        self.image = enemyPrototype.image
        self.rect = self.image.get_rect(**kwargs)
        self.curMoveIndex = 0
        self.speed = pygame.Vector2(0, 0)
        self.precisePos = pygame.Vector2(0, 0) # This is needed for the enemy to move because pygame.Rect does not take into account floating point precision
        self.speed = self.computeSpeed()
        self.health = self.enemyPrototype.health

        self.shotEventId = self.enemyPrototype.attack.createShotTimer()


    def die(self):
        self.kill()
        self.enemyPrototype.attack.removeShotTimer(self.shotEventId)
        cube = IceCube(self.enemyPrototype.iceDrop, center=self.rect.center)
        self.iceCubes.add(cube)

    def update(self, **kwargs) -> None:
        # If it goes offscreen, die
        if self.rect.right < 0 or self.rect.bottom < 0 or self.rect.left > self.gameWorldSurf.get_width() or self.rect.top > self.gameWorldSurf.get_height():
            self.kill()
            return

        # Kill enemy if it's hit by a player projectile
        for projectile in self.playerProjectileGroup.sprites():
            if self.rect.colliderect(projectile.rect):
                self.health -= projectile.damage

                if self.health <= 0:
                    self.die()
                    return

                projectile.kill()


        # Shoot
        if "events" in kwargs:
            for event in kwargs["events"]:
                if event.type == self.shotEventId:
                    self.enemyPrototype.attack.performAttack(self.gameWorldSurf, self.rect, self.enemyProjectileGroup)


        # If move is completed
        if self.curDestionation.x == numpy.ceil(numpy.round(self.precisePos.x, 2)) and self.curDestionation.y == numpy.ceil(numpy.round(self.precisePos.y, 2)): # Floating point :)))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
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

        self.curDestionation = pygame.Vector2(self.rect.center) + pygame.Vector2(move.delta)

        return pygame.Vector2(move.delta) / (TARGET_FPS * move.duration)