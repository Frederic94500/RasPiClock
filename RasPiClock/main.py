# -*- encoding: utf-8 -*-
# RasPiClock - Frédéric94500

import configparser
import os
import socket
import sys
import time

from Crypto import Crypto


def core(conf, papirus):  # Fonction Coeur
    try:
        obj = [Crypto("", "", [conf["CRYPTO"]["pair0"], conf["CRYPTO"]["pair1"]])]
        if not testing(obj):
            raise ValueError()
        while True:
            for i in obj:
                i.print(papirus)
                time.sleep(5)
                for j in range(720):
                    i.print_update(papirus)
                    time.sleep(5)
                papirus.Clear()
    except (socket.error, socket.gaierror, socket.herror, socket.timeout):  # Situation d'erreur de connexion
        papirus.Clear()
        papirus.AddText("Erreur de connexion, \nnouvelle tentative de connexion dans: T", 10, 48, size=20,
                        fontPath="Ubuntu.ttf", Id="TimerErr")
        for i in range(15):
            papirus.UpdateText("TimerErr",
                               "Erreur de connexion, \nnouvelle tentative de connexion dans: " + str(15 - i),
                               fontPath="Ubuntu.ttf")
            papirus.WriteAll(True)
            time.sleep(1)
        papirus.Clear()
        core(conf, papirus)
    except ValueError:
        sys.exit(1)
    except KeyboardInterrupt:
        print("Vous avez arrêté le processus, nettoyage de l'écran")
        os.system("papirus-clear")
        sys.exit()


def testing(obj):
    for i in obj:
        if not i.test():
            return False
    return True


if __name__ == '__main__':
    if os.path.exists('/etc/default/epd-fuse'):
        from papirus import PapirusTextPos

        papirus = PapirusTextPos(False)
        papirus.Clear()

        conf = configparser.ConfigParser()
        conf.read("config.cfg")

        core(conf, papirus)

    else:  # Si papirus n'est pas installé
        print("Erreur, il faut installer Papirus (https://github.com/PiSupply/PaPiRus) pour exécuter ce programme!")
        sys.exit()
