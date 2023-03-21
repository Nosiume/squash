from abc import ABC, abstractmethod

class GameState:

    def __init__(self, clearColor, screen):
        self.clearColor = clearColor
        self.screen = screen

    def clear(self):
        self.screen.fill(self.clearColor)

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self):
        pass
