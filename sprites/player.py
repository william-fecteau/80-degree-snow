import pygame
from anim.spritesheet import SpriteSheet
from sprites.projectile import Projectile

DEFAULT_SHOT_SPEED_MS = 100
E_PLAYER_SHOT_COOLDOWN = pygame.USEREVENT + 1


class Player(pygame.sprite.Sprite):
    def __init__(self, playerProjectileGroup: pygame.sprite.Group, enemyProjectileGroup: pygame.sprite.Group, gameWorldSurf: pygame.Surface, **kwargs):
        pygame.sprite.Sprite.__init__(self)

        # Loading images
        self.spritesheet = SpriteSheet("res/frosto.png", 64, 64)
        self.frontImage = self.spritesheet.image_at(1, 1, -1)
        self.backImage = self.spritesheet.image_at(1, 0, -1)
        self.states = {
            "FRONT": self.frontImage,
            "BACK": self.backImage
        }
        self.curState = "FRONT"
        self.image = self.states[self.curState]

        self.initialSize = self.image.get_size()
        self.gameWorldSurf = gameWorldSurf
        self.rect = self.image.get_rect(**kwargs)
        self.direction = pygame.math.Vector2()
        self.canShoot = True
        self.isAlive = True
        self.speed = 10
        self.pewSound = pygame.mixer.Sound("res/pew1.mp3")
        self.dieSound = pygame.mixer.Sound("res/playerHit1.mp3")

        self.playerProjectileGroup = playerProjectileGroup
        self.enemyProjectileGroup = enemyProjectileGroup

        # Shooting
        self.projectileSurface = pygame.image.load("res/intro_ball.gif")
        pygame.time.set_timer(E_PLAYER_SHOT_COOLDOWN, DEFAULT_SHOT_SPEED_MS)

        # Hitbox
        self.resetHitbox()


    def resetHitbox(self):
        self.hitbox = pygame.Rect(self.rect.left, self.rect.top, self.rect.width / 2, self.rect.height)
        self.hitbox.center = self.rect.center


    def setShotCooldown(self, shotSpeedMs: int) -> None:
        pygame.time.set_timer(E_PLAYER_SHOT_COOLDOWN, 0)
        self.canShoot = True
        pygame.time.set_timer(E_PLAYER_SHOT_COOLDOWN, shotSpeedMs)


    def shoot(self) -> None:
        if self.canShoot:
            pygame.mixer.Sound.play(self.pewSound)

            projectile = Projectile(self.gameWorldSurf, self.projectileSurface, pygame.Vector2(
                0, -20), bottom=(self.rect.top), centerx=self.rect.centerx)
            self.playerProjectileGroup.add(projectile)
            self.canShoot = False


    def update(self, events, keys, frostLevel: int) -> None:
        self.direction = pygame.Vector2(0, 0)

        # Check if player is dead
        for enemy in self.enemyProjectileGroup.sprites():
            if self.hitbox.colliderect(enemy.rect):
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
        oldState = self.curState
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
            self.curState = "FRONT"
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
            self.curState = "BACK"

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1

        if self.curState != oldState:
            self.image = self.states[self.curState]
            oldPos = self.rect.center
            self.rect = self.image.get_rect(center=oldPos)

        # Scale hitbox in function of frostlevel if it has changed
        self.scalePlayer(frostLevel)

        self.rect.center += self.direction * self.speed

        # If player goes offscreen, dont lmao
        rect = self.gameWorldSurf.get_rect()
        if self.rect.left < rect.left:
            self.rect.left = rect.left
        elif self.rect.right > rect.right:
            self.rect.right = rect.right

        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > rect.height:
            self.rect.bottom = rect.height

        self.hitbox.center = self.rect.center

        

    def scalePlayer(self, frostLevel: int) -> None:
        frostFactor = frostLevel if frostLevel > 3 else 3

        factor = frostFactor/5
        curPos = self.rect.center

        self.image = pygame.transform.scale(self.states[self.curState].copy(), (self.initialSize[0] * factor, self.initialSize[1] * factor))
        self.rect = self.image.get_rect(center=curPos)

        self.resetHitbox()