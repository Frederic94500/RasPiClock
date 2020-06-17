# -*- encoding: utf-8 -*-

import json, configparser, requests, socket, sys, time, base64
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
		if conf["TWITCH"]["twitchapiclientid"] != "":
			test_Twitch(conf)
		if conf["TWITTER"]["TwitterAPI"] != "" and conf["TWITTER"]["twitterapisecret"] != "":
			BearerRAW = SV.SVTwitterGetToken(conf)
			if BearerRAW.status_code == 200: 
				BearerAUTH = BearerRAW.json()['access_token']
				test_Twitter(conf, BearerAUTH)
		if conf["RATP"]["typetrans1"] != "" and conf["RATP"]["line1"] != "" and conf["RATP"]["station1"] != "" and conf["RATP"]["sens1"]:
			test_RATP(conf)
	except (ValueError, socket.error, socket.gaierror, socket.herror, socket.timeout): #Situation d'erreur de connexion
		for I in range(15):
			print("Erreur de connexion, nouvelle tentative de connexion dans: " + str(15 - I))
			time.sleep(1)
		main()


def espacement():
	print("")
	print("==============================")
	print("")

def test_Crypto(conf):
	print("Crypto:")
	for i in range(2):
		ReponseCrypto = SV.SVCrypto(conf, "coin" + str(i + 1))
		PCT = list(str(ReponseCrypto.json()["RAW"][conf["CRYPTO"]["coin" + str(i + 1)]][conf["CRYPTO"]["Currency"]]["CHANGEPCT24HOUR"]))
		del PCT[-14:-1]
	
		print(conf["CRYPTO"]["coin" + str(i + 1)] + ": " + conf["CRYPTO"]["Currency"] + " " + str(ReponseCrypto.json()["RAW"][conf["CRYPTO"]["coin" + str(i + 1)]][conf["CRYPTO"]["Currency"]]["PRICE"]) + " - " + "".join(PCT))

	espacement()

def test_Meteo(conf, Units):
	ReponseMeteo = SV.SVMeteo(conf)

	print("Météo:")
	print("Température: " + str(ReponseMeteo.json()["main"]["temp"]) + "°C")
	print("Temp. Min: " + str(ReponseMeteo.json()["main"]["temp_min"]) + "°C" + " Temp. Max: " + str(ReponseMeteo.json()["main"]["temp_max"]) + Units)
	print("Temps: " + ReponseMeteo.json()["weather"][0]["description"].capitalize()) 

	espacement()

def test_Musique(conf):
	ReponseLastFM = SV.SVMusique(conf)

	print("Last.fm:")

	try:
		if ReponseLastFM.json()["recenttracks"]["track"][0]["@attr"]["nowplaying"] == "true":
			print("Actuellement: " + ReponseLastFM.json()["recenttracks"]["track"][0]["artist"]["#text"] + " - " + ReponseLastFM.json()["recenttracks"]["track"][0]["name"])
			print("Album: " + ReponseLastFM.json()["recenttracks"]["track"][0]["album"]["#text"])
			print("")
			print("Précédent: " + ReponseLastFM.json()["recenttracks"]["track"][1]["artist"]["#text"] + " - " + ReponseLastFM.json()["recenttracks"]["track"][1]["name"])
	except:
		print("Précédent: " + ReponseLastFM.json()["recenttracks"]["track"][0]["artist"]["#text"] + " - " + ReponseLastFM.json()["recenttracks"]["track"][0]["name"])
		print("Album: " + ReponseLastFM.json()["recenttracks"]["track"][0]["album"]["#text"])
	finally:
		espacement()

def test_Twitch(conf):
	print("Twitch:")

	for i in range(2):
		ReponseID = SV.SVTwitchGetID(conf, "TwitchSt" + str(i + 1))
		ReponseTwitchSt = SV.SVTwitchGetStatus(conf, ReponseID)
		try:
			if ReponseTwitchSt.json()["stream"]["broadcast_platform"] == "live":
				print(ReponseTwitchSt.json()["stream"]["channel"]["display_name"] + ": ON")
				print("Jeu: " + ReponseTwitchSt.json()["stream"]["game"])
				print("Titre: " + ReponseTwitchSt.json()["stream"]["channel"]["status"])
		except: print(conf["TWITCH"]["TwitchSt" + str(i + 1)].capitalize() + ": OFF")
		finally: espacement()

def test_Twitter(conf, BearerAUTH):
	ReponseTwitter = SV.SVTwitter(conf, BearerAUTH)

	print("Twitter:")
	print("Compte: " + ReponseTwitter.json()["name"])
	print(str(ReponseTwitter.json()["followers_count"]) + " abonnés")
	print("")
	print("Dernier tweet:")
	print(ReponseTwitter.json()["status"]["text"])

	espacement()

