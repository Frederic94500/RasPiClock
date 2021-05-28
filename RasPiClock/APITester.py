# -*- encoding: utf-8 -*-

import socket, time, configparser
import Request as RQ

conf = configparser.ConfigParser()
conf.read("config.cfg")

def apiCheck(conf, textPAPIRUS):
	try:
		if crypto(conf): return True #Fin de la vérification des API
		else: return False
	except (ValueError, socket.error, socket.gaierror, socket.herror, socket.timeout): #Situation d'erreur de connexion
		textPAPIRUS.Clear()
		textPAPIRUS.AddText("Erreur de connexion, nouvelle tentative de connexion dans: T", 10, 48, size = 20, fontPath="Ubuntu.ttf", Id="TimerErr")
		for I in range(15):
			textPAPIRUS.UpdateText("TimerErr", "Erreur de connexion, \nnouvelle tentative de connexion dans: " + str(15 - I), fontPath="Ubuntu.ttf")
			textPAPIRUS.WriteAll(True)
			time.sleep(1)
		textPAPIRUS.Clear()
		apiCheck()

def crypto(conf):
	for i in range(2):
		reponseCrypto = RQ.crypto(conf, "pair" + str(i+1))
		if reponseCrypto.status_code != 200:
			print("Erreur dans la config Crypto, veuillez vérifier votre saisie!")
			return False
		else:
			return True
