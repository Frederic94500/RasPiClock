import requests as rq
import time
import json

from papirus import Papirus
from papirus import PapirusComposite

'''def Ordre(Order):
	if Order == 0: Crypto()'''

def Crypto():
	ReponseBTC = rq.get("https://chain.so/api/v2/get_info/ticker_BTC_USD")
	DataBTC = json.loads(ReponseBTC.text)
	ResultBTC = DataBTC["data"]
	PriceBTC = list(str(ResultBTC["price"]))
	del PriceBTC[-7:-1]

	ReponseETH = rq.get("https://chain.so/api/v2/get_info/ticker_ETH_USD")
	DataETH = json.loads(ReponseETH.text)
	ResultETH = DataETH["data"]
	PriceETH = list(str(ResultETH["price"]))
	del PriceETH[-7:-1]

	TextEtImg.UpdateText("Bitcoin", "$ " + "".join(PriceBTC))
	TextEtImg.AddImg("BTC.bmp", 10, 22, (44,44))

	TextEtImg.UpdateText("Ethereum", "$ " + "".join(PriceETH))
	TextEtImg.AddImg("ETH.bmp", 10, 110, (44,68))

	TextEtImg.WriteAll()
	Ecran.partial_update()

	#print("$" + "".join(price) + " | TX Unconfirmed: " + str(result["unconfirmed_txs"]))
	#Order = 0
	time.sleep(30)
	Crypto()

Ecran = Papirus()
TextEtImg = PapirusComposite(False)

TextEtImg.AddText("$ BTC", 64, 24, Id="Bitcoin", fontPath="Ubuntu.ttf" , size = 40)
TextEtImg.AddText("$ ETH", 64, 110, Id="Ethereum", fontPath="Ubuntu.ttf" , size = 40)

Crypto()


