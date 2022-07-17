import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, gameWorldSurf: pygame.Surface, image: pygame.Surface, speed: pygame.math.Vector2(), damage: int = 1, width = None, **kwargs):
        pygame.sprite.Sprite.__init__(self)

        self.gameWorldSurf = gameWorldSurf
        self.image = pygame.Surface.convert_alpha(image)
        self.rect = self.image.get_rect(**kwargs)
        if(width != None):  self.image = pygame.Surface.convert_alpha(pygame.transform.scale(image, (width, image.get_height() * (width / image.get_width()))))
        self.precisePos = pygame.Vector2(self.rect.center)
        self.speed = speed
        self.damage = damage
                
    def update(self) -> None:
        self.precisePos += self.speed
        self.rect.center = self.precisePos

        # If it goes offscreen, die
        if self.rect.right < 0 or self.rect.bottom < 0 or self.rect.left > self.gameWorldSurf.get_width() or self.rect.top > self.gameWorldSurf.get_height():
            self.kill()
