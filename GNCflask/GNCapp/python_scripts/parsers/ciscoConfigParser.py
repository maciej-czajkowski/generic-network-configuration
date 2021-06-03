# --- this class handles the parsing of cisco config file
class  ciscoConfigParser:
    config = []
    def __init__(self):
        #  --- open file and read all lines
        self.config = []
        
    def parseConfig(self, filename):
        self.filename = filename
        lines = open(self.filename, "r").readlines()
        configEntry = []
        for line in lines:
            if line != '!\n':
                configEntry.append(line.replace('\n', ''))
            else:
                # print(configEntry)
                self.config.append(configEntry.copy())
                # print(self.config)
                configEntry.clear()    
            