import requests as rq
import time
import json
import sys
import os

A = 1

Creation = 0
Repeat = 0

def Main():
	try:
		while A == 1:
			global Creation
			Creation = 0
			Crypto()
			Meteo()
			Musique()
		#if Order == 3: Twitter() #WIP
		#if Order == 4: RATP() #WIP
	except KeyboardInterrupt:
		print("Vous avez arrêté le processus, nettoyage de l'écran")
		sys.exit()

def Crypto():
	global Creation
	global Repeat
	if Creation == 0:
		Creation = 1
		Repeat = 0

	ReponseCrypto = rq.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH&tsyms=USD&api_key=261d6b25933c3a0ccd3b991898b6ed86ac7815ec7ebedda674dd7ff116f23e51")
	DataCrypto = json.loads(ReponseCrypto.text)

	PCTBTC = list(str(DataCrypto["RAW"]["BTC"]["USD"]["CHANGEPCT24HOUR"]))
	del PCTBTC[-14:-1]
	PCTETH = list(str(DataCrypto["RAW"]["ETH"]["USD"]["CHANGEPCT24HOUR"]))
	del PCTETH[-14:-1]


	print(str(DataCrypto["RAW"]["BTC"]["USD"]["PRICE"]))
	print(str(DataCrypto["RAW"]["ETH"]["USD"]["PRICE"]))

	print("".join(PCTBTC))
	print("".join(PCTETH))

	time.sleep(3)

	Repeat += 1
	if Repeat == 6:
		return
	else:
		Crypto()

def Meteo():
	ReponseMeteo = rq.get("https://api.openweathermap.org/data/2.5/weather?q=Champigny-sur-Marne,fr&units=metric&lang=fr&appid=b3e6135efddd4b5f7ebc6add6fb003f3")
	DataMeteo = json.loads(ReponseMeteo.text)

	print(str(DataMeteo["main"]["temp"]))

	time.sleep(15)

def Musique():
	ReponseLastFM = rq.get("http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=Frederic94500&api_key=5bf1ea23824ae3745971ec27e036d3fa&limit=1&format=json")
	DataLast = json.loads(ReponseLastFM.text)

	TextEtImg.AddText("Last.fm:", 10, 10, size = 20, fontPath="Ubuntu.ttf")

	time.sleep(15)


Main()


