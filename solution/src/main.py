#! /usr/bin/env python3

import sys, os
import signal
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
# Protocol                                                                     #
################################################################################
class Protocol(object):
    def __init__(self, connection, session):
        self.connected = False
        self.conn = connection
        self.game = session

    def format_cmd(self, act, arg):
        cmd = act + ":"
        for a in arg:
            cmd = cmd + a + ","
        cmd = cmd[:-1] + ";"
        return cmd
    
    def parse_cmd(self, cmd):
        act = cmd[:4]
        arg = cmd[5:-1]
        sarg = arg.split(",")
        return act, sarg
        
    def ping(self):
        self.conn.send_cmd("PING:null;")
        response = self.conn.recv_cmd()
    
    def connection(self):
        global version
        
        if self.conn.server == True:
            cmd = self.format_cmd("CONN", [str(version),
                                           str(self.game.ball.speed),
                                           str(self.game.player_1.max_speed),
                                           str(self.game.player_2.max_speed)])
            self.conn.send_cmd(cmd)
            
            rep = self.conn.recv_cmd()
            if rep != cmd:
                cmd = self.format_cmd("NOPE", ["null"])
                self.conn.close_connection_with_msg("Fail client config: " + rep)
                sys.exit(1)

            cmd = self.format_cmd("OKAY", ["null"])
            self.conn.send_cmd(cmd)
                
        else:
            print("Wait server paramètre ...", end=" ")
            cmd = self.conn.recv_cmd()
            print("Done")
            act, arg = self.parse_cmd(cmd)

            # commande error
            if act != "CONN":
                self.conn.close_connection_with_msg("Invalid command: " + act)
                sys.exit(1)
                
            # incompatible version
            if arg[0] != str(version):
                self.conn.close_connection_with_msg("Incompatible version: " + arg[0])
                sys.exit(1)
                
            self.game.ball.speed = int(arg[1])
            self.game.player_1.max_speed = int(arg[2])
            self.game.player_2.max_speed = int(arg[3])

            cmd = self.format_cmd("CONN", [str(version),
                                           str(self.game.ball.speed),
                                           str(self.game.player_1.max_speed),
                                           str(self.game.player_2.max_speed)])
            self.conn.send_cmd(cmd)

            cmd = self.conn.recv_cmd()
            atc, arg = self.parse_cmd(cmd)

            if atc == "NOPE":
                self.conn.close_connection_with_msg("Incompatible version: " + arg[0])
                sys.exit(1)
            
        self.connected = True
        
        
################################################################################
# Main                                                                         #
################################################################################
host, port, server, ssl = get_option()

connection = Sock(host, port, server=server, tcp=True, ssl=ssl)
session = Game()
multi = Protocol(connection, session)

multi.connection()

session.throw_ball();

while True:
    for e in pygame.event.get():
        # Check for exit
        if e.type == pygame.QUIT:
            connection.close_connection_with_msg("Pygame event quit")
            sys.exit()

        session.update_screen()
        session.delay()
