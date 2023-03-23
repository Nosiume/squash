import pygame
from squash import SquashState
from menu import MenuState, WaitingRoom

class Squash:

    def __init__(self, dimensions):
        pygame.init()
        pygame.font.init()

        self.server = None
        self.client = None

        self.screen = pygame.display.set_mode(dimensions)
        self.clock = pygame.time.Clock()
        self.running = True

        self.states = {
            "Menu": MenuState(self, self.screen),
            "WaitingRoom": WaitingRoom(self, self.screen),
            "Squash": SquashState(self, self.screen)
        }
        self.currentState = self.states["Menu"]


    def changeState(self, name):
        self.currentState = self.states[name]

    def handleEvents(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
        self.currentState.handleEvents(events)

    def run(self, fps=60):
        while self.running:
            self.handleEvents()

            self.currentState.clear()
            self.currentState.update()
            self.currentState.render()

            pygame.display.update()
            pygame.display.flip()
            self.clock.tick(fps)

        if self.server: 
            self.server.close()
        if self.client:
            self.client.close()
        pygame.quit()

def main():
    game = Squash((1280, 720))
    game.run(fps=144)

if __name__ == "__main__":
    main()