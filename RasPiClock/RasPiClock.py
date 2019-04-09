# -*- encoding: utf-8 -*-
#RasPiClock - Frédéric94500, EliottCheypeplus, ParsaEtz

import time, json, sys, os, socket, configparser, hashlib
import requests as rq
from tkinter import *
from tkinter.messagebox import *

Metric = "°C"
Imperial = "°F"

#Fonction Main
def Main():
	A = 0
	try:
		Save()
		if A == 0:
			APICheck()
			A = 1
		while A == 1:
			Crypto()
			Meteo()
			Musique()
			Social()
			#RATP() #WIP?
	except (ValueError, socket.error, socket.gaierror, socket.herror, socket.timeout):
		TextEtImg.Clear()
		TextEtImg.AddText("ERREUR de connexion, nouvelle tentative de connexion dans: T", 10, 48, size = 20, fontPath="Ubuntu.ttf", Id="TimerErr")
		for I in range(15):
			TextEtImg.UpdateText("TimerErr", "ERREUR de connexion, \nnouvelle tentative de connexion dans: " + str(15 - I), fontPath="Ubuntu.ttf")
			TextEtImg.WriteAll(True)
			time.sleep(1)
		TextEtImg.Clear()
		Main()
	except KeyboardInterrupt:
		print("Vous avez arrêté le processus, nettoyage de l'écran")
		os.system("papirus-clear")
		sys.exit()

#Fonction de test de chaque paramètre (sauf Twitch)
def APICheck():
	Check = 0
	ReponseCrypto = rq.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=" + conf["CRYPTO"]["Coin1"] + "," + conf["CRYPTO"]["Coin2"] + "&tsyms=" + conf["CRYPTO"]["Currency"] + "&api_key=" + conf["API_KEY"]["CryptoAPI"])
	DataCrypto = json.loads(ReponseCrypto.text)
	ReponseMeteo = rq.get("https://api.openweathermap.org/data/2.5/weather?q=" + conf["WEATHER"]["City"] + "&units=" + conf["WEATHER"]["Units"] + "&lang=" + conf["WEATHER"]["Lang"] + "&appid=" + conf["API_KEY"]["MeteoAPI"])
	DataMeteo = json.loads(ReponseMeteo.text)
	ReponseLastFM = rq.get("http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=" + conf["LASTFM"]["UserFM"] + "&limit=1&format=json&api_key=" + conf["API_KEY"]["LastFmAPI"])
	DataLast = json.loads(ReponseLastFM.text)
	ReponseTwitter = rq.get("https://api.twitter.com/1.1/users/show.json?screen_name=" + conf["SOCIAL"]["UserTW"], headers={'Authorization': "Bearer " + conf["API_KEY"]["TwitterAPI"]})
	DataTwitter = json.loads(ReponseTwitter.text)

	try:
		if DataCrypto["Response"] == "Error":
			print("Erreur dans la config Crypto, veuiller vérifier votre saisie!")
			sys.exit()
	except:
		Check += 1

	try:
		if DataMeteo["cod"] == range(400, 599):
			print("Erreur dans la config Météo, veuiller vérifier votre saisie!")
			sys.exit()
	except:
		Check += 1

	try:
		if DataLast["error"] == range(2, 29):
			print("Erreur dans la config LastFM, veuiller vérifier votre saisie!")
			sys.exit()
	except:
		Check += 1
	try:
		if DataTwitter["errors"][0]["code"] == range(49, 599):
			print("Erreur dans la config Twitter, veuiller vérifier votre saisie!")
			sys.exit()
	except:
		Check += 1

	if Check == 4:
		with open("config.conf","rb") as f:
			bytes = f.read()
			hashconf = hashlib.sha256(bytes).hexdigest()

		hash = open("hash.txt", "w")
		hash.write(hashconf)
		hash.close


def Save(): #Fonction d'enregistrement du fichier de conf
	conf["API-KEY"]["CryptoAPI"] = ZTCryptoAPI.get()
	conf["API-KEY"]["MeteoAPI"] = ZTMeteoAPI.get()
	conf["API-KEY"]["LastFmAPI"] = ZTLastFmAPI.get()
	conf["API-KEY"]["TwitterAPI"] = ZTLastFmAPI.get()
	conf["API-KEY"]["TwitchAPI"] = ZTLastFmAPI.get()

	conf["CRYPTO"]["Currency"] = ZTCCurrency.get()
	conf["CRYPTO"]["Coin1"] = ZTCCoin1.get()
	conf["CRYPTO"]["Coin2"] = ZTCCoin2.get()

	conf["WEATHER"]["City"] = ZTWCity.get()
	conf["WEATHER"]["Units"] = ZTWUnits.get()
	conf["WEATHER"]["Lang"] = ZTWLang.get()

	conf["LASTFM"]["UserFM"] = ZTFUserFM.get()

	conf["SOCIAL"]["UserTW"] = ZTSUserTW.get()

	conf["SOCIAL"]["TwitchSt1"] = ZTSTwitchSt1.get()
	conf["SOCIAL"]["TwitchSt2"] = ZTSTwitchSt2.get()

	with open('config.cfg', 'w') as configfile:
		config.write(configfile)
	
	with open('config.conf', "rb") as FC:
		bytes = FC.read()
		HashNew = hashlib.sha256(bytes).hexdigest()
	
	FH = open('hash.txt', "r")
	HashOld = FH.read()

	if HashOld != HashNew:
		A = 0
		return A
	if HashOld == HashNew:
		A = 1
		return A


