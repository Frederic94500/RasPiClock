# -*- encoding: utf-8 -*-
#RasPiClock - Frédéric94500

import time, json, sys, os, requests, socket, configparser, hashlib, threading

import PrintScreen as PS
import Services as SV

Units = "°K"
STOP = False
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
				global BearerAUTH
				BearerRAW = os.popen("curl -u '"+ conf["TWITTER"]["TwitterAPI"] + ":" + conf["TWITTER"]["TwitterAPISecret"] + "' --data 'grant_type=client_credentials' 'https://api.twitter.com/oauth2/token'").read()
				BearerJSON = json.loads(BearerRAW)
				BearerAUTH = BearerJSON["access_token"]
			while True:
				global STOP
				#global SLEEP
				"""if (time.strftime("%H", time.localtime()) >= conf["SLEEP"]["HStart"] or time.strftime("%H", time.localtime()) < conf["SLEEP"]["HEnd"]) and conf["SLEEP"]["HStart"] != "" and conf["SLEEP"]["HEnd"] != "":
					i = 0
					while time.strftime("%H", time.localtime()) >= conf["SLEEP"]["HStart"] or time.strftime("%H", time.localtime()) < conf["SLEEP"]["HEnd"]:
						if i == 60 or i == 0:
							TextPAPIRUS.Clear()
							TextPAPIRUS.AddText("Je dors", 10, 10, size = 20, fontPath="Ubuntu.ttf")
							TextPAPIRUS.AddText("Retour à " + conf["SLEEP"]["HEnd"] + "H", 10, 40, size = 20, fontPath="Ubuntu.ttf")
							TextPAPIRUS.AddText(time.strftime("%H:%M", time.localtime()), 200, 10, Id="Time", size = 20, fontPath="Ubuntu.ttf")
							TextPAPIRUS.WriteAll(True)
							i = 0
						time.sleep(120)
						TextPAPIRUS.UpdateText("Time", time.strftime("%H:%M", time.localtime()), fontPath="Ubuntu.ttf")
						TextPAPIRUS.WriteAll(True)
						i += 1
					TextPAPIRUS.Clear()
					break;"""
				if conf["CRYPTO"]["CryptoAPI"] != "":
					PS.Crypto(conf, TextPAPIRUS)
				if conf["WEATHER"]["MeteoAPI"] != "":
					PS.Meteo(conf, TextPAPIRUS, Units)
				if conf["LASTFM"]["LastFmAPI"] != "":
					PS.Musique(conf, TextPAPIRUS)
				if conf["TWITCH"]["TwitchAPI"] != "":
					PS.Twitch(conf, TextPAPIRUS)
				if conf["TWITTER"]["TwitterAPI"] != "" and conf["TWITTER"]["twitterapisecret"] != "":
					PS.Twitter(conf, TextPAPIRUS, BearerAUTH)
				if conf["RATP"]["typetransA"] != "" and conf["RATP"]["lineA"] != "" and conf["RATP"]["stationA"] != "":
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

		Adaptation()

	def HashVerify():
		ConfFile = open('config.cfg', "rb")
		bytes = ConfFile.read()
		HashNew = hashlib.sha256(bytes).hexdigest()
		ConfFile.close()
	
		HashFile = open('hash.txt', "r")
		HashOld = HashFile.read()
		HashFile.close()

		if HashOld != HashNew:
			APICheck()
		if HashOld == HashNew:
			Adaptation()

	def APICheck(): #Fonction de test de chaque paramètre (sauf Twitch)
		Check = 0

		#Test des APIs
		try:
			if conf["WEATHER"]["MeteoAPI"] != "":
				SV.SVMeteo(conf)
				if 400 <= int(SV.DataMeteo["cod"]) <= 599: 
						ERROR = "Erreur dans la config Météo, veuillez vérifier votre saisie!"
						ErrorConfig(ERROR)
						return
				else:
					Check += 1
			else:
				Check += 1

			if conf["CRYPTO"]["CryptoAPI"] != "":
				SV.SVCrypto(conf)
				try:
					if SV.DataCrypto["Response"] == "Error":
						ERROR = "Erreur dans la config Crypto, veuillez vérifier votre saisie!"
						ErrorConfig(ERROR)
						return
				except KeyError:
					Check += 1
			else:
				Check += 1

			if conf["LASTFM"]["LastFmAPI"] != "":
				SV.SVMusique(conf)
				try:
					if 2 <= int(SV.DataLast["error"]) <= 29:
						ERROR = "Erreur dans la config LastFM, veuillez vérifier votre saisie!"
						ErrorConfig(ERROR)
						return
				except KeyError:
					Check += 1
			else:
				Check += 1

			if conf["TWITTER"]["TwitterAPI"] != "" and conf["TWITTER"]["twitterapisecret"] != "":
				try:
					BearerRAW = os.popen("curl -u '"+ conf["TWITTER"]["TwitterAPI"] + ":" + conf["TWITTER"]["TwitterAPISecret"] + "' --data 'grant_type=client_credentials' 'https://api.twitter.com/oauth2/token'").read()
					BearerJSON = json.loads(BearerRAW)
					BearerAUTH = BearerJSON["access_token"]
				except KeyError:
					ERROR = "Erreur dans la config Twitter, il faut 2 clés API! Veuillez vérifier votre saisie!"
					ErrorConfig(ERROR)
					return
				finally:
					try:
						SV.SVTwitter(conf, BearerAUTH)
						if 49 <= int(SV.DataTwitter["errors"][0]["code"]) <= 599:
							ERROR = "Erreur dans la config Twitter, veuillez vérifier votre saisie!"
							ErrorConfig(ERROR)
							return
					except KeyError:
						Check += 1
			else:
				Check += 1

			if conf["RATP"]["typetransA"] != "" and conf["RATP"]["lineA"] != "" and conf["RATP"]["stationA"] != "":
				try:
					SV.SVRATP(conf)
					if SV.OutputA["result"]["code"] == 404:
						ERROR = "Erreur dans la config RATP A, veuillez vérifier votre saisie!"
						ErrorConfig(ERROR)
						return
				except:
					if conf["RATP"]["typetransB"] != "" and conf["RATP"]["lineB"] != "" and conf["RATP"]["stationB"] != "":
						try:
							if SV.OutputB["result"]["code"] == 404:
								ERROR = "Erreur dans la config RATP B, veuillez vérifier votre saisie!"
								ErrorConfig(ERROR)
								return
						except:
							Check += 1
					else:
						Check += 1
			else:
				Check += 1

		except (ValueError, socket.error, socket.gaierror, socket.herror, socket.timeout): #Situation d'erreur de connexion
			TextPAPIRUS.Clear()
			TextPAPIRUS.AddText("Erreur de connexion, nouvelle tentative de connexion dans: T", 10, 48, size = 20, fontPath="Ubuntu.ttf", Id="TimerErr")
			for I in range(15):
				TextPAPIRUS.UpdateText("TimerErr", "Erreur de connexion, \nnouvelle tentative de connexion dans: " + str(15 - I), fontPath="Ubuntu.ttf")
				TextPAPIRUS.WriteAll(True)
				time.sleep(1)
			TextPAPIRUS.Clear()
			APICheck()

		finally: #Fin de la vérification des API
			if Check == 5:
				HashSave()

	def ErrorConfig(ERROR):
			print(ERROR)
			sys.exit()

	def Adaptation():
		global Units

		if conf["WEATHER"]["Units"] == "imperial":
			Units = "°F"
		if conf["WEATHER"]["Units"] == "metric":
			Units = "°C"
		else:
			Units = "°K"

		Main()

	
	HashVerify()

else: #Si papirus n'est pas installé
	print("Erreur, veuillez écrire -b ou -bash ou rien et installer Papirus (https://github.com/PiSupply/PaPiRus) pour éxécuter le programme!")
