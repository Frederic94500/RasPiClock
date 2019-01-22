import requests as rq
import time
import json
import sys
import os

from papirus import Papirus
from papirus import PapirusComposite

Creation = 0
Repeat = 0
global Order
Order = 0

def Ordre(Order):
	try:
		TextEtImg.Clear() #WIP
		if Order == 0:
			Creation = 0
			Crypto()
		if Order == 1: Meteo()
		if Order == 2: Musique()
		if Order == 3: Twitter() #WIP
		if Order == 4: RATP() #WIP
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

	ReponseCrypto = rq.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH&tsyms=USD&api_key=261d6b25933c3a0ccd3b991898b6ed86ac7815ec7ebedda674dd7ff116f23e51")
	DataCrypto = json.loads(ReponseCrypto.text)

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
		Order = 1
		Ordre(Order)
	else:
		Crypto()

def Meteo():
	ReponseMeteo = rq.get("https://api.openweathermap.org/data/2.5/weather?q=Champigny-sur-Marne,fr&units=metric&lang=fr&appid=b3e6135efddd4b5f7ebc6add6fb003f3")
	DataMeteo = json.loads(ReponseMeteo.text)

	TextEtImg.AddText("Météo:", 10, 10, size = 20, fontPath="Ubuntu.ttf")
	TextEtImg.AddText("Temperature: " + str(DataMeteo["main"]["temp"]) + "°C", 10, 40, size = 25, fontPath="Ubuntu.ttf")
	TextEtImg.AddText("Temp Min: " + str(DataMeteo["main"]["temp_min"]) + "°C" + " Temp Max: " + str(DataMeteo["main"]["temp_max"]) + "°C", 10, 65, size = 12, fontPath="Ubuntu.ttf")
	TextEtImg.AddText("Temps: " + DataMeteo["weather"][0]["description"], 10, 85, size = 25, fontPath="Ubuntu.ttf") 

	TextEtImg.WriteAll(True)

	time.sleep(15)

	Order = 2
	Ordre(Order)

def Musique():
	ReponseLastFM = rq.get("http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=Frederic94500&api_key=5bf1ea23824ae3745971ec27e036d3fa&limit=1&format=json")
	DataLast = json.loads(ReponseLastFM.text)

	TextEtImg.AddText("Last.fm:", 10, 10, size = 20, fontPath="Ubuntu.ttf")

	try:
		if DataLast["recenttracks"]["track"][0]["@attr"]["nowplaying"] == "true":
			TextEtImg.AddText("Actuellement:", 10, 40, size = 25, fontPath="Ubuntu.ttf")
			TextEtImg.AddText(DataLast["recenttracks"]["track"][0]["artist"]["#text"] + " - " + DataLast["recenttracks"]["track"][0]["name"], 10, 65, size = 15, fontPath="Ubuntu.ttf")
			TextEtImg.AddText(DataLast["recenttracks"]["track"][0]["album"]["#text"], 10, 80, size = 10, fontPath="Ubuntu.ttf")

			TextEtImg.AddText("Précédent:", 10, 115, size = 25, fontPath="Ubuntu.ttf")
			TextEtImg.AddText(DataLast["recenttracks"]["track"][1]["artist"]["#text"] + " - " + DataLast["recenttracks"]["track"][0]["name"], 10, 140, size = 15, fontPath="Ubuntu.ttf")
			TextEtImg.AddText(DataLast["recenttracks"]["track"][1]["album"]["#text"], 10, 155, size = 10, fontPath="Ubuntu.ttf")
	
	except KeyError:
		TextEtImg.AddText("Précédent:", 10, 40, size = 25, fontPath="Ubuntu.ttf")
		TextEtImg.AddText(DataLast["recenttracks"]["track"][0]["artist"]["#text"] + " - " + DataLast["recenttracks"]["track"][0]["name"], 10, 65, size = 15, fontPath="Ubuntu.ttf")
		TextEtImg.AddText(DataLast["recenttracks"]["track"][0]["album"]["#text"], 10, 80, size = 10, fontPath="Ubuntu.ttf")

	TextEtImg.WriteAll(True)

	time.sleep(15)

	Order = 0
	Crypto()

Ecran = Papirus()
TextEtImg = PapirusComposite(False)

Ordre(Order)


