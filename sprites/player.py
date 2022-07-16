import pygame
from sprites.projectile import Projectile

DEFAULT_SHOT_SPEED_MS = 300
E_PLAYER_SHOT_COOLDOWN = pygame.USEREVENT + 1


class Player(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, playerProjectileGroup: pygame.sprite.Group, enemyProjectileGroup: pygame.sprite.Group, gameworld: pygame.Rect, **kwargs):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.gameworld = gameworld
        self.rect = self.image.get_rect(**kwargs)
        self.direction = pygame.math.Vector2()
        self.canShoot = True
        self.isAlive = True
        self.speed = 10
        self.pewSound = pygame.mixer.Sound("res/pew1.mp3")
        self.dieSound = pygame.mixer.Sound("res/playerHit1.mp3")

        self.playerProjectileGroup = playerProjectileGroup
        self.enemyProjectileGroup = enemyProjectileGroup

        self.projectileSurface = pygame.image.load("res/intro_ball.gif")
        pygame.time.set_timer(E_PLAYER_SHOT_COOLDOWN, DEFAULT_SHOT_SPEED_MS)


    def setShotCooldown(self, shotSpeedMs: int) -> None:
        pygame.time.set_timer(E_PLAYER_SHOT_COOLDOWN, 0)
        self.canShoot = True
        pygame.time.set_timer(E_PLAYER_SHOT_COOLDOWN, shotSpeedMs)


    def shoot(self) -> None:
        if self.canShoot:
            pygame.mixer.Sound.play(self.pewSound)

            projectile = Projectile(self.projectileSurface, pygame.Vector2(0, -20), bottom=(self.rect.top), centerx=self.rect.centerx)
            self.playerProjectileGroup.add(projectile)
            self.canShoot = False


    def update(self, events, keys) -> None:
        self.direction = pygame.Vector2(0, 0)

        # Check if player is dead
        for enemy in self.enemyProjectileGroup.sprites():
            if self.rect.colliderect(enemy.rect):
                self.isAlive = False
                pygame.mixer.Sound.play(self.dieSound)
                return

        # Check if player can shoot
        for event in events:
            if event.type == E_PLAYER_SHOT_COOLDOWN:
                self.canShoot = True

        if (keys[pygame.K_SPACE] or keys[pygame.K_z]) and self.canShoot:
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

        # If player goes offscreen, dont lmao
        if self.rect.left < self.gameworld.left:
            self.rect.left = self.gameworld.left
        elif self.rect.right > self.gameworld.right:
            self.rect.right = self.gameworld.right

        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > self.gameworld.height:
            self.rect.bottom = self.gameworld.height
