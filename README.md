# Botnet
Développement
Botnet Python
Janvier 2020
 
 
Rapport et documents annexes
Travail par Romain Dache et Hugo Hainaut



Architecture générale
Comme prévu dans les instructions de ce travail, l’ensemble du botnet est divisé en deux parties : le programme destiné aux machine esclaves, et le pregramme destiné à la machine Maitre.
L’interface avec l’utilisateur se fait uniquement sur la machine Maitre, et les renseignements et instructions sont passées aux esclaves (cf titre suivant).
Les tâches demandées sont effectuées sur ces machines, puis une confirmation, ou des informations, sont renvoyées à la machine maitre.
La communication entre les machines
La communication entre les machines et le serveur se fait via une connexion TCP (précisé dans les arguments des sockets). Lors de la connexion, l’host est prédéfini dans le main ainsi que le port utilisé pour celle-ci.
Les fonctions dans la machine master
Il y a différentes fonctions utilisées dans le fichier master, chacune a sa propre utilité et dispose de ses arguments propres
Le main :
Il s’occupe de faire tourner les fonctions qui sont appelées les unes à la suites des autres, on prédéfini un host et un port (qui auraient très bien pu être déclaré comme des valeurs par défaut), on utilise les sockets pour lier le client au serveur qu’on lie ensuite via la commande bind.
Enfin, on ouvre le port d’écoute et on appel la fonction “connexion” qui a pour but de boucler sur le port d’écoute afin d’assurer une connexion entre le client et le serveur.


Les choix de fonction :
Un choix d’actions est proposé à l’utilisateur sous la forme d’un simple digit à renseigner,et une boucle de sécurité empêche tout choix invalide.
Une fois la validité du choix confirmée, le résultat est testé par une suite de elif, chacun envoyant un ordre spécifique aux machines esclaves, après une demande de renseignement supplémentaires le cas échéant (les fonctions get_log et ddos).

Les fonctions dans les machines slave
Le main
Constitué en majorité d’une boucle permettant la réception et l’envoi de données entre les machines, il comprend également la sélection en elif permettant de lancer les fonctions utiles.
Certaines de ces conditions sont plus complexes que d’autres, nommément les conditions gérant le lancement des fonctions get_log et ddos.
En effet, celles-ci nécessitent des paramètres extérieurs à la machine esclave, qui doivent donc être extraits du flux de données pour être utilisables.
A cette fin, les données sont récupérées via une variable de type string, puis séparées grâce à la fonction .split.
Dans les cas de la fonction ddos, une autre complexité s’ajoute, puisque un format datetime doit être reconstitué à partir du string récupéré.
Une fois cette variable utilisable, on utilise la fonction enterabs du module schedule pour enregistrer l’événement à lancer à la date adaptée.


Start log
Les variables globales fichierLog et temoinLog sont utilisées ici, respectivement pour garder facilement traçable le nom du fichier de log, et pour garder trace de l’accomplissement de cette fonction à l’adresse de la fonction stop_log.
Des informations sur le système sont ensuite enregistrées dans le fichier log pour une utilisation ultérieures.

Stop log
Rien de compliqué ici, la fonction teste l’accomplissement de la première tâche et renvoie le résultat.
Get log
Cette fonction fait appel à une fonction secondaire qui a pour but de compter les lignes du fichier de logs.
Le nombre en question est ensuite utilisé dans une autre boucle de lecture du fichier, qui va copier les lignes demandées dans une liste de string.
Cette liste est ensuite renvoyée à la fonction main.
Ddos
Cette fonction utilise des éléments du module scapy pour envoyer, au moment opportun, une boucle rapide de requêtes http à l’adresse IP de la cible, renseignée par la machine Master.



Nos sources :
●	https://2.python-requests.org/en/master/user/quickstart/#make-a-request
●	https://stackoverflow.com/questions/89228/calling-an-external-command-from-python
●	https://tutorial.eyehunts.com/python/python-read-file-line-by-line-readlines/
●	https://stackoverflow.com/questions/16043797/python-passing-variables-between-functions
●	https://docs.python.org/2/library/logging.html
●	https://github.com/invernizzi/scapy-http
●	https://stackoverflow.com/questions/30481003/send-http-request-at-user-set-time-python-back-end
●	https://github.com/dbader/schedule
●	https://stackoverflow.com/questions/11523918/python-start-a-function-at-given-time
●	https://stackabuse.com/
●	https://www.tutorialspoint.com/python_penetration_testing/python_penetration_testing_dos_and_ddos_attack.htm
●	https://www.youtube.com/watch?v=WM1z8soch0Q (Sockets Tutorial with Python 3)
●	https://realpython.com/python-logging/#the-logging-module





