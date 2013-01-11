#Name: events.py
#Date: 6:58PM, 27/10/12
#Author: John Board

import sys
sys.dont_write_bytecode = True

"""
File for common events, and custom events.
"""

#---[Event Definitions]---#

#This is really just an enum of event types, not required, just makes the code
#prettier

#
        
            
#---[Templates]---#

class Event:
    def __init__(self):
        pass
    
class EventWithData(Event):
    def __init__(self, data):
        self.data = data
        
    def setData(self, data):
        self.data = data
        
    def getData(self):
        return self.data

class CancellableEvent(Event):
    def __init__(self):
        Event.__init__(self)
        self.cancelled = False
    def isCancelled(self):
        return self.cancelled
    
    def setCancelled(self, cancelled):
        self.cancelled = cancelled
        
class CancellableEventWithData(EventWithData):
    def __init__(self, data):
        EventWithData.__init__(self, data)
        self.cancelled = False
    def isCancelled(self):
        return self.cancelled
    
    def setCancelled(self, cancelled):
        self.cancelled = cancelled
        
        

#---[Custom Events]---#

class EventType:
    ON_PACKET_RECEIVED = 1
    ON_CLIENT_JOIN = 2
    
class OnPacketRecieved(EventWithData):
    def __init__(self, data):
        EventWithData.__init__(self, data)
        
class OnClientJoin(CancellableEventWithData):
    def __init__(self, data):
        CancellableEventWithData.__init__(self, data)
        