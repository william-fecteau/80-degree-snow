import math
import pygame
from anim.spritesheet import SpriteSheet
from sprites.projectile import Projectile

DEFAULT_SHOT_SPEED_MS = 100
E_PLAYER_SHOT_COOLDOWN = pygame.USEREVENT + 1
PLAYER_LIVES = 3

class Player(pygame.sprite.Sprite):
    def __init__(self, playerProjectileGroup: pygame.sprite.Group, enemyProjectileGroup: pygame.sprite.Group, gameWorldSurf: pygame.Surface, **kwargs):
        pygame.sprite.Sprite.__init__(self)

        self.playerProjectileGroup = playerProjectileGroup
        self.enemyProjectileGroup = enemyProjectileGroup
        self.gameWorldSurf = gameWorldSurf

        # Setup sounds
        self.pewSound = pygame.mixer.Sound("res/pew1.mp3")
        self.dieSound = pygame.mixer.Sound("res/playerHit1.mp3")

        # Setup images
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
        self.rect = self.image.get_rect(**kwargs)

        self.direction = pygame.math.Vector2()

        self.isAlive = True
        self.lives = PLAYER_LIVES
        self.speed = 10

        # Frost setup
        self.oldFrost = 10
        self.scaleDamage(self.oldFrost)

        self.resetHitbox()
        # Shooting
        self.canShoot = True
        self.projectileSurface = pygame.image.load(
            "res/frostBullet.png")
        pygame.time.set_timer(E_PLAYER_SHOT_COOLDOWN, DEFAULT_SHOT_SPEED_MS)

        # Hitbox
        self.resetHitbox()

    def die(self):
        self.lives -= 1
        # self.rect.centerx = self.gameWorldSurf.get_width() / 2
        # self.rect.bottom = self.gameWorldSurf.get_height()
        self.resetHitbox()
        self.isAlive = False
        pygame.mixer.Sound.play(self.dieSound)


    def resetHitbox(self):
        self.hitbox = pygame.Rect(
            self.rect.left, self.rect.top, self.rect.width / 2, self.rect.height)
        self.hitbox.center = self.rect.center


    def setShotCooldown(self, shotSpeedMs: int) -> None:
        pygame.time.set_timer(E_PLAYER_SHOT_COOLDOWN, 0)
        self.canShoot = True
        pygame.time.set_timer(E_PLAYER_SHOT_COOLDOWN, shotSpeedMs)

    def shoot(self) -> None:
        if self.canShoot:
            pygame.mixer.Sound.play(self.pewSound)

            projectile = Projectile(self.gameWorldSurf, self.projectileSurface, pygame.Vector2(
                0, -20), self.projectileDamage, bottom=(self.rect.top), centerx=self.rect.centerx)
            self.playerProjectileGroup.add(projectile)
            self.canShoot = False

    def update(self, events, keys, frostLevel: int) -> None:
        self.direction = pygame.Vector2(0, 0)

        # Check if player is dead
        if self.isAlive:
            for enemy in self.enemyProjectileGroup.sprites():
                if self.hitbox.colliderect(enemy.rect):
                    self.die()
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
        if oldState != self.curState or self.oldFrost != frostLevel:
            self.scalePlayer(frostLevel)
            self.scaleDamage(frostLevel)
            self.oldFrost = frostLevel

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

    def scaleDamage(self, frostLevel) -> None:
        # frost 1 => 30 damage
        # frost 10 => 10 damage
        self.projectileDamage = math.floor((20/9) * frostLevel + (70/9))

    def scalePlayer(self, frostLevel: int) -> None:
        frostFactor = frostLevel if frostLevel > 3 else 3

        factor = frostFactor/5
        curPos = self.rect.center

        self.image = pygame.transform.scale(self.states[self.curState].copy(
        ), (self.initialSize[0] * factor, self.initialSize[1] * factor))
        self.rect = self.image.get_rect(center=curPos)

        self.resetHitbox()
