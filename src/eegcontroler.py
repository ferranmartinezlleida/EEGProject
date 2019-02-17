from pythonosc import dispatcher, osc_server


class OSCcontroler:

    def __init__(self,modulardispatcher,host ='127.0.0.1',port = 5000):
        self.host = host
        self.port = port
        self.dispatcher = modulardispatcher.getDispatcher()

    def setPort(self,port):
        self.port = port

    def setHost(self,host):
        self.host = host

    def buildServer(self):
        self.server = osc_server.OSCUDPServer((self.host, self.port), self.dispatcher)

    def initiate_server(self):
        self.server.serve_forever()

    def shutdown_server(self):
        self.server.shutdown()



class ModularDispatcher:

    def __init__(self,module):
        self.module = module
        self.dispatcher = dispatcher.Dispatcher()
        self.configured = False

    def getDispatcher(self):

        if not self.configured:
                self.configure()
                self.configured = True
        return self.dispatcher

    def configured(self):
        return self.configured


    def mapPath(self, path, function):
        self.dispatcher.map(path, function)


    def mapSameFunctionToPaths(self, function,paths):
        for path in paths:
            self.dispatcher.map(path, function)

    def configure(self):
        self.module.configure(self)
        self.configured = True