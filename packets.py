from abc import ABC, abstractmethod
import pickle

class Packet(ABC):

    def __init__(self, id):
        self.id = id
        self.rawData = b''

    def setData(self, rawData):
        self.rawData = rawData

    def send(self, socket):
        socket.send(self.id + self.rawData)

    def sendTo(self, socket, target):
        socket.sendto(self.id + self.rawData, target)

    @abstractmethod
    def onClientReceive(self, client):
        pass

    @abstractmethod
    def onServerReceive(self, server, origin):
        pass

    """ STATIC METHODS """
    def parse(packetData):
        id = packetData[:2]
        data = packetData[2:]

        packet = PACKET_TYPES[id]()
        packet.setData(data)

        return packet

class ToggleReadyPacket(Packet):

    def __init__(self, player=None):
        super().__init__(b'02')

        #If we do have packet body for the player we create byte payload
        if player:
            self.setData(pickle.dumps(player))
    
    def onClientReceive(self, client):
        if not self.rawData:
            print("ToggleReadyPacket [Client Receive] - I must have gotten lost there woopsie")
            return
        origin = pickle.loads(self.rawData)
        client.game.states['WaitingRoom'].toggleReady(origin)
    
    def onServerReceive(self, server, origin):
        #Update ready state on everyone's pov
        server.sendToAll(ToggleReadyPacket(player=origin))

class PlayerListPacket(Packet):

    def __init__(self, playerList=None):
        super().__init__(b'01')

        #If we have data set we create byte payload
        if playerList:
            self.setData(pickle.dumps(playerList))
    
    def onClientReceive(self, client):
        playerList = pickle.loads(self.rawData)
        for player in playerList:
            client.game.states['WaitingRoom'].addPlayer(player)
    
    def onServerReceive(self, server, origin):
        #shouldn't happen but in case it does we just dispatch it to update the clients
        server.sendToAll(self)

class ConnectionPacket(Packet):

    def __init__(self):
        super().__init__(b'00')
    
    def onClientReceive(self, client):
        print("[+] A player arrived !")
    
    def onServerReceive(self, server, origin):
        #When we receive connection we update every player's player list
        server.sendToAll(PlayerListPacket(playerList=server.clients))
        server.sendToAll(self)

PACKET_TYPES = {
    b'00': ConnectionPacket,
    b'01': PlayerListPacket,
    b'02': ToggleReadyPacket
}