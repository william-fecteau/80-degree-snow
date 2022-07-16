import pygame

from sprites.playerProjectileGroup import PlayerProjectileGroup
from sprites.projectile import Projectile

DEFAULT_SHOT_SPEED_MS = 300
E_PLAYER_SHOT_COOLDOWN = pygame.USEREVENT + 1

class Player(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, playerProjectileGroup: PlayerProjectileGroup, **kwargs):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect(**kwargs)
        self.direction = pygame.math.Vector2()
        self.canShoot = True
        self.speed = 10

        self.playerProjectileGroup = playerProjectileGroup
        self.projectileSurface = pygame.image.load("res/intro_ball.gif")
        pygame.time.set_timer(E_PLAYER_SHOT_COOLDOWN, DEFAULT_SHOT_SPEED_MS)


    def setShotCooldown(self, shotSpeedMs: int) -> None:
        pygame.time.set_timer(E_PLAYER_SHOT_COOLDOWN, 0)
        self.canShoot = True
        pygame.time.set_timer(E_PLAYER_SHOT_COOLDOWN, shotSpeedMs)


    def shoot(self) -> None:
        print("test")
        projectile = Projectile(self.projectileSurface, pygame.Vector2(0, -20), bottom=(self.rect.top), centerx=self.rect.centerx)
        self.playerProjectileGroup.add(projectile)


    def update(self, events, keys) -> None:
        self.direction = pygame.Vector2(0, 0)

        screen = pygame.display.get_surface()
        # If player goes offscreen, dont lmao
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screen.get_width():
            self.rect.right = screen.get_width()
            
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > screen.get_height():
            self.rect.bottom = screen.get_height()


        # Check if player can shoot
        for event in events:
            if event.type == E_PLAYER_SHOT_COOLDOWN:
                self.canShoot = True
        
        if (keys[pygame.K_SPACE] or keys[pygame.K_z]) and self.canShoot:
            self.canShoot = False
            self.shoot()


        # Move player
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1

        self.rect.center += self.direction * self.speed