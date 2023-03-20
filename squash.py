import pygame
import random

class Racket:

    def __init__(self, x, y):
        self.texture = pygame.image.load("./raquettebleue.gif")
        self.x, self.y = x, y

    def update(self, screen):
        self.hitbox = pygame.Rect(self.x, self.y+10, 20, 80)
        self.top_hitbox = pygame.Rect(self.x, self.y, 20, 10)
        self.bottom_hitbox = pygame.Rect(self.x, self.y+90, 20, 10)

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
        self.dx = self.dy = random.choice([-self.speed, self.speed])
    
    def update(self, screen, racket):
        self.hitbox = self.texture.get_rect(topleft = (self.x, self.y))

        changes = racket.ballCollision(self.hitbox)
        self.dx *= changes[0]
        self.dy *= changes[1]
        
        self.x += self.dx
        self.y += self.dy

        w,h = pygame.display.get_surface().get_size()
        if self.x < 0 or self.x > w-40:
            self.dx *= -1
        if self.y < 0 or self.y > h-40:
            self.dy *= -1

    def render(self, screen):
        screen.blit(self.texture, (self.x, self.y))

class Squash:

    def __init__(self, dimensions):
        pygame.init()
        self.screen = pygame.display.set_mode(dimensions)
        self.clock = pygame.time.Clock()
        self.running = True

        self.ball = Ball(200, 100, 5)
        self.racket = Racket(100, 100)


    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.racket.update(self.screen)
        self.ball.update(self.screen, self.racket)
        
    def render(self):
        self.racket.render(self.screen)
        self.ball.render(self.screen)

    def run(self, fps=60):
        while self.running:
            self.handleEvents()

            self.screen.fill("cyan")

            self.update()
            self.render()

            pygame.display.flip()
            self.clock.tick(fps)
        pygame.quit()

def main():
    game = Squash((1280, 720))
    game.run(fps=144)

if __name__ == "__main__":
    main()