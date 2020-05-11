import traceback
from argparse import ArgumentParser
from twisted.internet import reactor, protocol
from twisted.protocols import basic
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.python import log
from twisted.protocols.basic import LineReceiver
from interactivedeck import InteractiveDeck
import sys
import socket

from gameserver import Server

inputlist=[]
name='unknown'

class ClientProtocol(LineReceiver):
    def __init__(self):
        self.deck = InteractiveDeck()
        self.deck.clear()

    def lineReceived(self, data):
        log.msg('Data received {}'.format(data))
        # self.transport.loseConnection()
        data = data.decode("utf-8")
        if data[1] ==':':
            command,message = data.split(':',1)
            self.handlecommand(command,message)
        else:
            #probably text for the end-user...
            print(data)

    def connectionMade(self):
        # data = 'Hello, Server!'
        # self.transport.write(data.encode())
        # log.msg('Data sent {}'.format(data))
        log.msg('Connection made')
        pass

    def connectionLost(self, reason):
        log.msg('Lost connection because {}'.format(reason))

    def returnhand(self):
        cards=','.join(self.deck.cards)
        self.sendLine('^:RETURNHAND={}'.format(cards).encode("utf-8"))
        self.deck.clear()

    def handlelongcommands(self, command):
        if command == "RETURNHAND":
            self.returnhand()
        elif command == "TRIKFINISHED":
            pass
        elif command == "GAMEFINISHED":
            pass
        else:
            log.msg('Unknown command {}'.format(command))

    def returnparameter(self,parameter):
        val=''
        if parameter=="name":
            global name
            val=name
        self.sendLine('!:{}={}'.format(parameter,val).encode("utf-8"))
        log.msg(('!:{}={}'.format(parameter,val).encode("utf-8")))


    def handlecommand(self, command,message):
        if command=="+":
            self.deck.addCard(message)
        elif command=="B":
            keuze = self.pickFromMenu(message)
            self.sendLine("B:{}".format(keuze).encode("utf-8"))
        elif command=="-":
            for i in range(int(message)):
                keuze = self.deck.userPickCard()
                self.deck.removeCard(keuze)
                self.sendLine("+:{}".format(keuze).encode("utf-8"))
        elif command == "^":
            #longformatcommands
            self.handlelongcommands(message)
        elif command == "P":
            #inform player has played given card
            player, card = message.split(',', 1)
            print("{} has played {}".format(player,self.deck.card2str(card)))
        elif command=="?":
            self.returnparameter(message)
        else:
            log.msg('Unknown command {}'.format(command))

    def getinput(self,message):
        global inputlist
        if len(inputlist)>0:
            inp=inputlist.pop(0)
            print("{} : predefined answer {}".format(message,inp))
            return inp
        else:
            return input(message)

    def pickFromMenu(self,message):
        # first display current cards in hand
        self.deck.display()
        items = message.split(":")
        while True:
            try:
                for nr,line in enumerate(items):
                    print("{0:>2d}. {1}".format(nr+1,line))
                userInput = int(self.getinput("Kies nummer aub : "))
            except ValueError:
                print("Not an integer! Try again.")
                continue
            except KeyboardInterrupt:
                print("KeyboardInterrupt occured")
                sys.exit(1)
                raise
            else:
                if userInput < 1 or userInput > len(items):
                    print("Geen geldig nummer")
                    continue
                return items[userInput - 1]

class ClientFactory(ClientFactory):
    def startedConnecting(self, connector):
        log.msg('Started to connect.')

    def buildProtocol(self, addr):
        log.msg('Connected.')
        return ClientProtocol()

    def clientConnectionLost(self, connector, reason):
        log.msg('Lost connection. Reason: {}'.format(reason))

    def clientConnectionFailed(self, connector, reason):
        log.msg('Lost failed. Reason: {}'.format(reason))

def get_IP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip=s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


if __name__ == "__main__":
    parser = ArgumentParser(description="Wies game user client")

    parser.add_argument(
        "-a", "--address",
        nargs=1,
        #default="192.168.1.28",
        #default="127.0.0.1",
        default=get_IP(),
        help="Wies server ip address",
    )

    parser.add_argument(
        "-p", "--port",
        nargs=1,
        type=int,
        default=8123,
        help="Wies server port",
    )

    parser.add_argument(
        "-n", "--name",
        nargs=1,
        type=str,
        default='unknown',
        help="player name",
    )

    parser.add_argument(
        "-i", "--input",
        nargs=1,
        type=str,
        default='1',
        help="predefined list of choices(comma separated) useful for debugging",
    )

    print(parser.print_help())
    options = parser.parse_args()
    try:
        address = options.address
        port = options.port
        name = options.name
        inputlist = options.input.split(',')
        print('Connecting to server on {0}:{1}'.format(address, port))
        log.startLogging(sys.stdout)
        # TODO: remove prints with logging
        reactor.connectTCP(address, port, ClientFactory())
        # reactor.callWhenRunning(self.commit_loop)
        reactor.run()

    except Exception as e:
        # TODO: add inner level exceptions handling
        print("An error occurred:".format(e))
        print("Traceback:", traceback.format_exc())

    print("Program ends")
