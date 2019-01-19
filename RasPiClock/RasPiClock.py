import requests as rq
import time
import json

from papirus import Papirus
from papirus import PapirusComposite

'''def Ordre(Order):
	if Order == 0: Crypto()'''

def Crypto():
	ReponseCrypto = rq.get("https://min-api.cryptocompare.com/data/pricemulti?fsyms=BTC,ETH&tsyms=USD&api_key=261d6b25933c3a0ccd3b991898b6ed86ac7815ec7ebedda674dd7ff116f23e51")
	DataCrypto = json.loads(ReponseCrypto.text)

	ResultBTC = DataCrypto["BTC"]
	PriceBTC = str(ResultBTC["USD"])

	ResultETH = DataCrypto["ETH"]
	PriceETH = str(ResultETH["USD"])

	TextEtImg.UpdateText("Bitcoin", "$ " + PriceBTC)
	TextEtImg.AddImg("BTC.bmp", 10, 22, (44,44))

	TextEtImg.UpdateText("Ethereum", "$ " + PriceETH)
	TextEtImg.AddImg("ETH.bmp", 10, 110, (44,68))

	TextEtImg.WriteAll()
	Ecran.fast_update()

	#print("$" + "".join(price) + " | TX Unconfirmed: " + str(result["unconfirmed_txs"]))
	#Order = 0
	time.sleep(30)
	Crypto()

Ecran = Papirus()
TextEtImg = PapirusComposite(False)

TextEtImg.AddText("$ BTC", 64, 24, Id="Bitcoin", fontPath="Ubuntu.ttf" , size = 30)
TextEtImg.AddText("$ ETH", 64, 110, Id="Ethereum", fontPath="Ubuntu.ttf" , size = 30)

Crypto()


