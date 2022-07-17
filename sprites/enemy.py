from math import floor
from pickle import FRAME
import pygame
import random
import numpy
from iceCube import IceCube
from sprites.enemyPrototype import EnemyPrototype
from sprites.projectile import Projectile
from constants import TARGET_FPS
from utils import resource_path

class Enemy(pygame.sprite.Sprite):
    def __init__(self, gameWorldSurf: pygame.Surface, enemyPrototype: EnemyPrototype, playerProjectileGroup: pygame.sprite.Group, enemyProjectileGroup: pygame.sprite.Group, iceCubes: pygame.sprite.Group, width, deathAnimsDic, **kwargs):
        pygame.sprite.Sprite.__init__(self)

        self.gameWorldSurf = gameWorldSurf

        self.playerProjectileGroup = playerProjectileGroup
        self.enemyProjectileGroup = enemyProjectileGroup
        self.iceCubes = iceCubes

        self.enemyPrototype = enemyPrototype
        self.image = pygame.transform.scale(enemyPrototype.image, (width, enemyPrototype.image.get_height() * (width / enemyPrototype.image.get_width()))) if width != None else enemyPrototype.image
        self.rect = self.image.get_rect(**kwargs)
        self.curMoveIndex = 0
        self.speed = pygame.Vector2(0, 0)
        self.precisePos = pygame.Vector2(0, 0) # This is needed for the enemy to move because pygame.Rect does not take into account floating point precision
        self.speed = self.computeSpeed()
        self.health = self.enemyPrototype.health
        self.ANIM_FPS = 15

        self.shotEventId = self.enemyPrototype.attack.createShotTimer()
        self.dead = False
        self.deathAnim = 0

        self.deathAnimsDic = deathAnimsDic;

        # Setup sounds
        self.hitSound = pygame.mixer.Sound(resource_path("res/enemyDmg1.mp3"))
        pygame.mixer.Sound.set_volume(self.hitSound,1)


    def die(self):
        self.enemyPrototype.attack.removeShotTimer(self.shotEventId)
        self.dead = True
        
    def update(self, **kwargs) -> None:
        if self.dead:
            self.deathAnim += 1
            if self.deathAnim > self.ANIM_FPS*(len(self.deathAnimsDic)-1): self.kill()
            elif self.deathAnim % self.ANIM_FPS == 0: 
                if self.deathAnim < 40 : self.image = pygame.transform.scale(self.deathAnimsDic[floor(self.deathAnim/self.ANIM_FPS)], (self.rect.width , self.rect.height ))
                else: self.image = pygame.transform.scale(self.deathAnimsDic[3 - floor(self.deathAnim/self.ANIM_FPS)], (self.rect.width , self.rect.height))


        if not self.dead:
            # If it goes offscreen, die
            if self.rect.right < 0 or self.rect.bottom < 0 or self.rect.left > self.gameWorldSurf.get_width() or self.rect.top > self.gameWorldSurf.get_height():
                self.kill()
                return

            # Kill enemy if it's hit by a player projectile
            for projectile in self.playerProjectileGroup.sprites():
                if self.rect.colliderect(projectile.rect):
                    self.health -= projectile.damage
                    pygame.mixer.Sound.play(self.hitSound)

                    if self.health <= 0:
                        if self.enemyPrototype.iceDrop:
                            for i in range(self.enemyPrototype.iceDrop):
                                cube = IceCube(1, self.playerProjectileGroup, 
                                    center=(random.randint(self.rect.center[0]-20, self.rect.center[0]+20),
                                          random.randint(self.rect.center[1]-20, self.rect.center[1]+20))
                                )
                                self.iceCubes.add(cube)
                        else:
                            cube = IceCube(1, self.playerProjectileGroup, center=(self.rect.center))
                            self.iceCubes.add(cube)
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

        self.curDestionation = pygame.Vector2(self.rect.center) + pygame.Vector2(move.delta)

        return pygame.Vector2(move.delta) / (TARGET_FPS * move.duration)