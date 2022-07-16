import pygame
import random
import numpy
from sprites.projectile import Projectile

DEFAULT_SHOT_SPEED_MS = 300
E_PLAYER_SHOT_COOLDOWN = pygame.USEREVENT + 1

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, health: int, playerProjectileGroup: pygame.sprite.Group,
     enemyProjectileGroup: pygame.sprite.Group, projectile_speed: int=5, number_of_projectile: int = 1, rotate_speed: float =0, 
    rotation: float = 0, **kwargs):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect(**kwargs)
        self.playerProjectileGroup = playerProjectileGroup
        self.enemyProjectileGroup = enemyProjectileGroup
        self.health = health
        self.rotate_speed = numpy.pi/16
        self.number_of_projectile = 4
        self.projectile_speed = 10
        self.rotation = numpy.pi/3

        self.projectileImg = pygame.image.load("res/intro_ball.gif")


    def calculateSpeed(self, rotate: float) -> pygame.math.Vector2:
        return pygame.math.Vector2(self.projectile_speed*numpy.cos(rotate), self.projectile_speed*numpy.sin(rotate))

    def shoot(self) -> None:
        rotationActuel = self.rotation
        for i in range(self.number_of_projectile):  
            projectile = Projectile(self.projectileImg, self.calculateSpeed(rotationActuel), centerx=self.rect.centerx, bottom=self.rect.bottom)
            self.enemyProjectileGroup.add(projectile)
            rotationActuel += self.rotate_speed
        

    

        

    def update(self) -> None:
        for projectile in self.playerProjectileGroup.sprites():
            if self.rect.colliderect(projectile.rect):
                self.health -= 1

                if self.health <= 0:
                    self.kill()
                    break

                projectile.kill()

        shouldShoot = random.randint(0, 1000)
        if shouldShoot > 998:
            self.shoot()
