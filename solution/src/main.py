#! /usr/bin/env python3

import sys, os
import signal
import pygame
import getopt
import _thread
import time

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
        self.conn = connection
        self.connected = False
        self.game = session

    def format_cmd(self, act, arg):
        cmd = act + ":"
        for a in arg:
            cmd = cmd + a + ","
        cmd = cmd[:-1] + ";"
        print(cmd)
        return cmd
    
    def parse_cmd(self, cmd):
        act = cmd[:4]
        if cmd[-1:] == ';':
            arg = cmd[5:-1]
        else:
            arg = cmd[5:]
        sarg = arg.split(",")
        return act, sarg

    def recv_command(self):
        cmds = self.conn.recv_cmd_list()

        for cmd in cmds:
            if cmd not in ('', '\n'):
                act, arg = self.parse_cmd(cmd)
            
                if act == "MOVE":
                    self.game.player_2.move_paddle(arg[0])
                    print(arg[0])
                # elif act == "SYNC":
                #     print(act)
                elif act == "PING":
                    self.conn.send_cmd(self.format_cmd("PONG", ["null"]))
                else:
                    self.conn.close_connection_with_msg("Commande Unkown !")
                    sys.exit(1)

    def send_move_command(self, direction):
        if self.game.player_1.state != direction:
            cmd = self.format_cmd("MOVE", [direction])
            self.conn.send_cmd(cmd)
            self.game.player_1.state = direction
                    
    def calcul_ping(self):
        # On sais jamais ¯\_(ツ)_/¯
        if self.connected == False:
            sys.exit(1)
            
        if self.conn.server == True:
            cmd = self.format_cmd("PING", ["null"])
            start = time.time() # Start timer
            self.conn.send_cmd(cmd) # Send ping cmd
            cmd = self.conn.recv_cmd() # Wait pong cmd

            # Fail ping
            if cmd[:4] != "PONG":
                self.conn.close_connection_with_msg("Fail PING: " + cmd)
                sys.exit(1)
            stop = time.time() # Stop timer
            
            self.ping = stop - start
            print("Ping : ", self.ping)
        else:
            pong = self.format_cmd("PONG", ["null"])
            # time.sleep(0.03) # add 30 ms ping <-- To delete
            cmd = self.conn.recv_cmd() # Wait ping cmd
            # Not a PING
            if cmd[:4] != "PING":
                cmd = self.format_cmd("NOPE", ["null"])
                self.conn.close_connection_with_msg("Fail PING: " + cmd)
                sys.exit(1)

            self.conn.send_cmd(pong) # Send pong cmd
        
    def connection(self):
        global version
        
        if self.conn.server == True:
            cmd = self.format_cmd("CONN", [str(version),
                                           str(self.game.ball.vx),
                                           str(self.game.ball.vy),
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

            # Commande error
            if act != "CONN":
                self.conn.close_connection_with_msg("Invalid command: " + act)
                
            # Incompatible version
            if arg[0] != str(version):
                self.conn.close_connection_with_msg("Incompatible version: " + arg[0])

            # Set game paraméters
            self.game.ball.vx = int(arg[1])
            self.game.ball.vy = int(arg[2])
            self.game.player_1.max_speed = int(arg[3])
            self.game.player_2.max_speed = int(arg[4])

            cmd = self.format_cmd("CONN", [str(version),
                                           str(self.game.ball.vx),
                                           str(self.game.ball.vy),
                                           str(self.game.player_1.max_speed),
                                           str(self.game.player_2.max_speed)])
            self.conn.send_cmd(cmd)

            cmd = self.conn.recv_cmd()
            atc, arg = self.parse_cmd(cmd)

            if atc == "NOPE":
                self.conn.close_connection_with_msg("Incompatible version: " + arg[0])
                
        self.connected = True

    def game_mode(self):
        self.conn.set_recv_no_blocking()
        
################################################################################
# Main                                                                         #
################################################################################
host, port, server, ssl = get_option()

connection = Sock(host, port, server=server, tcp=True, ssl=ssl)
session = Game(server)
multi = Protocol(connection ,session)

multi.connection()
time.sleep(0.5)
multi.calcul_ping()
multi.game_mode()

#session.ball.throw()

while True:
    for event in pygame.event.get():
        ret = session.event(event)

    if ret not in ("nope", ""):
        multi.send_move_command(ret);
    multi.recv_command()
    
    session.draw()
    session.delay()
