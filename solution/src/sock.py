#! /usr/bin/env python3

import sys
import socket
import time

BUF_SIZE = 1024

class Sock(object):
    def __init__(self, host, port, server =False, tcp =True, ssl =False):
        self.host = host
        self.port = port
        self.server = server
        self.tcp = tcp
        self.ssl = ssl

        if self.server == True:
            self.wait_client()
        else:
            self.connect_to_server()
        
    def close_connection(self):
        self.data.close()

        if self.server == True:
            self.conn.close()

        print("Connection close")
        sys.exit(1)
        
    def close_connection_with_msg(self, msg):
        self.conn.close()

        if self.server == True:
            self.conn.close()

        print("Connection close:", end=" ")

        if msg in (b'', b'\n', "", "\n"):
            print("with empty data send by peer")
        else:
            print(msg)
        sys.exit(1)
        
    def tcp_connect(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.host, self.port))
        self.data = self.conn

    def connect_to_server(self):
        # if ssl == True:
        #     self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        #     context.load_verify_locations("../authorite/ca.crt")

        #     tmp_conn = tcp_connect(host, port)
        #     self.conn = context.wrap_socket(tmp_conn, server_hostname=host)
        # else:
            self.tcp_connect()

    def wait_client(self):
        self.conn = socket.socket()
        self.conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.conn.bind((self.host, self.port))
        self.conn.listen()
        print("Wait client connection...", end=" ")
        self.data, self.client_addr = self.conn.accept()
        print("Connected !")

    def send_cmd(self, request):
        cmd = request.encode()
        self.data.send(cmd)
    
    def recv_cmd_list(self):
        try:
            answer = self.data.recv(BUF_SIZE)
            if answer in (b'', b'\n'):
                self.close_connection_with_msg(str(answer))
            return answer.decode().split(';')
        except:
            return ['']
    
    def recv_cmd(self):
        answer = self.data.recv(BUF_SIZE)
        if answer in (b'', b'\n'):
            self.close_connection_with_msg(str(answer))    
        return answer.decode()

    def set_recv_no_blocking(self):
        self.data.setblocking(0)
    
    # """ HACK : setblocking as to 0
    #            Save CPU time
    #            Add time out ?
    #            20 ms ? To many lag in game ? 
    # """
    # def recv_cmd(self):
    #     while True:
    #         try:
    #             answer = self.data.recv(BUF_SIZE)
    #             return answer.decode()
    #         except:
    #             sys.pause()
    #             #time.sleep(2) # Sleep 20 ms