def test_RATP(conf):
	print("RATP:")

	if conf["RATP"]["typetrans1"] != "" and conf["RATP"]["line1"] != "" and conf["RATP"]["station1"] != "" and conf["RATP"]["sens1"] != "":
		i = 1
		ReponseRATP = SV.SVRATP(conf, "typetrans" + str(i), "line" + str(i), "station" + str(i), "sens" + str(i))
		print("Station: " + conf["RATP"]["station" + str(i)] + " - " + conf["RATP"]["line" + str(i)])
		print("Prochain: " + ReponseRATP.json()["result"]["schedules"][0]["message"])
		print("Direction: " + ReponseRATP.json()["result"]["schedules"][0]["destination"])
		print("")

	if conf["RATP"]["typetrans2"] != "" and conf["RATP"]["line2"] != "" and conf["RATP"]["station2"] != "" and conf["RATP"]["sens2"] != "":
		i += 1
		ReponseRATP = SV.SVRATP(conf, "typetrans" + str(i), "line" + str(i), "station" + str(i), "sens" + str(i))
		print("Station: " + conf["RATP"]["station" + str(i)] + " - " + conf["RATP"]["line" + str(i)])
		print("Prochain: " + ReponseRATP.json()["result"]["schedules"][0]["message"])
		print("Direction: " + ReponseRATP.json()["result"]["schedules"][0]["destination"])

	espacement()

def APICheck(): #Fonction de test de chaque paramètre
	#Test des APIs
	try:
		if TestMeteo() and TestCrypto() and TestMusique() and TestTwitter() and TestRATP() and TestTwitch(): return True #Fin de la vérification des API
		else: return False

	except (ValueError, socket.error, socket.gaierror, socket.herror, socket.timeout): #Situation d'erreur de connexion
		for I in range(15):
			print("Erreur de connexion, nouvelle tentative de connexion dans: " + str(15 - I))
			time.sleep(1)
		APICheck()

def TestMeteo():
	if conf["WEATHER"]["MeteoAPI"] != "":
		ReponseMeteo = SV.SVMeteo(conf)
		if ReponseMeteo.status_code == 200: return True
		else:
			print("Erreur dans la config Météo, veuillez vérifier votre saisie!")
			return False
	else: return True

def TestCrypto():
	if conf["CRYPTO"]["CryptoAPI"] != "":
		i = 1
		ReponseCrypto = SV.SVCrypto(conf, "coin" + str(i))
		try:
			if ReponseCrypto.json()["Response"] == "Error":
				print("Erreur dans la config Crypto, veuillez vérifier votre saisie!")
				return False
		except: return True
	else: return True

def TestMusique():
	if conf["LASTFM"]["LastFmAPI"] != "":
		ReponseLastFM = SV.SVMusique(conf)
		if ReponseLastFM.status_code == 200: return True
		else: 
			print("Erreur dans la config LastFM, veuillez vérifier votre saisie!")
			return False
	else: return True

def TestTwitter():
	if conf["TWITTER"]["TwitterAPI"] != "" and conf["TWITTER"]["twitterapisecret"] != "":
		BearerRAW = SV.SVTwitterGetToken(conf)
		if BearerRAW.status_code == 200: 
			BearerAUTH = BearerRAW.json()['access_token']
			ReponseTwitter = SV.SVTwitter(conf, BearerAUTH)
			if ReponseTwitter.status_code == 200:
				return True
			else:
				print("Erreur dans la config Twitter, veuillez vérifier votre saisie!")
				return False
		else:
			print("Erreur lors de la création du token Twitter, veuillez vérifier votre saisie!")
			return False
	else: return True

def TestRATP():
	if conf["RATP"]["typetrans1"] != "" and conf["RATP"]["line1"] != "" and conf["RATP"]["station1"] != "" and conf["RATP"]["sens1"] != "":
		i = 1
		ReponseRATP = SV.SVRATP(conf, "typetrans" + str(i), "line" + str(i), "station" + str(i), "sens" + str(i))
		if ReponseRATP.status_code == 200:
			if conf["RATP"]["typetrans2"] != "" and conf["RATP"]["line2"] != "" and conf["RATP"]["station2"] != "" and conf["RATP"]["sens2"] != "":
				i += 1
				ReponseRATP = SV.SVRATP(conf, "typetrans" + str(i), "line" + str(i), "station" + str(i), "sens" + str(i))
				if ReponseRATP.status_code == 200:
						return True
				else:
					print("Erreur dans la config RATP 2, veuillez vérifier votre saisie!")
					return False
			else: return True
		else:
			print("Erreur dans la config RATP 1, veuillez vérifier votre saisie!")
			return False
	else: return True

def TestTwitch():
	if conf["TWITCH"]["twitchapiclientid"] != "":
		i = 1
		ReponseID = SV.SVTwitchGetID(conf, "TwitchSt" + str(i))
		if ReponseID.status_code == 200:
			if conf["TWITCH"]["TwitchSt2"] != "":
				i += 1
				ReponseID = SV.SVTwitchGetID(conf, "TwitchSt" + str(i))
				if ReponseID.status_code == 200:
					return True
				else:
					print("Erreur dans la config Twitch, veuillez vérifier votre saisie!")
					return False
			else: return True
		else: 
			print("Erreur dans la config Twitch, veuillez vérifier votre saisie!")
			return False
	else: return True

def Adaptation():
	global Units

	if conf["WEATHER"]["Units"] == "imperial":
		Units = "°F"
	if conf["WEATHER"]["Units"] == "metric":
		Units = "°C"
	else:
		Units = "°K"

	main()

#APICheck()
#Adaptation()

if APICheck():
	Adaptation()
