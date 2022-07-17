import pygame
import os

NB_STACK_MAX = 5
CUBES_IMG = [pygame.image.load(os.path.join(
    'res', f'ice{i+1}.png')) for i in range(NB_STACK_MAX)]
SPEED_DOWN = 3
HIT_BEFORE_BREAK = 5


class IceCube(pygame.sprite.Sprite):
    def __init__(self, nbIce: int, playerProjectileGroup: pygame.sprite.Group, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.playerProjectileGroup = playerProjectileGroup

        # 5 incrément de 5 start à 24
        self.nbIce = nbIce
        self.image = CUBES_IMG[nbIce - 1]
        self.rect = self.image.get_rect(**kwargs)
        self.hitsBeforeBreak = HIT_BEFORE_BREAK

    def update(self):
        self.rect.centery += SPEED_DOWN

        for playerProjectile in self.playerProjectileGroup.sprites():
            if playerProjectile.rect.colliderect(self.rect):
                self.hitsBeforeBreak -= 1

                if self.hitsBeforeBreak <= 0:
                    self.kill()
                    break

                playerProjectile.kill()
