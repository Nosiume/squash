import pygame
from squash import SquashState

class Squash:

    def __init__(self, dimensions):
        pygame.init()

        self.screen = pygame.display.set_mode(dimensions)
        self.clock = pygame.time.Clock()
        self.running = True

        self.states = {
            "Squash": SquashState(self.screen)
        }
        self.currentState = "Squash"


    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def run(self, fps=60):
        while self.running:
            self.handleEvents()

            state = self.states[self.currentState]
            state.clear()
            state.update()
            state.render()

            pygame.display.flip()
            self.clock.tick(fps)
        pygame.quit()

def main():
    game = Squash((1280, 720))
    game.run(fps=144)

if __name__ == "__main__":
    main()