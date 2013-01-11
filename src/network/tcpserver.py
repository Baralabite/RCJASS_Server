import socket, packet, address, sys
sys.path.append("..")
from event import events, eventhandler

class TCPServer:
    def __init__(self, parent, name, logger, taskmanager, config):
        self.parent = parent
        self.name = name
        self.logger = logger
        self.taskmanager = taskmanager
        self.config = config
        self.clients = {}
        self.eventhandler = eventhandler.EventHandler(self, self.name, self.logger, self.taskmanager)
        
        
    def start(self, addr):
        self.address = addr
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except:
            self.logger.printErrorStack()
            self.logger.error("Could not start "+self.getName()+"-TCPServer on "+self.getAddress().getStringAddress()+".")
        self.socket.bind(self.address.getTuple())
        self.taskmanager.addThread(self.getName()+"-ConnectionLoop", self.connectionLoop)
        self.logger.debug(self.getName()+"-TCPServer started on "+self.address.getStringAddress())
    
    def connectionLoop(self):
        while 1:
            self.socket.listen(1)
            conn, addr = self.socket.accept()
            self.logger.debug("Incoming Connection From: "+addr[0])
            addr = address.Address(self, addr[0], addr[1])
            
            client = Client(self, conn, addr, self.logger, self.taskmanager, self.config)
            
            event = events.OnClientJoin(client)
            self.eventhandler.callEvents(events.EventType.ON_CLIENT_JOIN, event)
            if event.isCancelled():
                self.disconnectClient(client.getName())
            else:
                self.clients[client.getName()] = client
            
    def getClient(self, name):
        return self.clients[name]
    
    def getClients(self):
        return self.clients
    
    def getClientNames(self):
        return self.clients.keys()
    
    def getNumberOfClients(self):
        return len(self.clients)
    
    def getName(self):
        return self.name
    
    def getAddress(self):
        return self.address
    
    def disconnectClient(self, name):
        self.getClient(name).disconnect()
        del self.clients[name]
    
    def stop(self):
        pass
        
class Client:
    def __init__(self, parent, connection, addr, logger, taskmanager, config):
        self.parent = parent
        self.connection = connection
        self.address = addr
        self.logger = logger
        self.taskmanager = taskmanager
        self.config = config
        self.name = ""
        self.password = ""
        self.packets = []
        self.running = True
        
        while 1:
            data = self.connection.recv(self.config.getInt("NetworkBuffer"))
            try:    
                pkt = packet.parse(data)
                if pkt["ID"]==packet.PacketID.LOGIN:
                    self.name = pkt["VALUE"][0]
                    self.password = pkt["VALUE"][1]
                    break
            except:
                self.logger.error("Invalid Packet Recieved from "+self.getAddress().getStringAddress()+": "+str(data))
        self.logger.debug("Client Connected with the username '"+self.getName()+"' and the password '"+self.password+"'")
        self.eventhandler = eventhandler.EventHandler(parent, self.name+"-Client", self.logger, self.taskmanager)
        self.taskmanager.addThread(self.getName(), self.rxLoop)
                
    def getConnection(self):
        return self.connection
    
    def getAddress(self):
        return self.address
    
    def getName(self):
        return self.name
    
    def getPassword(self):
        return self.password
    
    def send(self, ID, Data):
        pkt = packet.construct(ID, Data)
        try:
            self.connection.send(pkt)
            return True
        except:
            return False
        
    def rxLoop(self):
        while self.running:
            pkt = {"ID": None, "VALUE": None}
            data = ""
            try:
                try:                
                    #data = self.connection.recv(self.config.getInt("NetworkBuffer"))
                    while data != "[":
                        data = self.connection.recv(1)
                    rx = ""
                    while rx != "]":
                        rx = self.connection.recv(1)
                        data = data + rx                
                    if self.config.getBoolean("DebugMode"):
                        self.logger.debug("Received Packet from the client "+self.getName()+": "+data)    
                    try:
                            pkt = packet.parse(data)
                    except:
                        self.logger.error("Packet Parsing Failure.")
                        self.send(packet.PacketID.INVALID_PACKET_SYNTAX, None)
                except:
                    if not self.send(packet.PacketID.PING, None):
                        self.logger.error("Packet Reception Failure.")
                        self.logger.debug("'"+self.getName()+"' Disconnected.")
                        self.parent.disconnectClient(self.getName())
                        break
                
                if pkt["ID"]==packet.PacketID.DISCONNECT:
                    self.logger.debug("'"+self.getName()+"' Disconnected.")
                    self.parent.disconnectClient(self.getName())
                    break
                elif pkt["ID"]==packet.PacketID.PING:
                    self.send(packet.PacketID.PING, None)
                else:
                    event = events.OnPacketRecieved(pkt)
                    self.eventhandler.callEvents(events.EventType.ON_PACKET_RECEIVED, event)
                    
            except:
                self.logger.printErrorStack()
            
    def getPackets(self):
        pkt = self.packets
        self.packets = []
        return pkt
        
    def disconnect(self):
        self.connection.close()
        self.running = False
