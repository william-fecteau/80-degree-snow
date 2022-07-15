import pygame

DEFAULT_SHOT_SPEED_MS = 1000
E_PLAYER_SHOT_COOLDOWN = pygame.USEREVENT + 1

class Player(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, **kwargs):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect(**kwargs)
        self.direction = pygame.math.Vector2()
        self.canShoot = True
        self.speed = 10

        pygame.time.set_timer(E_PLAYER_SHOT_COOLDOWN, DEFAULT_SHOT_SPEED_MS)


    def setShotCooldown(self, shotSpeedMs: int):
        pygame.time.set_timer(E_PLAYER_SHOT_COOLDOWN, 0)
        self.canShoot = True
        pygame.time.set_timer(E_PLAYER_SHOT_COOLDOWN, shotSpeedMs)


    def shoot(self):
        print("PIOU")


    def update(self, events, keys):
        self.direction = pygame.Vector2(0, 0)

        # Check if player can shoot
        for event in events:
            if event.type == E_PLAYER_SHOT_COOLDOWN:
                self.canShoot = True
        
        if keys[pygame.K_SPACE] and self.canShoot:
            self.canShoot = False
            self.shoot()


        # Move player
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1

        self.rect.center += self.direction * self.speed