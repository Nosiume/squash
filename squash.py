import pygame
from pygame.math import Vector2
from gamestates import GameState

class Racket:

    def __init__(self, x, y):
        self.texture = pygame.image.load("./raquettebleue.gif")
        self.x, self.y = x, y

    def update(self, screen):
        self.hitbox = pygame.Rect(self.x, self.y+5, 20, 80)
        self.top_hitbox = pygame.Rect(self.x, self.y, 20, 5)
        self.bottom_hitbox = pygame.Rect(self.x, self.y+95, 20, 5)

        _, h = pygame.display.get_surface().get_size()
        _, y = pygame.mouse.get_pos()
        if 0 <= y <= h-100:
            self.y = y

    def render(self, screen):
        screen.blit(self.texture, (self.x, self.y))

    def ballCollision(self, ballHitbox):
        if pygame.Rect.collidelist(ballHitbox, [self.top_hitbox, self.bottom_hitbox]) != -1:
            return (1, -1)
        elif pygame.Rect.colliderect(ballHitbox, self.hitbox):
            return (-1, 1)
        return (1, 1)

class Ball:

    def __init__(self, x, y, speed):
        self.texture = pygame.image.load("./balle-jaune.gif")
        self.x, self.y = x, y
        self.speed = speed
        self.direction = (Vector2(1, 1).normalize() * speed)
    
    def update(self, screen, racket):
        self.hitbox = self.texture.get_rect(topleft = (self.x, self.y))

        changes = racket.ballCollision(self.hitbox)
        self.direction.x *= changes[0]
        self.direction.y *= changes[1]
        
        self.x += self.direction.x
        self.y += self.direction.y

        w,h = pygame.display.get_surface().get_size()
        if self.x < 0 or self.x > w-40:
            self.direction.x *= -1
        if self.y < 0 or self.y > h-40:
            self.direction.y *= -1

    def render(self, screen):
        screen.blit(self.texture, (self.x, self.y))

class SquashState(GameState):

    def __init__(self, game, screen):
        super().__init__(game, "cyan", screen)

        self.ball = Ball(200, 100, 5)
        self.racket = Racket(100, 100)

    def handleEvents(self, events):
        pass

    def update(self):
        self.racket.update(self.screen)
        self.ball.update(self.screen, self.racket)

    def render(self):
        self.racket.render(self.screen)
        self.ball.render(self.screen)