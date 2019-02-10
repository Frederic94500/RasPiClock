# -*- encoding: utf-8 -*-

import requests as rq
import time, json, sys, os, socket

from papirus import Papirus, PapirusComposite

A = 0
CryptoPrix = ["BitcoinP", "BitcoinPCT", "EthereumP", "EthereumPCT"]
IMG = ["BTC", "ETH"]

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
	ReponseCrypto = rq.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH&tsyms=USD&api_key=261d6b25933c3a0ccd3b991898b6ed86ac7815ec7ebedda674dd7ff116f23e51")
	DataCrypto = json.loads(ReponseCrypto.text)

	PCTBTC = list(str(DataCrypto["RAW"]["BTC"]["USD"]["CHANGEPCT24HOUR"]))
	del PCTBTC[-14:-1]
	PCTETH = list(str(DataCrypto["RAW"]["ETH"]["USD"]["CHANGEPCT24HOUR"]))
	del PCTETH[-14:-1]

	TextEtImg.UpdateText("Titre", "Crypto:", fontPath="Ubuntu.ttf")

	TextEtImg.AddImg("BTC.bmp", 10, 42, (44,44), Id=IMG[0])
	TextEtImg.AddImg("ETH.bmp", 10, 100, (44,68), Id=IMG[1])

	TextEtImg.UpdateText("BitcoinP", "$ " + str(DataCrypto["RAW"]["BTC"]["USD"]["PRICE"]), fontPath="Ubuntu.ttf")
	TextEtImg.UpdateText("BitcoinPCT", "".join(PCTBTC) + "%", fontPath="Ubuntu.ttf")
	TextEtImg.UpdateText("EthereumP", "$ " + str(DataCrypto["RAW"]["ETH"]["USD"]["PRICE"]), fontPath="Ubuntu.ttf")
	TextEtImg.UpdateText("EthereumPCT", "".join(PCTETH) + "%", fontPath="Ubuntu.ttf")

	TextEtImg.WriteAll(True)
	time.sleep(15)

	for I in range(4):
		TextEtImg.UpdateText(CryptoPrix[I], "", fontPath="Ubuntu.ttf")
	for I in range(2):
		TextEtImg.RemoveImg(IMG[I])
	return

def Meteo():
	ReponseMeteo = rq.get("https://api.openweathermap.org/data/2.5/weather?q=Champigny-sur-Marne,fr&units=metric&lang=fr&appid=b3e6135efddd4b5f7ebc6add6fb003f3")
	DataMeteo = json.loads(ReponseMeteo.text)

	TextEtImg.UpdateText("Titre", "Météo:", fontPath="Ubuntu.ttf")
	TextEtImg.AddText("Température: " + str(DataMeteo["main"]["temp"]) + "°C", 10, 40, size = 25, fontPath="Ubuntu.ttf")
	TextEtImg.AddText("Temp. Min: " + str(DataMeteo["main"]["temp_min"]) + "°C" + " Temp. Max: " + str(DataMeteo["main"]["temp_max"]) + "°C", 10, 65, size = 12, fontPath="Ubuntu.ttf")
	TextEtImg.AddText("Temps: " + DataMeteo["weather"][0]["description"], 10, 85, size = 25, fontPath="Ubuntu.ttf") 

	TextEtImg.WriteAll(True)
	time.sleep(15)
	TextEtImg.Clear()

def Musique():
	ReponseLastFM = rq.get("http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=Frederic94500&api_key=5bf1ea23824ae3745971ec27e036d3fa&limit=1&format=json")
	DataLast = json.loads(ReponseLastFM.text)

	TextEtImg.UpdateText("Titre", "Last.fm:", fontPath="Ubuntu.ttf")
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
	ReponseTwitter = rq.get("https://api.twitter.com/1.1/users/show.json?screen_name=Frederic94500", headers={'Authorization': "Bearer AAAAAAAAAAAAAAAAAAAAAGRr9QAAAAAApU6cp18UYHWmOtfqvvPZ783n7kI%3DVcwCE2OxcjpJuaR6bFdUAkF6gQQDlBgYHqLpSVYciHgeQRQEfF"})
	DataTwitter = json.loads(ReponseTwitter.text)

	ReponseTwitchZ = rq.get("https://api.twitch.tv/helix/streams?user_login=zerator", headers={"Client-ID": "6k8zx7uira85jc67wzh5m03sxzn4xb"})
	ReponseTwitchMV = rq.get("https://api.twitch.tv/helix/streams?user_login=mistermv", headers={"Client-ID": "6k8zx7uira85jc67wzh5m03sxzn4xb"})
	DataZ = json.loads(ReponseTwitchZ.text)
	DataMV = json.loads(ReponseTwitchMV.text)

	TextEtImg.UpdateText("Titre", "Réseaux Sociaux:", fontPath="Ubuntu.ttf")
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


Ecran = Papirus()
TextEtImg = PapirusComposite(False)

TextEtImg.Clear()

TextEtImg.AddText("", 10, 10, Id="Titre", size = 30)

TextEtImg.AddText("", 64, 44, Id="BitcoinP", size = 30)
TextEtImg.AddText("", 64, 74, Id="BitcoinPCT", size = 15)
TextEtImg.AddText("", 64, 114, Id="EthereumP", size = 30)
TextEtImg.AddText("", 64, 144, Id="EthereumPCT", size = 15)


Main()


