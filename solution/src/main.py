#! /usr/bin/env python3

import sys, os
import pygame
import getopt
import time

from pong import *
from sock import *
from protocol import *

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

connection = Sock(host, port, server=server, tcp=True, ssl=ssl)
session = Game(server)
multi = Protocol(connection, session)

multi.connection(version)
session.ball.throw()

while True:
    start = time.time()
    for event in pygame.event.get():
        ret = session.event(event)

    if ret not in ("nope", ""):
        multi.send_move_command(ret)
        
    multi.recv_command()
    
    session.draw(server)
    stop = time.time()
    session.delay(stop-start)
