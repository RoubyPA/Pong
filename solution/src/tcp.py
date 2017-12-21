#!/usr/bin/env python3
import socket, sys, os
from _thread import *

host = ''
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((host, port))
except socket.error as e:
    print(str(e))

s.listen(5)
print('Waiting for a connection')
def threaded_client(conn):
    conn.send(str.encode('Welcome, type your info\n'))

    while True:
        data = conn.recv(2048)
        reply = 'Server ouptut: '+data.decode('utf-8')
        if not data:
            break
        conn.sendall(str.encode(reply))
    conn.close()

while True:
    conn, addr = s.accept()
    print('connected to: '+addr[0]+':'+str(addr[1]))

    start_new_thread(threaded_client,(conn,))


    
# maChaussette = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
# #serv = 1
# #host = 2

# while (serv != '1') and (serv != '2'):

# #Serveur :
# if serv == '1':
# 	try:
# 		maChaussette.bind(('', port))
# 	except socket.error:
# 		print("La liaison de la socket à l'adresse choisie à échouée")
# 		sys.exit()
# 	print("Serveur prêt, en attende d'un autre joueur")

# 	maChaussette.listen(2)
# 	connexion, adresse = maChaussette.accept()
# 	while True:
# 		os.system('cls' if os.name == 'nt' else 'clear')


                
# else:
# 	#Client
# 	try:
# 		maChaussette.connect((serveur, port))
# 	except socket.error:
# 		print("La connexion a échouée")
# 		sys.exit()
# 	print("Connexion réussie avec le serveur")
# 	maChaussette.send(nom.encode("Utf8"))
# 	joueurServeur = maChaussette.recv(1024).decode("Utf8")
# 	while True:
# 		os.system('cls' if os.name == 'nt' else 'clear')
# 		print("Joueurs : \n", nom, "\n", joueurServeur)
# 		choix = input("Pierre (1), Feuille (2) ou Ciseau (3) ")
# 		maChaussette.send(choix.encode("Utf8"))
# 		print("En attente du choix de l'autre joueur")
# 		resultat = maChaussette.recv(1024).decode("Utf8")
# 		print(resultat)
# 		input("Appuyez sur une touche pour continuer")

# connexion.send(resultatClient.encode("Utf8"))
# maChaussette.recv(1024).decode("Utf8")
