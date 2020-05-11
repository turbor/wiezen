import traceback
import socket
from argparse import ArgumentParser
from twisted.internet import reactor,protocol
from twisted.protocols.basic import LineReceiver
from twisted.protocols import basic
from twisted.internet.protocol import Protocol, ClientFactory

from gameserver import Server
from gameserver import WiesClientFactory

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


    parser = ArgumentParser(description="Wies game server")

    parser.add_argument(
        "-a", "--address",
        nargs=1,
        #default="192.168.1.28",
        default=get_IP(),
        #default="127.0.0.1",
        help="Wies server ip address",
    )

    parser.add_argument(
        "-p", "--port",
        nargs=1,
        type=int,
        default=8123,
        help="Wies server port",
    )

    print( parser.print_help() )
    options  = parser.parse_args()
    try:
        address =  options.address
        port =  options.port
        print('Starting server on {0}:{1}'.format(address, port))
        # TODO: remove prints with logging
        reactor.listenTCP(port, WiesClientFactory(), interface=address)
        #reactor.callWhenRunning(self.commit_loop)
        reactor.run()

    except Exception as e:
        # TODO: add inner level exceptions handling
        print( "Server error occurred:".format(e) )
        print( "Traceback:", traceback.format_exc() )

    print("Program ends")
