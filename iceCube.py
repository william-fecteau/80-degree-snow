import pygame

NB_STACK_MAX = 2
CUBES_IMG = [pygame.image.load(f'res/images/ice{i+1}.png') for i in range(NB_STACK_MAX)]
SPEED_DOWN = 3


class IceCube(pygame.sprite.Sprite):
    def __init__(self, nbIce: int, **kwargs):
        pygame.sprite.Sprite.__init__(self)

        # 5 incrément de 5 start à 24
        self.image = CUBES_IMG[nbIce - 1]
        self.rect = self.image.get_rect(**kwargs)


    def update(self):
        self.rect.centery += SPEED_DOWN

