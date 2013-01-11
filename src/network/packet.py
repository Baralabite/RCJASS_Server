def construct(ID, data):
    if type(data)==type(""):
        data = "'"+data+"'"
    return "["+str(ID)+": "+str(data)+"]"

def parse(data):
    packetID, data = data.lstrip("[").rstrip("]").split(":")
    return {"ID": int(packetID), "VALUE": eval(data)}

def getPacketFromID(id):
    pass

def getPacketID(name):
    pass

#TODO: Turn PacketID into a "3rd-party" file.

class PacketID:
    LOGIN=1
    INVALID_PACKET = 2
    INVALID_PACKET_SYNTAX=3
    DISCONNECT=4
    PING=5
    SHUTDOWN = 6
    RESTART = 7
    START = 8
    RESET = 9
    PAUSE = 10
    RESUME = 11
    INCREASE_SIMULATION_SPEED = 12
    DECREASE_SIMULATION_SPEED = 13
    SET_SIMULATION_SPEED = 14
    GET_SIMULATION_SPEED = 15