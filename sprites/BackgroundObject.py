import random
import pygame

class BackgroundObject(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, speed: pygame.math.Vector2(), width = None, randomPos=True, OFFSET= 0, **kwargs):
        pygame.sprite.Sprite.__init__(self)

        self.speed = speed
        if(width != None):  self.image = pygame.transform.scale(image, (width, image.get_height() * (width / image.get_width())))
        else: self.image = image

        self.rect = self.image.get_rect(**kwargs)
        self.rect.width = self.image.get_width()
        self.rect.height = self.image.get_height()
        self.randomPos = randomPos
        self.OFFSET = OFFSET

        self.image = pygame.Surface.convert_alpha(self.image);


    def update(self) -> None:
        self.rect.center += self.speed

        # If it goes offscreen, die
        screen = pygame.display.get_surface()
        if self.rect.top >  screen.get_height():
            if self.randomPos: self.rect.left = random.randint(-int(self.rect.width/2), screen.get_width()+int(self.rect.width/2))
            else: self.rect.bottom = screen.get_height()
            self.rect.bottom = self.OFFSET
