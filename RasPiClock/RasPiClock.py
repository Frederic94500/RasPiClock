# -*- encoding: utf-8 -*-
#RasPiClock - Frédéric94500, EliottCheypeplus, ParsaEtz

import time, json, sys, os, socket, configparser, hashlib
import requests as rq
from tkinter import *
from tkinter.messagebox import *

A = 0
Metric = "°C"
Imperial = "°F"

#Fonction Main
def Main():
	try:
		if A == 0:
			APICheck()
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

	finally:
		if Check == 4:
			A = 1
			return A

"""def Save():
	if HashOld =! HashNew:
		A = 0
"""

def Crypto(): #Fonction Crypto (CryproCompare)
	TextEtImg.AddImg("BTC.bmp", 10, 42, (44,44))
	TextEtImg.AddImg("ETH.bmp", 10, 100, (44,68))
	TextEtImg.AddText("Crypto:", 10, 10, size = 20, fontPath="Ubuntu.ttf")

	ReponseCrypto = rq.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=" + conf["CRYPTO"]["Coin1"] + "," + conf["CRYPTO"]["Coin2"] + "&tsyms=" + conf["CRYPTO"]["Currency"] + "&api_key=" + conf["API_KEY"]["CryptoAPI"])
	DataCrypto = json.loads(ReponseCrypto.text)

	PCTC1 = list(str(DataCrypto["RAW"][conf["CRYPTO"]["Coin1"]][conf["CRYPTO"]["Currency"]]["CHANGEPCT24HOUR"]))
	del PCTC1[-14:-1]
	PCTC2 = list(str(DataCrypto["RAW"][conf["CRYPTO"]["Coin2"]][conf["CRYPTO"]["Currency"]]["CHANGEPCT24HOUR"]))
	del PCTC2[-14:-1]

	TextEtImg.AddText(conf["CRYPTO"]["Currency"] + " " + str(DataCrypto["RAW"][conf["CRYPTO"]["Coin1"]][conf["CRYPTO"]["Currency"]]["PRICE"]), 64, 44, size = 30, fontPath="Ubuntu.ttf")
	TextEtImg.AddText(conf["CRYPTO"]["Currency"] + " " + str(DataCrypto["RAW"][conf["CRYPTO"]["Coin2"]][conf["CRYPTO"]["Currency"]]["PRICE"]), 64, 114, size = 30, fontPath="Ubuntu.ttf")
	TextEtImg.AddText("".join(PCTC1) + "%", 64, 74, size = 15, fontPath="Ubuntu.ttf")
	TextEtImg.AddText("".join(PCTC2) + "%", 64, 144, size = 15, fontPath="Ubuntu.ttf")

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

conf = configparser.ConfigParser()
conf.read("config.cfg")

if os.path.exists('/etc/default/epd-fuse'):
	from papirus import Papirus, PapirusComposite
	Ecran = Papirus()
	TextEtImg = PapirusComposite(False)
	TextEtImg.Clear()

	Main()
else:
	print("ATTENTION, vous n'avez pas installé la biblothèque Papirus, veuillez l'installer via https://github.com/PiSupply/PaPiRus") #Phrase temp
	sys.exit()
