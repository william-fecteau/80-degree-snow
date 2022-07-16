import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, speed: pygame.math.Vector2(), **kwargs):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface.convert_alpha(image)
        self.rect = self.image.get_rect(**kwargs)
        self.speed = speed


    def update(self) -> None:
        self.rect.center += self.speed

        # If it goes offscreen, die
        screen = pygame.display.get_surface()
        if self.rect.right < 0 or self.rect.bottom < 0 or self.rect.left > screen.get_width() or self.rect.top > screen.get_height():
            self.kill()
