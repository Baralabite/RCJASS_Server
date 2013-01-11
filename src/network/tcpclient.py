import socket, packet

class Client:
    def __init__(self, name, logger, taskmanager, config):
        self.name = name
        self.logger = logger
        self.taskmanager = taskmanager
        self.config = config
        self.onRecievePacketFunc = None
        self.onExitPacketFunc = None
    
    def connect(self, addr, username, password):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(addr.getTuple())
        self.send(packet.PacketID.LOGIN, (username, password))
        
    def rxLoop(self):
        while 1:
            pkt = packet.parse(self.socket.recv(self.config.getInt("NetworkBuffer")))
            if self.onRecievePacketFunc!=None:
                self.onRecievePacketFunc(pkt)
            else:
                self.packets.append(pkt)
                
    def getPackets(self):
        pkts = self.packets
        self.packets = []
        return pkts
            
    def setOnReceiveListener(self, func):
        self.onRecievePacketFunc = func
        
    def setOnExitListener(self, func):
        self.onRecievePacketFunc = func
    
    def disconnect(self):
        self.socket.close()
    
    def send(self, id_, data):
        self.socket.send(packet.construct(id_, data))