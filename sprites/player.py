import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, **kwargs):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect(**kwargs)
        self.direction = pygame.math.Vector2()
        self.speed = 10


    def input(self):
        keys = pygame.key.get_pressed()

        self.direction.x = 0
        self.direction.y = 0

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        


    def update(self):
        self.input()
        newPos = self.direction * self.speed
        self.rect.center += newPos

        screen = pygame.display.get_surface()

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screen.get_width():
            self.rect.right = screen.get_width()
            
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > screen.get_height():
            self.rect.bottom = screen.get_height()
        