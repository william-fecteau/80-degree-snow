import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, direction: pygame.math.Vector2(), speed: int, **kwargs):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect(**kwargs)
        self.direction = direction.normalize()
        self.speed = speed


    def update(self) -> None:
        self.rect.center += self.direction * self.speed
