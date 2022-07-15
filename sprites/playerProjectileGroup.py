import pygame

class PlayerProjectileGroup(pygame.sprite.Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)