def Crypto(): #Fonction Crypto (CryproCompare)
	TextEtImg.AddText("Crypto:", 10, 10, size = 20, fontPath="Ubuntu.ttf")

	ReponseCrypto = rq.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=" + conf["CRYPTO"]["Coin1"] + "," + conf["CRYPTO"]["Coin2"] + "&tsyms=" + conf["CRYPTO"]["Currency"] + "&api_key=" + conf["API_KEY"]["CryptoAPI"])
	DataCrypto = json.loads(ReponseCrypto.text)

	PCTC1 = list(str(DataCrypto["RAW"][conf["CRYPTO"]["Coin1"]][conf["CRYPTO"]["Currency"]]["CHANGEPCT24HOUR"]))
	del PCTC1[-14:-1]
	PCTC2 = list(str(DataCrypto["RAW"][conf["CRYPTO"]["Coin2"]][conf["CRYPTO"]["Currency"]]["CHANGEPCT24HOUR"]))
	del PCTC2[-14:-1]

	TextEtImg.AddText(conf["CRYPTO"]["Coin1"] + " " + conf["CRYPTO"]["Currency"] + " " + str(DataCrypto["RAW"][conf["CRYPTO"]["Coin1"]][conf["CRYPTO"]["Currency"]]["PRICE"]), 10, 44, size = 25, fontPath="Ubuntu.ttf")
	TextEtImg.AddText(conf["CRYPTO"]["Coin1"] + " " + conf["CRYPTO"]["Currency"] + " " + str(DataCrypto["RAW"][conf["CRYPTO"]["Coin2"]][conf["CRYPTO"]["Currency"]]["PRICE"]), 10, 114, size = 25, fontPath="Ubuntu.ttf")
	TextEtImg.AddText("".join(PCTC1) + "%", 10, 74, size = 15, fontPath="Ubuntu.ttf")
	TextEtImg.AddText("".join(PCTC2) + "%", 10, 144, size = 15, fontPath="Ubuntu.ttf")

	TextEtImg.AddText(time.strftime("%H:%M", time.localtime()), 200, 10, size = 20, fontPath="Ubuntu.ttf")

	TextEtImg.WriteAll(True)
	time.sleep(15)
	TextEtImg.Clear()

def Meteo(): #Fonction Météo (OpenWeatherMap)
	ReponseMeteo = rq.get("https://api.openweathermap.org/data/2.5/weather?q=" + conf["WEATHER"]["City"] + "&units=" + conf["WEATHER"]["Units"] + "&lang=" + conf["WEATHER"]["Lang"] + "&appid=" + conf["API_KEY"]["MeteoAPI"])
	DataMeteo = json.loads(ReponseMeteo.text)

	TextEtImg.AddText("Météo:", 10, 10, size = 20, fontPath="Ubuntu.ttf")
	TextEtImg.AddText("Température: " + str(DataMeteo["main"]["temp"]) + "°C", 10, 40, size = 25, fontPath="Ubuntu.ttf")
	TextEtImg.AddText("Temp. Min: " + str(DataMeteo["main"]["temp_min"]) + "°C" + " Temp. Max: " + str(DataMeteo["main"]["temp_max"]) + "°C", 10, 65, size = 12, fontPath="Ubuntu.ttf")
	TextEtImg.AddText("Temps: " + DataMeteo["weather"][0]["description"], 10, 85, size = 25, fontPath="Ubuntu.ttf") 

	TextEtImg.AddText(time.strftime("%H:%M", time.localtime()), 200, 10, size = 20, fontPath="Ubuntu.ttf")

	TextEtImg.WriteAll(True)
	time.sleep(15)
	TextEtImg.Clear()

