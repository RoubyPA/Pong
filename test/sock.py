#! /usr/bin/python3

import socket

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
    
    def tcp_connect(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.host, self.port))

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

        self.client, self.client_addr = self.conn.accept()
        
    def close_connection(self):
        self.conn.close()
        print("Connection close")
    
    def get_str_from_socket(self):
        answer = self.conn.recv(BUF_SIZE)
        return answer.decode()
