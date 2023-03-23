from gamestates import GameState

import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame.math import Vector2

from random import randint

from network import Server, Client
from packets import ConnectionPacket, ToggleReadyPacket

class Particle:

    def __init__(self, rect, color):
        self.rect = rect
        self.color = color
        self.direction = Vector2(randint(-100, 100), randint(-100, 100)).normalize() * 5

    def update(self):
        w, h = pygame.display.get_surface().get_size()
        rectX, rectY = self.rect.center
        if rectX <= 0 or rectX >= w:
            self.direction.x *= -1
        if rectY <= 0 or rectY >= h:
            self.direction.y *= -1

        self.rect = self.rect.move(self.direction.x, self.direction.y)

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        
class WaitingRoom(GameState):

    def __init__(self, game, screen):
        super().__init__(game, "yellow", screen)

        self.players = {}

        self.titleFont = pygame.font.Font("./font.ttf", size=100)
        self.textFont = pygame.font.Font("./font.ttf", size=40)

        self.readyButton = Button(
            screen,
            1000, 550, 150, 100,
            text='Ready',
            inactiveColour=(62, 212, 99),
            hoverColour=(125, 229, 150),
            pressedColor=(94, 163, 111),
            textColour=(255, 255, 255),
            font = self.textFont,
            radius=100,
            onClick = lambda: self.game.client.sendPacket(ToggleReadyPacket())
        )

    def addPlayer(self, addr):
        if len(self.players) != 2 and addr not in self.players:
            self.players[addr] = False

    def toggleReady(self, addr):
        self.players[addr] = not self.players[addr]

    def handleEvents(self, events):
        pygame_widgets.update(events)

    def update(self):
        pass

    def render(self):
        title = self.titleFont.render("Waiting Room", True, "white")
        self.screen.blit(title, (275, 50))

        # Split the screen
        pygame.draw.rect(self.screen, "gray", (600, 200, 10, 500))

        # Draw players
        for i, player in enumerate(self.players.keys()):
            playerText = self.textFont.render("Player " + str(i), True, "white")
            readyText = self.textFont.render("Ready" if self.players[player] else "Not Ready", True, "white")
            self.screen.blit(playerText, (100, 250 + i*150))
            self.screen.blit(readyText, (700, 250 + i*150))

        # Draw button
        self.readyButton.draw()

class MenuState(GameState):

    def __init__(self, game, screen):
        super().__init__(game, "yellow", screen)
        self.titleFont = pygame.font.Font("./font.ttf", size=100)
        self.widgetFont = pygame.font.Font("./font.ttf", size=50)

        w, h = pygame.display.get_surface().get_size()
        self.particles = []
        for i in range(25):
            p = Particle(
                pygame.Rect(0, 0, 20, 20).move(
                    randint(0, w),
                    randint(0, h)
                ),
                (62, 224, 180)
            )
            self.particles.append(p)

        self.hostButton = Button(
            screen,
            375, 300, 500, 100,
            text='Host Game',
            inactiveColour=(62, 212, 99),
            hoverColour=(125, 229, 150),
            pressedColor=(94, 163, 111),
            textColour=(255, 255, 255),
            font = self.widgetFont,
            radius=100,
            onClick = self.hostGame
        )
        
        self.joinButton = Button(
            screen,
            375, 450, 500, 100,
            text='Join Game',
            inactiveColour=(62, 212, 99),
            hoverColour=(125, 229, 150),
            pressedColor=(94, 163, 111),
            textColour=(255, 255, 255),
            font = self.widgetFont,
            radius=100,
            onClick = self.joinGame
        )

    def hostGame(self):
        self.game.server = Server(1234)
        self.game.client = Client("localhost", 1234, self.game)
        self.game.client.sendPacket(ConnectionPacket())

        self.game.changeState("WaitingRoom")

    def joinGame(self):
        # TODO: Make an interactive state to type ip and port
        import pyautogui
        ip = pyautogui.prompt(text='Enter an IP Address : ', title='IP Prompt', default='localhost')
        port = int(pyautogui.prompt(text='Enter a PORT : ', title='Port Prompt', default='1234'))
        self.game.client = Client(ip, port, self.game)
        self.game.client.sendPacket(ConnectionPacket()) #TODO: maybe put that line in client class

        self.game.changeState("WaitingRoom")

    def handleEvents(self, events):
        pygame_widgets.update(events)

    def update(self):
        for particle in self.particles:
            particle.update()

    def render(self):
        for particle in self.particles:
            particle.render(self.screen)

        self.hostButton.draw()
        self.joinButton.draw()

        title = self.titleFont.render("Squash", True, "white")
        self.screen.blit(title, (425, 100))