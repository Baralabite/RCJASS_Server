class Address:
    def __init__(self, parent, ip, port):
        self.parent = parent
        self.ip = ip
        self.port = port
        
    def getIP(self):
        return self.ip
    
    def setIP(self, ip):
        self.ip = ip
        
    def getPort(self):
        return self.port

    def setPort(self, port):
        self.port = port
        
    def getTuple(self):
        return self.ip, self.port
    
    def getStringAddress(self):
        return str(self.ip)+":"+str(self.port)