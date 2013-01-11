#Name: configparser.py
#Date: 6:58PM, 27/10/12
#Author: John Board

class Configuration:
    def __init__(self, parent, path):
        self.parent = parent
        try:
            self.file = open(path, "r")
            self.values = {}
            for value in self.file.readlines():
                try:
                    self.values[value.split(":")[0]] = value.split(":")[1].lstrip(" ").rstrip("\n")
                except:
                    if not value.startswith("#") and not value.startswith(" ") and not value.startswith("\n"):
                        print "[SEVERE] Invalid Syntax: "+value
                        quit()
            self.file.close()
        except IOError:
            print "[ERROR] Configuration File Not Found: "+path
            print "[ERROR] Configuration failed to load config file: "+path
            quit()
        except Exception:
            print "[ERROR] Configuration failed to load config file: "+path
            quit()
    
    def getString(self, name):
        try:
            return str(self.values[name])
        except KeyError:
            print "Key ("+name+") Doesn't Exist"
            return ""
        except:
            return ""
      
    def getDictValue(self, name):
        try:
            return eval(self.values[name].replace("=", ":"))
        except KeyError:
            print "Key ("+name+") Doesn't Exist"
            return []
        except:
            return []
        
    def getEvalValue(self, name):
        try:
            return eval(self.values[name])
        except KeyError:
            print "Key ("+name+") Doesn't Exist"
            return []
        except:
            return []
        
    def getFloat(self, name):
        try:
            return float(self.values[name])
        except KeyError:
            print "Key ("+name+") Doesn't Exist"
            return []
        except:
            return []
        
    def getBoolean(self, name):
        try:
            if self.values[name]=="True":
                return True
            elif self.values[name]=="False":
                return False
        except KeyError:
            print "Key ("+name+") Doesn't Exist"
            return None
        except:
            return None
    
    def getInt(self, name):
        try:
            return int(self.values[name])
        except KeyError:
            print "Key ("+name+") Doesn't Exist"
            return -1
        except:
            return -1
        
    def getTuple(self, name):
        try:
            return eval(self.values[name])
        except KeyError:
            print "Key ("+name+") Doesn't Exist"
            return []
        except:
            return []