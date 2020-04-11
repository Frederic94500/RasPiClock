# -*- encoding: utf-8 -*-

import json, configparser, requests, socket, sys, os
import Services as SV

conf = configparser.ConfigParser()
conf.read("config.cfg")

def main():
	try:
		if conf["CRYPTO"]["CryptoAPI"] != "":
			test_Crypto(conf)
		if conf["WEATHER"]["MeteoAPI"] != "":
			test_Meteo(conf, Units)
		if conf["LASTFM"]["LastFmAPI"] != "":
			test_Musique(conf)
		if conf["TWITCH"]["TwitchAPI"] != "":
			test_Twitch(conf)
		if conf["TWITTER"]["TwitterAPI"] != "" and conf["TWITTER"]["twitterapisecret"] != "":
			global BearerAUTH
			BearerRAW = os.popen("curl -u '"+ conf["TWITTER"]["TwitterAPI"] + ":" + conf["TWITTER"]["TwitterAPISecret"] + "' --data 'grant_type=client_credentials' 'https://api.twitter.com/oauth2/token'").read()
			BearerJSON = json.loads(BearerRAW)
			BearerAUTH = BearerJSON["access_token"]
			test_Twitter(conf, BearerAUTH)
		if conf["RATP"]["typetransA"] != "" and conf["RATP"]["lineA"] != "" and conf["RATP"]["stationA"] != "":
			test_RATP(conf)
	except (ValueError, socket.error, socket.gaierror, socket.herror, socket.timeout): #Situation d'erreur de connexion
		for I in range(15):
			clear()
			print("Erreur de connexion, nouvelle tentative de connexion dans: " + str(15 - I))
			time.sleep(1)
		main()


def espacement():
	print("")
	print("==============================")
	print("")

def test_Crypto(conf):
	SV.SVCrypto(conf)

	PCTC1 = list(str(SV.DataCrypto["RAW"][conf["CRYPTO"]["Coin1"]][conf["CRYPTO"]["Currency"]]["CHANGEPCT24HOUR"]))
	del PCTC1[-14:-1]
	PCTC2 = list(str(SV.DataCrypto["RAW"][conf["CRYPTO"]["Coin2"]][conf["CRYPTO"]["Currency"]]["CHANGEPCT24HOUR"]))
	del PCTC2[-14:-1]
	
	print("Crypto:")
	print(conf["CRYPTO"]["Coin1"] + ": " + conf["CRYPTO"]["Currency"] + " " + str(SV.DataCrypto["RAW"][conf["CRYPTO"]["Coin1"]][conf["CRYPTO"]["Currency"]]["PRICE"]) + " - " + "".join(PCTC1))
	print(conf["CRYPTO"]["Coin2"] + ": " + conf["CRYPTO"]["Currency"] + " " + str(SV.DataCrypto["RAW"][conf["CRYPTO"]["Coin2"]][conf["CRYPTO"]["Currency"]]["PRICE"]) + " - " + "".join(PCTC2))

	espacement()

def test_Meteo(conf, Units):
	SV.SVMeteo(conf)

	print("Météo:")
	print("Température: " + str(SV.DataMeteo["main"]["temp"]) + "°C")
	print("Temp. Min: " + str(SV.DataMeteo["main"]["temp_min"]) + "°C" + " Temp. Max: " + str(SV.DataMeteo["main"]["temp_max"]) + Units)
	print("Temps: " + SV.DataMeteo["weather"][0]["description"].capitalize()) 

	espacement()

def test_Musique(conf):
	SV.SVMusique(conf)

	print("Last.fm:")

	try:
		if SV.DataLast["recenttracks"]["track"][0]["@attr"]["nowplaying"] == "true":
			print("Actuellement: " + SV.DataLast["recenttracks"]["track"][0]["artist"]["#text"] + " - " + SV.DataLast["recenttracks"]["track"][0]["name"])
			print("Album: " + SV.DataLast["recenttracks"]["track"][0]["album"]["#text"])
			print("")
			print("Précédent: " + SV.DataLast["recenttracks"]["track"][1]["artist"]["#text"] + " - " + SV.DataLast["recenttracks"]["track"][1]["name"])
	except:
		print("Précédent: " + SV.DataLast["recenttracks"]["track"][0]["artist"]["#text"] + " - " + SV.DataLast["recenttracks"]["track"][0]["name"])
		print("Album: " + SV.DataLast["recenttracks"]["track"][0]["album"]["#text"])
	finally:
		espacement()

def test_Twitch(conf):
	print("Twitch:")

	for i in range(2):
		try:
			DataSt = SV.SVTwitch(conf, "TwitchSt" + str(i + 1))
			if DataSt["data"][0]["type"] == "live":
				GameName = SV.SVTwitchGame(conf, DataSt)
				print(conf["TWITCH"]["TwitchSt" + str(i + 1)].capitalize() + ": ON")
				print("Jeu: " + GameName["data"][0]["name"])
				print("Titre: " + DataSt["data"][0]["title"])
		except IndexError:
			print(conf["TWITCH"]["TwitchSt" + str(i + 1)].capitalize() + ": OFF")
		finally:
			espacement()

def test_Twitter(conf, BearerAUTH):
	SV.SVTwitter(conf, BearerAUTH)

	print("Twitter:")
	print("Compte: " + SV.DataTwitter["name"])
	print(str(SV.DataTwitter["followers_count"]) + " abonnés")
	print("")
	print("Dernier tweet:")
	print(SV.DataTwitter["status"]["text"])

	espacement()

def test_RATP(conf):
	SV.SVRATP(conf)

	print("RATP:")

	print("Station: " + conf["RATP"]["stationA"] + " - " + conf["RATP"]["lineA"])
	print("Prochain: " + SV.OutputA["result"]["schedules"][0]["message"])
	print("Direction: " + SV.OutputA["result"]["schedules"][0]["destination"])
	print("")

	if conf["RATP"]["typetransB"] != "" and conf["RATP"]["lineB"] != "" and conf["RATP"]["stationB"] != "":
		print("Station: " + conf["RATP"]["stationB"] + " - " + conf["RATP"]["lineB"])
		print("Prochain: " + SV.OutputB["result"]["schedules"][0]["message"])
		print("Direction: " + SV.OutputB["result"]["schedules"][0]["destination"])

	espacement()

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
		for I in range(15):
			clear()
			print("Erreur de connexion, nouvelle tentative de connexion dans: " + str(15 - I))
			time.sleep(1)
		APICheck()

	finally: #Fin de la vérification des API
		if Check == 5:
			Adaptation()

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

	main()

APICheck()