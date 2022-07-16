import pygame
import random
import numpy
from sprites.enemyPrototype import EnemyPrototype
from sprites.projectile import Projectile

DEFAULT_SHOT_SPEED_MS = 300
E_PLAYER_SHOT_COOLDOWN = pygame.USEREVENT + 1

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemyPrototype: EnemyPrototype, **kwargs):
        pygame.sprite.Sprite.__init__(self)

        self.enemyPrototype = enemyPrototype
        self.image = enemyPrototype.image
        self.rect = self.image.get_rect(**kwargs)
        

    def update(self) -> None:
        for projectile in self.enemyPrototype.playerProjectileGroup.sprites():
            if self.rect.colliderect(projectile.rect):
                self.enemyPrototype.health -= 1

                if self.enemyPrototype.health <= 0:
                    self.kill()
                    break

                projectile.kill()

        shouldShoot = random.randint(0, 1000)
        if shouldShoot > 998:
            self.enemyPrototype.attack.performAttack(self.rect, self.enemyPrototype.enemyProjectileGroup)
