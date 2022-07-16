import pygame

from sprites.playerProjectileGroup import PlayerProjectileGroup

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, playerProjectileGroup: PlayerProjectileGroup, **kwargs):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect(**kwargs)
        self.playerProjectileGroup = playerProjectileGroup


    def update(self) -> None:
        for projectile in self.playerProjectileGroup.sprites():
            if self.rect.colliderect(projectile.rect):
                self.kill()
                projectile.kill()
                break
