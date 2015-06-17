from configparser import SafeConfigParser

class Configuration():
    def __init__(self, filename):
        self.filename = filename
        self.config = SafeConfigParser()
        try:
            open(filename, 'r').close()
        except FileNotFoundError:
            print("File doesn't exist!")
            
        self.config.read(filename)
        
        self.dictionary = dict(self.config.items('AUTHENTICATION'))
            
    def AddAtribute(self, Key, Value):
        self.config.set("AUTHENTICATION", Key, Value)
        file = open(self.filename, 'w')
        self.config.write(file)
        self.RefreshAttribute()
     
    def RefreshAttribute(self):
        self.dictionary = dict(self.config.items('AUTHENTICATION'))
        
    
    
    
    