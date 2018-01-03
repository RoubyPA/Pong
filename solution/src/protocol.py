#! /usr/bin/env python3

import sys, os

from pong import *
from sock import *

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
        
        if cmds == []:
            return "none"

        for cmd in cmds:
            if cmd not in ('', '\n'):
                act, arg = self.parse_cmd(cmd)
            
                if act == "MOVE":
                    self.game.player_2.move_paddle(arg[0])
                elif act == "THRW":
                    self.game.ball.throw()
                    self.game.score.player_2 = int(arg[0])
                    self.game.score.player_1 = int(arg[1])
                    self.game.player_2.coords[0] = int(arg[2])
                    self.game.player_2.coords[1] = int(arg[3])
                    self.game.player_1.coords[0] = int(arg[4])
                    self.game.player_1.coords[1] = int(arg[5])
                    self.game.ball.vx = int(arg[6])
                    self.game.ball.vy = int(arg[7])
                elif act == "PING":
                    self.conn.send_cmd(self.format_cmd("PONG", ["null"]))
                else:
                    self.conn.close_connection_with_msg("Commande Unkown !")
                    sys.exit(1)


    def send_throw_command(self):
        "Syncronisation des positions et lancement reinit position balle"
        cmd = self.format_cmd("THRW",
                              [str(self.game.score.player_1),
                               str(self.game.score.player_2),
                               str(self.game.player_1.coords[0]),
                               str(self.game.player_1.coords[1]),
                               str(self.game.player_2.coords[0]),
                               str(self.game.player_2.coords[1]),
                               str(self.game.ball.vx),
                               str(self.game.ball.vy)])
        self.conn.send_cmd(cmd)
            
    def send_move_command(self, direction):
        if self.game.player_1.state != direction:
            cmd = self.format_cmd("MOVE", [direction])
            self.conn.send_cmd(cmd)
            self.game.player_1.state = direction
                    
    def calcul_ping(self):
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
        
    def connection(self, version):
        "Séquance de connection entre le server et le client, à besion de la version du programme pour vérifier la compatiblilité"
        # global version
        
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
        time.sleep(0.5)
        self.calcul_ping()
        self.game_mode()

    def game_mode(self):
        self.conn.set_recv_no_blocking()
        
