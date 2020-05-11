from twisted.protocols.basic import LineReceiver
from twisted.internet import protocol
from dirigent import Dirigent
from twisted.internet.protocol import Protocol, ClientFactory


class Server:
    commit_period = 10

    def __init__(self, options):
        self.options = options

class WiesClientFactory(protocol.ClientFactory):
    #protocol = WiesClient
    dirigent = Dirigent("IE wies dirigent")

    def buildProtocol(self, addr):
        return WiesClient(WiesClientFactory.dirigent)

class WiesClient(LineReceiver):
    clientcounter=0;

    def __init__(self,dirigent):
        self.clientid = WiesClient.clientcounter
        self.parameters=dict()
        self.name = "client"+str(self.clientid)
        self.dirigent = dirigent
        WiesClient.clientcounter = WiesClient.clientcounter + 1

    def connectionMade(self):
        self.sendLine( b"?:name" )
        self.dirigent.add_player(self.clientid, self)

    def connectionLost(self, reason):
        self.dirigent.remove_player(self.clientid)

    def lineReceived(self, line):
        line=line.decode("utf-8")
        if len(line)>0 and  line[1]==':':
            command, message = str(line).split(':', 2)
            if command=='!':
                parameter,value = str(message).split('=', 2)
                self.parameters[parameter]=value
                if parameter=="name":
                    self.name=value
            else:
                self.dirigent.receiveMessage(self,line)
        else:
            print (len(line))
            #print(line[1])
            print(line)


        # if self.state == "GETNAME":
        #     self.handle_GETNAME(line)
        # else:
        #     self.handle_COM(line)

    def sendCard(self,card):
        self.sendLine(str("+:%s"%card).encode("utf-8"))
