# -*- encoding: utf-8 -*-
#RasPiClock - Frédéric94500, EliottCheypeplus, ParsaEtz

import time, json, sys, os, socket, configparser
import requests as rq
from tkinter import *
from tkinter.messagebox import *

A = 0

def LibCheck():
	try:
		from papirus import Papirus, PapirusComposite
		Ecran = Papirus()
		TextEtImg = PapirusComposite(False)
		TextEtImg.Clear()

		Main()
	except ModuleNotFoundError:
		print("ATTENTION, vous n'avez pas installé la biblothèque Papirus, veuillez l'installer") #Phrase temp
		sys.exit()

def Main():
	try:
		while A == 0:
			Crypto()
			Meteo()
			Musique()
			Social()
		#if Order == 4: RATP() #WIP
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

def Crypto():
	TextEtImg.AddImg("BTC.bmp", 10, 42, (44,44))
	TextEtImg.AddImg("ETH.bmp", 10, 100, (44,68))
	TextEtImg.AddText("Crypto:", 10, 10, size = 20, fontPath="Ubuntu.ttf")

	ReponseCrypto = rq.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH&tsyms=USD&api_key=" + conf["API_KEY"]["CryptoAPI"])
	DataCrypto = json.loads(ReponseCrypto.text)

	PCTBTC = list(str(DataCrypto["RAW"]["BTC"]["USD"]["CHANGEPCT24HOUR"]))
	del PCTBTC[-14:-1]
	PCTETH = list(str(DataCrypto["RAW"]["ETH"]["USD"]["CHANGEPCT24HOUR"]))
	del PCTETH[-14:-1]

	TextEtImg.AddText("$ " + str(DataCrypto["RAW"]["BTC"]["USD"]["PRICE"]), 64, 44, size = 30, fontPath="Ubuntu.ttf")
	TextEtImg.AddText("$ " + str(DataCrypto["RAW"]["ETH"]["USD"]["PRICE"]), 64, 114, size = 30, fontPath="Ubuntu.ttf")
	TextEtImg.AddText("".join(PCTBTC) + "%", 64, 74, size = 15, fontPath="Ubuntu.ttf")
	TextEtImg.AddText("".join(PCTETH) + "%", 64, 144, size = 15, fontPath="Ubuntu.ttf")

	TextEtImg.WriteAll(True)
	time.sleep(15)
	TextEtImg.Clear()

def Meteo():
	ReponseMeteo = rq.get("https://api.openweathermap.org/data/2.5/weather?q=Champigny-sur-Marne,fr&units=metric&lang=fr&appid=" + conf["API_KEY"]["MeteoAPI"])
	DataMeteo = json.loads(ReponseMeteo.text)

	TextEtImg.AddText("Météo:", 10, 10, size = 20, fontPath="Ubuntu.ttf")
	TextEtImg.AddText("Température: " + str(DataMeteo["main"]["temp"]) + "°C", 10, 40, size = 25, fontPath="Ubuntu.ttf")
	TextEtImg.AddText("Temp. Min: " + str(DataMeteo["main"]["temp_min"]) + "°C" + " Temp. Max: " + str(DataMeteo["main"]["temp_max"]) + "°C", 10, 65, size = 12, fontPath="Ubuntu.ttf")
	TextEtImg.AddText("Temps: " + DataMeteo["weather"][0]["description"], 10, 85, size = 25, fontPath="Ubuntu.ttf") 

	TextEtImg.WriteAll(True)
	time.sleep(15)
	TextEtImg.Clear()

def Musique():
	ReponseLastFM = rq.get("http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=Frederic94500&limit=1&format=json&api_key=" + conf["API_KEY"]["LastFmAPI"])
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
		TextEtImg.WriteAll(True)
		time.sleep(15)
		TextEtImg.Clear()

def Social():
	ReponseTwitter = rq.get("https://api.twitter.com/1.1/users/show.json?screen_name=Frederic94500", headers={'Authorization': "Bearer " + conf["API_KEY"]["TwitterAPI"]})
	DataTwitter = json.loads(ReponseTwitter.text)

	ReponseTwitchZ = rq.get("https://api.twitch.tv/helix/streams?user_login=zerator", headers={"Client-ID": conf["API_KEY"]["TwitchAPI"]})
	ReponseTwitchMV = rq.get("https://api.twitch.tv/helix/streams?user_login=mistermv", headers={"Client-ID": conf["API_KEY"]["TwitchAPI"]})
	DataZ = json.loads(ReponseTwitchZ.text)
	DataMV = json.loads(ReponseTwitchMV.text)

	TextEtImg.AddText("Réseaux Sociaux:", 10, 10, size = 20, fontPath="Ubuntu.ttf")
	TextEtImg.AddText("Twitter: " + str(DataTwitter["followers_count"]) + " Followers", 10, 40, size = 25, fontPath="Ubuntu.ttf")
	TextEtImg.AddText("Twitch:", 10, 75, size = 25, fontPath="Ubuntu.ttf")

	try:
		if DataZ["data"][0]["type"] == "live":
			TextEtImg.AddText("ZeratoR: ON", 10, 100, size = 20, fontPath="Ubuntu.ttf")
	except IndexError:
		TextEtImg.AddText("ZeratoR: OFF", 10, 100, size = 20, fontPath="Ubuntu.ttf")
	try:
		if DataMV["data"][0]["type"] == "live":
			TextEtImg.AddText("MisterMV: ON", 10, 130, size = 20, fontPath="Ubuntu.ttf")
	except IndexError:
		TextEtImg.AddText("MisterMV: OFF", 10, 130, size = 20, fontPath="Ubuntu.ttf")
	finally:
		TextEtImg.WriteAll(True)
		time.sleep(15)
		TextEtImg.Clear()

conf = configparser.ConfigParser()
conf.read("config.cfg")

Main()


