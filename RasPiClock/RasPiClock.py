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
		TextEtImg.Clear()
		if Order == 0:
			Creation = 0
			Crypto()
		if Order == 1: Meteo() #WIP
		if Order == 2: Musique() #WIP
		if Order == 3: RATP() #WIP
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

	ReponseCrypto = rq.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH&tsyms=USD&api_key=261d6b25933c3a0ccd3b991898b6ed86ac7815ec7ebedda674dd7ff116f23e51")
	DataCrypto = json.loads(ReponseCrypto.text)

	PriceBTC = str(DataCrypto["RAW"]["BTC"]["USD"]["PRICE"])
	PCTBTC = list(str(DataCrypto["RAW"]["BTC"]["USD"]["CHANGEPCT24HOUR"]))
	del PCTBTC[-14:-1]

	PriceETH = str(DataCrypto["RAW"]["ETH"]["USD"]["PRICE"])
	PCTETH = list(str(DataCrypto["RAW"]["ETH"]["USD"]["CHANGEPCT24HOUR"]))
	del PCTETH[-14:-1]

	TextEtImg.UpdateText("BitcoinP", "$ " + PriceBTC, fontPath="Ubuntu.ttf")
	TextEtImg.UpdateText("EthereumP", "$ " + PriceETH, fontPath="Ubuntu.ttf")
	TextEtImg.UpdateText("BitcoinPCT", "".join(PCTBTC) + "%", fontPath="Ubuntu.ttf")
	TextEtImg.UpdateText("EthereumPCT", "".join(PCTETH) + "%", fontPath="Ubuntu.ttf")

	TextEtImg.WriteAll(True)

	time.sleep(3)

	Repeat = Repeat + 1
	if Repeat == 6:
		Order = 1
		Ordre(Order)
	else:
		Crypto()

def Meteo():
	ReponseMeteo = rq.get("https://api.openweathermap.org/data/2.5/weather?q=Champigny-sur-Marne,fr&units=metric&lang=fr&appid=b3e6135efddd4b5f7ebc6add6fb003f3")

	TextEtImg


Ecran = Papirus()
TextEtImg = PapirusComposite(False)

TextEtImg.Clear()

Ordre(Order)


