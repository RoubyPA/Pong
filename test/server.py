#!/usr/bin/python3
import socket
# import ssl

HOST= '127.0.0.1'
PORT= 7777
BUFSIZE= 1024

version = 0.1
ball_speed_x = 4
ball_speed_y = 4
r_speed = 2

# ssl context
# context = ssl.create_default_context (ssl.Purpose.CLIENT_AUTH)
# context.load_cert_chain("../serveur/server.crt", keyfile="../serveur/server.key")

# echo server
def star(conn):

    connected = 0

    while True:
        data = conn.recv(BUFSIZE)

        # disconnect 
        if data == b'' or data == b'\n' : break

        # decode msg
        msg = data.decode()
        print(msg)

        # if no client connected
        if connected == 0:
            if str(msg).find("CONN:") == 0:
                # generation of connection msg
                rep = "CONN:" + str(version) + "," + str(ball_speed_x) + "," + str(ball_speed_y) + "," + str(r_speed) + ";"
                
                # if connection message is same as recv message
                if str(msg).find(rep) == 0:
                    conn.send(rep.encode())
                
                    data = conn.recv(BUFSIZE)
                    msg = data.decode()
                    print(msg)

                    if str(msg).find("OKAY:null;") == 0:
                        connected = 1
                    else:
                        conn.send(b"NOPE:null;")
                        break # close connection
                else:
                    conn.send(b"NOPE:null;")
                    break # close connection
            else:
                conn.sendall(b"NOPE:null;")
                break # close connection
        else:
            # parse msg
            if str(msg).find("PING:null;") == 0:
                conn.send(b"PONG:null;")
            # TODO cmd START
            # TODO cmd Sync
            # TODO cmd MOVE (UP, DOWN, STOP)
            else:
                conn.send(b"NOPE:null;")
        
# main program
srvsocket = socket.socket()
srvsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srvsocket.bind((HOST, PORT))
srvsocket.listen(5)

while True:
    conn, fromaddr = srvsocket.accept()
    # ssl
    # sslconn = context.wrap_socket(conn, server_side=True)
    # echo(sslconn)
    # sslconn.close()
    star(conn)
    conn.close()
    
srvsocket.close()
