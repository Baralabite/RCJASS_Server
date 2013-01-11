#Gui Server
#Base (Admin) Server
#Script Server
import sys
sys.path.append("..")
from network import tcpserver, address, packet
from event import events

class AdminServer:
    def onPacketReceived(self, event):
        print "Got Packet!"
        if event.getData()["ID"]==packet.PacketID.SHUTDOWN:
            self.parent.stop()
        elif event.getData()["ID"]==packet.PacketID.START:
            self.simulation.start()
        elif event.getData()["ID"]==packet.PacketID.RESET:
            self.simulation.reset()
        elif event.getData()["ID"]==packet.PacketID.PAUSE:
            self.simulation.pause()
        elif event.getData()["ID"]==packet.PacketID.RESUME:
            self.simulation.resume()
        elif event.getData()["ID"]==packet.PacketID.INCREASE_SIMULATION_SPEED:
            self.simulation.increaseSimulationSpeed(event.getData()["VALUE"])
        elif event.getData()["ID"]==packet.PacketID.DECREASE_SIMULATION_SPEED:
            self.simulation.decreaseSimulationSpeed(event.getData()["VALUE"])
        elif event.getData()["ID"]==packet.PacketID.SET_SIMULATION_SPEED:
            self.simulation.setSimulationSpeed(event.getData()["VALUE"])
        
        
    def onClientConnect(self, event):
            print event.getData().getName(), self.config.getString("AdminUsername")
            print event.getData().getPassword(), self.config.getString("AdminPassword")
            if event.getData().getName()==self.config.getString("AdminUsername") and event.getData().getPassword()==self.config.getString("AdminPassword"):
                event.getData().eventhandler.addEventListener("BaseServer-"+event.getData().getName()+"onPacketReceivedListener", 
                                                              events.EventType.ON_PACKET_RECEIVED,
                                                              self.onPacketReceived)
            else:
                event.setCancelled(True)
                
    def __init__(self, parent, logger, taskmanager, config, simulation):
        self.parent = parent
        self.logger = logger
        self.taskmanager = taskmanager
        self.config = config
        self.simulation = simulation
        
        self.server = tcpserver.TCPServer(self, "BaseServer", self.logger, self.taskmanager, self.config)
        self.server.eventhandler.addEventListener("BaseServer-onClientConnectListener", 
                                                  events.EventType.ON_CLIENT_JOIN, 
                                                  self.onClientConnect)
        ip, port = self.config.getTuple("BaseServerBindAddress")
        self.server.start(address.Address(self, ip, port))