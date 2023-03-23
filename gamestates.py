from abc import ABC, abstractmethod

class GameState:

    def __init__(self, game, clearColor, screen):
        self.game = game
        self.clearColor = clearColor
        self.screen = screen

    def clear(self):
        self.screen.fill(self.clearColor)

    @abstractmethod
    def handleEvents(self, events):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self):
        pass
