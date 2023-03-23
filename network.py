import socket
import threading
from packets import *

class Server:

    def __init__(self, port):
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.clients = []

        self.running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def sendToAll(self, packet):
        for client in self.clients:
            packet.sendTo(self.socket, client)

    def run(self):
        self.socket.bind(("", self.port))

        while self.running:
            try:
                data, addr = self.socket.recvfrom(1024)
                if addr not in self.clients:
                    self.clients.append(addr)
            except OSError:
                exit(0)
            
            received = Packet.parse(data)
            received.onServerReceive(self, addr)

    def close(self):
        self.running = False
        try:
            self.socket.close()
            self.thread.join()
        except:
            print("failed to join thread")

class Client:

    def __init__(self, serverIp, serverPort, game):
        self.game = game

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.connect((serverIp, serverPort))

        self.running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def sendPacket(self, packet):
        packet.send(self.socket)

    def run(self):
        while self.running:
            try:
                received = Packet.parse(self.socket.recv(1024))
                received.onClientReceive(self)
            except OSError:
                exit(0)

    def close(self):
        self.running = False
        try:
            self.socket.close()
            self.thread.join()
        except:
            pass

