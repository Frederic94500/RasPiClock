# -*- encoding: utf-8 -*-
#RasPiClock - Frédéric94500

import time, sys, os, socket, configparser

import PrintScreen as PS
import APITester

def core(conf, textPAPIRUS): #Fonction Coeur
	try:
		while True:
			PS.crypto(conf, textPAPIRUS)
			time.sleep(5)
			for i in range(720):
				PS.crypto_update(conf, textPAPIRUS)
				time.sleep(5)
			textPAPIRUS.Clear()
	except (ValueError, socket.error, socket.gaierror, socket.herror, socket.timeout): #Situation d'erreur de connexion
		textPAPIRUS.Clear()
		textPAPIRUS.AddText("Erreur de connexion, \nnouvelle tentative de connexion dans: T", 10, 48, size = 20, fontPath="Ubuntu.ttf", Id="TimerErr")
		for I in range(15):
			textPAPIRUS.UpdateText("TimerErr", "Erreur de connexion, \nnouvelle tentative de connexion dans: " + str(15 - I), fontPath="Ubuntu.ttf")
			textPAPIRUS.WriteAll(True)
			time.sleep(1)
		textPAPIRUS.Clear()
		core()
	except KeyboardInterrupt:
		print("Vous avez arrêté le processus, nettoyage de l'écran")
		os.system("papirus-clear")
		sys.exit()

def main():
	if os.path.exists('/etc/default/epd-fuse'):
		from papirus import PapirusTextPos
		textPAPIRUS = PapirusTextPos(False)
		textPAPIRUS.Clear()

		conf = configparser.ConfigParser()
		conf.read("config.cfg")

		if APITester.api_tester(conf, textPAPIRUS):
			core(conf, textPAPIRUS)
		
	else: #Si papirus n'est pas installé
		print("Erreur, il faut installer Papirus (https://github.com/PiSupply/PaPiRus) pour éxécuter ce programme!")
		sys.exit()

main()