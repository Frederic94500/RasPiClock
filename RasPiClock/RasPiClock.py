import requests as rq
import time
import json

from papirus import Papirus
from papirus import PapirusComposite

Creation = 0

def Ordre(Order):
	TextEtImg.Clear()
	if Order == 0: Crypto()
	if Order == 1: Meteo() #WIP
	if Order == 2: Musique() #WIP
	if Order == 3: RATP() #WIP

def Crypto():
	global Creation

	if Creation == 0:
		TextEtImg.AddImg("BTC.bmp", 10, 42, (44,44))
		TextEtImg.AddImg("ETH.bmp", 10, 100, (44,68))
		TextEtImg.AddText("Crypto:", 10, 10, size = 20, fontPath="Ubuntu.ttf")
		TextEtImg.AddText("$ BTC", 64, 44, Id="BitcoinP", size = 30)
		TextEtImg.AddText("$ ETH", 64, 114, Id="EthereumP", size = 30)
		TextEtImg.AddText("% BTC", 64, 74, Id="BitcoinPCT", size = 15)
		TextEtImg.AddText("% ETH", 64, 174, Id="EthereumPCT", size = 15)
		Creation = 1

	ReponseCrypto = rq.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH&tsyms=USD&api_key=261d6b25933c3a0ccd3b991898b6ed86ac7815ec7ebedda674dd7ff116f23e51")
	DataCryptoRAW = json.loads(ReponseCrypto.text)
	DataCrypto = DataCryptoRAW["RAW"]

	ResultBTC = DataCrypto["BTC"]
	BTC = ResultBTC["USD"]
	PriceBTC = str(BTC["PRICE"])
	PCTBTC = list(str(BTC["CHANGEPCT24HOUR"]))
	del PCTBTC[-14:-1]

	ResultETH = DataCrypto["ETH"]
	ETH = ResultETH["USD"]
	PriceETH = str(ETH["PRICE"])
	PCTETH = list(str(ETH["CHANGEPCT24HOUR"]))
	del PCTETH[-14:-1]

	TextEtImg.UpdateText("BitcoinP", "$ " + PriceBTC, fontPath="Ubuntu.ttf")
	TextEtImg.UpdateText("EthereumP", "$ " + PriceETH, fontPath="Ubuntu.ttf")

	TextEtImg.UpdateText("BitcoinPCT", "".join(PCTBTC) + "%", fontPath="Ubuntu.ttf")
	TextEtImg.UpdateText("EthereumPCT", "".join(PCTBTC) + "%", fontPath="Ubuntu.ttf")

	TextEtImg.WriteAll(True)
	time.sleep(3)
	Crypto()

def Meteo():
	ReponseMeteo = rq.get("https://api.openweathermap.org/data/2.5/weather?q=Champigny-sur-Marne,fr&units=metric&lang=fr&appid=b3e6135efddd4b5f7ebc6add6fb003f3")

	TextEtImg


Ecran = Papirus()
TextEtImg = PapirusComposite(False)

TextEtImg.Clear()


Crypto()


