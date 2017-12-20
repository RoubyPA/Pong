#!/usr/bin/python3
import socket
# import ssl

HOST= "127.0.0.1"
PORT= 7777
BUFSIZE= 1024

version = 0.1
ball_speed_x = 4
ball_speed_y = 4
r_speed = 2

# ssl context
# context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
# context.load_verify_locations("../authorite/ca.crt")

# sock
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((HOST, PORT))
# ssl
# sslconn = context.wrap_socket(conn, server_hostname=HOST)
# request = b"Hello World!"
# sslconn.sendall(request)
# answer = sslconn.recv(BUFSIZE)
# print(answer.decode())
# sslconn.close()

# Application Connection
request = "CONN:" + str(version) + "," + str(ball_speed_x) + "," + str(ball_speed_y) + "," + str(r_speed) + ";"

conn.send(request.encode())
answer = conn.recv(BUFSIZE)
print(answer.decode())

# connection OKAY
request = b"OKAY:null;"
conn.send(request)
print(answer.decode())

# ping
request = b"PING:null;"
conn.send(request)
answer = conn.recv(BUFSIZE)
print(answer.decode())

conn.close()
