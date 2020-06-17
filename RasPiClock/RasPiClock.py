# -*- encoding: utf-8 -*-
#RasPiClock - Frédéric94500

import time, json, sys, os, requests, socket, configparser, hashlib

import PrintScreen as PS
import Services as SV
import APITester as APIT

Units = "°K"
SLEEP = False
BearerAUTH = ""

conf = configparser.ConfigParser()
conf.read("config.cfg")

if os.path.exists('/etc/default/epd-fuse'):
	from papirus import PapirusTextPos
	TextPAPIRUS = PapirusTextPos(False)
	TextPAPIRUS.Clear()

	def Main(): #Fonction Coeur
		try:
			if conf["TWITTER"]["TwitterAPI"] != "" and conf["TWITTER"]["twitterapisecret"] != "":
				BearerRAW = SV.SVTwitterGetToken(conf)
				if BearerRAW.status_code == 200: 
					BearerAUTH = BearerRAW.json()['access_token']
			while True:
				if conf["CRYPTO"]["CryptoAPI"] != "":
					PS.Crypto(conf, TextPAPIRUS)
				if conf["WEATHER"]["MeteoAPI"] != "":
					PS.Meteo(conf, TextPAPIRUS, Units)
				if conf["LASTFM"]["LastFmAPI"] != "":
					PS.Musique(conf, TextPAPIRUS)
				if conf["TWITCH"]["twitchapiclientid"] != "":
					PS.Twitch(conf, TextPAPIRUS)
				if conf["TWITTER"]["TwitterAPI"] != "" and conf["TWITTER"]["twitterapisecret"] != "":
					PS.Twitter(conf, TextPAPIRUS, BearerAUTH)
				if conf["RATP"]["typetrans1"] != "" and conf["RATP"]["line1"] != "" and conf["RATP"]["station1"] != "" and conf["RATP"]["sens1"]:
					PS.RATP(conf, TextPAPIRUS)
		except (ValueError, socket.error, socket.gaierror, socket.herror, socket.timeout): #Situation d'erreur de connexion
			TextPAPIRUS.Clear()
			TextPAPIRUS.AddText("ERREUR de connexion, nouvelle tentative de connexion dans: T", 10, 48, size = 20, fontPath="Ubuntu.ttf", Id="TimerErr")
			for I in range(15):
				TextPAPIRUS.UpdateText("TimerErr", "Erreur de connexion, \nnouvelle tentative de connexion dans: " + str(15 - I), fontPath="Ubuntu.ttf")
				TextPAPIRUS.WriteAll(True)
				time.sleep(1)
			TextPAPIRUS.Clear()
			Main()
		except KeyboardInterrupt:
			print("Vous avez arrêté le processus, nettoyage de l'écran")
			os.system("papirus-clear")
			sys.exit()

	def HashSave():
		ConfFile = open("config.cfg","rb")
		bytes = ConfFile.read()
		hashconf = hashlib.sha256(bytes).hexdigest()
		ConfFile.close()

		HashFile = open("hash.txt", "w")
		HashFile.write(hashconf)
		HashFile.close()

	def HashVerify():
		ConfFile = open('config.cfg', "rb")
		bytes = ConfFile.read()
		HashNew = hashlib.sha256(bytes).hexdigest()
		ConfFile.close()
	
		HashFile = open('hash.txt', "r")
		HashOld = HashFile.read()
		HashFile.close()

		if HashOld == HashNew:
			return True
		if HashOld != HashNew:
			return False

	def Adaptation():
		global Units

		if conf["WEATHER"]["Units"] == "imperial":
			Units = "°F"
		if conf["WEATHER"]["Units"] == "metric":
			Units = "°C"
		else:
			Units = "°K"

		Main()
	
	if HashVerify():
		Adaptation()
	else:
		if APIT.APICheck(conf, TextPAPIRUS):
			HashSave()
			Adaptation()

else: #Si papirus n'est pas installé
	print("Erreur, veuillez écrire -b ou -bash ou rien et installer Papirus (https://github.com/PiSupply/PaPiRus) pour éxécuter le programme!")
