#! /usr/bin/env python3

import sys
import pygame
import getopt

from pong import *
from sock import *

HOST = "127.0.0.1"
PORT = 6666

version = 0.1

def usage():
    print("Usage: " + sys.argv[0] + " [options] --port PORT")
    print("  -s, --server     Run as a server")
    print("  -c, --client     Run as a client")
    print("  -h, --host       Host ip addr (optional if localhost)")
    print("  -p, --port       Port number")
    print("  --ssl            Use ssl connection (not inplemented yet)")
    print("  --help           Show this help")
    sys.exit(1)
    
def get_option():
    short_options = "svh:p:"
    long_options = ['server', 'client', 'host=', 'port=', 'ssl', 'help']

    try:
        opts, args = getopt.getopt(sys.argv[1:], short_options, long_options)
    except getopt.GetoptError as err:
        print(err)
        usage()

    host = HOST
    port = PORT
    server = True
    ssl = False
    
    for o, a in opts:
        if o in ("-s", "--server"):
            server = True
        elif o in ("-c", "--client"):
            server = False
        elif o in ("-h", "--host"):
            host = a
        elif o in ("-p", "--port"):
            port = a
        elif o == "--ssl":
            ssl = True
        elif o == "--help":
            usage()
        else:
            print("Unkown option !")
            sys.exit(1)
        
    return host, port, server, ssl

################################################################################
# Main                                                                         #
################################################################################
host, port, server, ssl = get_option()

print(host)
print(port)
print(server)
print(ssl)

session = Game();
session.throw_ball();

while True:
    for e in pygame.event.get():
        # Check for exit
        if e.type == pygame.QUIT:
            sys.exit()

        session.update_screen()
        session.delay()
