import pygame
import random

from sprites.projectile import Projectile

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, health: int, playerProjectileGroup: pygame.sprite.Group, enemyProjectileGroup: pygame.sprite.Group, **kwargs):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect(**kwargs)
        self.playerProjectileGroup = playerProjectileGroup
        self.enemyProjectileGroup = enemyProjectileGroup
        self.health = health

        self.projectileImg = pygame.image.load("res/intro_ball.gif")


    def shoot(self) -> None:
        projectile = Projectile(self.projectileImg, pygame.math.Vector2(0, 5), centerx=self.rect.centerx, bottom=self.rect.bottom)
        self.enemyProjectileGroup.add(projectile)


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