def Musique(): #Fonction Musique (Last.fm)
	ReponseLastFM = rq.get("http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=" + conf["LASTFM"]["UserFM"] + "&limit=1&format=json&api_key=" + conf["API_KEY"]["LastFmAPI"])
	DataLast = json.loads(ReponseLastFM.text)

	TextEtImg.AddText("Last.fm:", 10, 10, size = 20, fontPath="Ubuntu.ttf")
	try:
		if DataLast["recenttracks"]["track"][0]["@attr"]["nowplaying"] == "true":
			TextEtImg.AddText("Actuellement:", 10, 40, size = 25, fontPath="Ubuntu.ttf")
			TextEtImg.AddText(DataLast["recenttracks"]["track"][0]["artist"]["#text"] + " - " + DataLast["recenttracks"]["track"][0]["name"], 10, 65, size = 15, fontPath="Ubuntu.ttf")
			TextEtImg.AddText(DataLast["recenttracks"]["track"][0]["album"]["#text"], 10, 95, size = 10, fontPath="Ubuntu.ttf")

			TextEtImg.AddText("Précédent:", 10, 115, size = 25, fontPath="Ubuntu.ttf")
			TextEtImg.AddText(DataLast["recenttracks"]["track"][1]["artist"]["#text"] + " - " + DataLast["recenttracks"]["track"][1]["name"], 10, 140, size = 15, fontPath="Ubuntu.ttf")
	except:
		TextEtImg.AddText("Précédent:", 10, 40, size = 25, fontPath="Ubuntu.ttf")
		TextEtImg.AddText(DataLast["recenttracks"]["track"][0]["artist"]["#text"] + " - " + DataLast["recenttracks"]["track"][0]["name"], 10, 65, size = 15, fontPath="Ubuntu.ttf")
		TextEtImg.AddText(DataLast["recenttracks"]["track"][0]["album"]["#text"], 10, 95, size = 10, fontPath="Ubuntu.ttf")
	finally:
		TextEtImg.AddText(time.strftime("%H:%M", time.localtime()), 200, 10, size = 20, fontPath="Ubuntu.ttf")
		TextEtImg.WriteAll(True)
		time.sleep(15)
		TextEtImg.Clear()

def Social(): #Fonction Réseaux Sociaux (Twitch & Twitter)
	ReponseTwitter = rq.get("https://api.twitter.com/1.1/users/show.json?screen_name=" + conf["SOCIAL"]["UserTW"], headers={'Authorization': "Bearer " + conf["API_KEY"]["TwitterAPI"]})
	DataTwitter = json.loads(ReponseTwitter.text)

	ReponseTwitchSt1 = rq.get("https://api.twitch.tv/helix/streams?user_login=" + conf["SOCIAL"]["TwitchSt1"], headers={"Client-ID": conf["API_KEY"]["TwitchAPI"]})
	ReponseTwitchSt2 = rq.get("https://api.twitch.tv/helix/streams?user_login=" + conf["SOCIAL"]["TwitchSt2"], headers={"Client-ID": conf["API_KEY"]["TwitchAPI"]})
	DataSt1 = json.loads(ReponseTwitchSt1.text)
	DataSt2 = json.loads(ReponseTwitchSt2.text)

	TextEtImg.AddText("Réseaux Sociaux:", 10, 10, size = 20, fontPath="Ubuntu.ttf")
	TextEtImg.AddText("Twitter: " + str(DataTwitter["followers_count"]) + " Followers", 10, 40, size = 25, fontPath="Ubuntu.ttf")
	TextEtImg.AddText("Twitch:", 10, 75, size = 25, fontPath="Ubuntu.ttf")

	try:
		if DataSt1["data"][0]["type"] == "live":
			TextEtImg.AddText(conf["SOCIAL"]["TwitchSt1"] + ": ON", 10, 100, size = 20, fontPath="Ubuntu.ttf")
	except IndexError:
		TextEtImg.AddText(conf["SOCIAL"]["TwitchSt1"] + ": OFF", 10, 100, size = 20, fontPath="Ubuntu.ttf")
	try:
		if DataSt2["data"][0]["type"] == "live":
			TextEtImg.AddText(conf["SOCIAL"]["TwitchSt2"] + ": ON", 10, 130, size = 20, fontPath="Ubuntu.ttf")
	except IndexError:
		TextEtImg.AddText(conf["SOCIAL"]["TwitchSt2"] + ": OFF", 10, 130, size = 20, fontPath="Ubuntu.ttf")
	finally:
		TextEtImg.AddText(time.strftime("%H:%M", time.localtime()), 200, 10, size = 20, fontPath="Ubuntu.ttf")
		TextEtImg.WriteAll(True)
		time.sleep(15)
		TextEtImg.Clear()

#def GUI(): #Fonction pour l'interface (en attente du merge)

conf = configparser.ConfigParser()
conf.read("config.cfg")

if os.path.exists('/etc/default/epd-fuse'):
	from papirus import Papirus, PapirusComposite
	Ecran = Papirus()
	TextEtImg = PapirusComposite(False)
	TextEtImg.Clear()

	#GUI() (en attente)
	Main() #Sera remplacé par le bouton "Afficher"
else:
	print("ATTENTION, vous n'avez pas installé la biblothèque Papirus, veuillez l'installer via https://github.com/PiSupply/PaPiRus") #Phrase temp
	sys.exit()
