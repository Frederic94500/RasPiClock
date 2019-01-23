# coding: utf-8

import requests as rq
import threading as th
import time
import json
import sys
import os

import API

from papirus import Papirus
from papirus import PapirusComposite

A = 1

Creation = 0
Repeat = 0

class Main(th):

	def Main():
		try:
			while A == 1:
				global Creation
				Creation = 0
				Crypto()
				Meteo()
				Musique()
				Social()
			#if Order == 4: RATP() #WIP
		except KeyboardInterrupt:
			print("Vous avez arrêté le processus, nettoyage de l'écran")
			os.system("papirus-clear")
			sys.exit()

	def Crypto():
		global Creation
		global Repeat
		if Creation == 0:
			TextEtImg.AddImg("BTC.bmp", 10, 42, (44,44))
			TextEtImg.AddImg("ETH.bmp", 10, 100, (44,68))
			TextEtImg.AddText("Crypto:", 10, 10, size = 20, fontPath="Ubuntu.ttf")
			TextEtImg.AddText("$ BTC", 64, 44, Id="BitcoinP", size = 30)
			TextEtImg.AddText("$ ETH", 64, 114, Id="EthereumP", size = 30)
			TextEtImg.AddText("% BTC", 64, 74, Id="BitcoinPCT", size = 15)
			TextEtImg.AddText("% ETH", 64, 144, Id="EthereumPCT", size = 15)
			Creation = 1
			Repeat = 0

		DataCrypto = json.loads(API.ReponseCrypto.text)

		PCTBTC = list(str(DataCrypto["RAW"]["BTC"]["USD"]["CHANGEPCT24HOUR"]))
		del PCTBTC[-14:-1]
		PCTETH = list(str(DataCrypto["RAW"]["ETH"]["USD"]["CHANGEPCT24HOUR"]))
		del PCTETH[-14:-1]

		TextEtImg.UpdateText("BitcoinP", "$ " + str(DataCrypto["RAW"]["BTC"]["USD"]["PRICE"]), fontPath="Ubuntu.ttf")
		TextEtImg.UpdateText("EthereumP", "$ " + str(DataCrypto["RAW"]["ETH"]["USD"]["PRICE"]), fontPath="Ubuntu.ttf")
		TextEtImg.UpdateText("BitcoinPCT", "".join(PCTBTC) + "%", fontPath="Ubuntu.ttf")
		TextEtImg.UpdateText("EthereumPCT", "".join(PCTETH) + "%", fontPath="Ubuntu.ttf")

		TextEtImg.WriteAll(True)
		time.sleep(3)
		Repeat += 1
		if Repeat == 6:
			TextEtImg.Clear()
			return
		else:
			Crypto()

	def Meteo():
		DataMeteo = json.loads(API.ReponseMeteo.text)

		TextEtImg.AddText("Météo:", 10, 10, size = 20, fontPath="Ubuntu.ttf")
		TextEtImg.AddText("Temperature: " + str(DataMeteo["main"]["temp"]) + "°C", 10, 40, size = 25, fontPath="Ubuntu.ttf")
		TextEtImg.AddText("Temp Min: " + str(DataMeteo["main"]["temp_min"]) + "°C" + " Temp Max: " + str(DataMeteo["main"]["temp_max"]) + "°C", 10, 65, size = 12, fontPath="Ubuntu.ttf")
		TextEtImg.AddText("Temps: " + DataMeteo["weather"][0]["description"], 10, 85, size = 25, fontPath="Ubuntu.ttf") 

		TextEtImg.WriteAll(True)
		time.sleep(15)
		TextEtImg.Clear()

	def Musique():
		DataLast = json.loads(API.ReponseLastFM.text)

		TextEtImg.AddText("Last.fm:", 10, 10, size = 20, fontPath="Ubuntu.ttf")

		try:
			if DataLast["recenttracks"]["track"][0]["@attr"]["nowplaying"] == "true":
				TextEtImg.AddText("Actuellement:", 10, 40, size = 25, fontPath="Ubuntu.ttf")
				TextEtImg.AddText(DataLast["recenttracks"]["track"][0]["artist"]["#text"] + " - " + DataLast["recenttracks"]["track"][0]["name"], 10, 65, size = 15, fontPath="Ubuntu.ttf")
				TextEtImg.AddText(DataLast["recenttracks"]["track"][0]["album"]["#text"], 10, 95, size = 10, fontPath="Ubuntu.ttf")

				TextEtImg.AddText("Précédent:", 10, 115, size = 25, fontPath="Ubuntu.ttf")
				TextEtImg.AddText(DataLast["recenttracks"]["track"][1]["artist"]["#text"] + " - " + DataLast["recenttracks"]["track"][1]["name"], 10, 140, size = 15, fontPath="Ubuntu.ttf")
		except KeyError:
			TextEtImg.AddText("Précédent:", 10, 40, size = 25, fontPath="Ubuntu.ttf")
			TextEtImg.AddText(DataLast["recenttracks"]["track"][0]["artist"]["#text"] + " - " + DataLast["recenttracks"]["track"][0]["name"], 10, 65, size = 15, fontPath="Ubuntu.ttf")
			TextEtImg.AddText(DataLast["recenttracks"]["track"][0]["album"]["#text"], 10, 95, size = 10, fontPath="Ubuntu.ttf")
		finally:
			TextEtImg.WriteAll(True)
			time.sleep(15)
			TextEtImg.Clear()

	def Social():
		DataTwitter = json.loads(API.ReponseTwitter.text)

		DataZ = json.loads(API.ReponseTwitchZ.text)
		DataMV = json.loads(API.ReponseTwitchMV.text)

		TextEtImg.AddText("Réseaux Sociaux:", 10, 10, size = 20, fontPath="Ubuntu.ttf")

		TextEtImg.AddText("Twitter: " + str(DataTwitter["followers_count"]) + " Followers", 10, 40, size = 25, fontPath="Ubuntu.ttf")
		TextEtImg.AddText("Twitch:", 10, 75, size = 25, fontPath="Ubuntu.ttf")

		try:
			if DataZ["data"][0]["type"] == "live":
				TextEtImg.AddText("ZeratoR: ON", 10, 100, size = 20, fontPath="Ubuntu.ttf")
		except IndexError:
			TextEtImg.AddText("Zerator: OFF", 10, 100, size = 20, fontPath="Ubuntu.ttf")

		try:
			if DataMV["data"][0]["type"] == "live":
				TextEtImg.AddText("MisterMV: ON", 10, 130, size = 20, fontPath="Ubuntu.ttf")
		except IndexError:
			TextEtImg.AddText("MisterMV: OFF", 10, 130, size = 20, fontPath="Ubuntu.ttf")

		finally:
			TextEtImg.WriteAll(True)
			time.sleep(15)
			TextEtImg.Clear()


Ecran = Papirus()
TextEtImg = PapirusComposite(False)

TextEtImg.Clear()

thread_1 = Main()
thread_2 = API.API()

thread_1.start()
thread_2.start()


