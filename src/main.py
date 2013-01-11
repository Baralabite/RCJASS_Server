'''
Created on 28/11/2012

@author: John
'''

from util import profiler, config, taskmanager, logger
from simulation import simulator
from server import admin
from network import tcpclient, address, packet

class Application:
    def __init__(self):
        self.running = True

    #---Initalization

    def initalize(self):
        self.initalizeCoreModules()        
        self.initalizeProfilers()
        self.initalizeConfiguration()
        self.initalizeSimulation()
        self.initalizeServers()
            
    
    def initalizeCoreModules(self):
        self.configuration = config.Configuration(self, "settings/config.conf")
        self.taskmanager = taskmanager.TaskManager(self, self.configuration)
        self.logger = logger.Logger(self, self.taskmanager, self.configuration)
    
    def initalizeProfilers(self):
        self.profiler = profiler.Profiler(self, "Initalization", self.logger, self.taskmanager)
        self.profiler.startTimer()    
        
    def initalizeConfiguration(self):
        self.networkconfiguration = config.Configuration(self, "settings/server.conf")
        
    def initalizeSimulation(self):
        self.simulation = simulator.Simulator()
        
    def initalizeServers(self):
        self.baseserver = admin.AdminServer(self, self.logger, self.taskmanager, self.networkconfiguration, self.simulation)
    
    #---Loop
    
    def loop(self):
        while self.running:
            pass
     
    #---Deinitalization
    
    def stop(self):
        print "\n\n\n"
        self.running = False
        quit()

if __name__ == '__main__':
    app = Application()
    app.initalize()
    app.loop()
    app.stop()