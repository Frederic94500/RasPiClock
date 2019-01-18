import requests as rq
import time
import json

from papirus import Papirus
from papirus import PapirusComposite

def Ordre(Order):
	if Order == 0: Crypto()

def Crypto():
	RC = rq.get("https://chain.so/api/v2/get_info/ticker_BTC_USD")
	data = json.loads(RC.text)
	result = data["data"]
	price = list(str(result["price"]))
	del price[-7:-1]

	TextEtImg.UpdateText("Bitcoin", "$ " + "".join(price))
	TextEtImg.AddImg("BTC.bmp", 10, 22, (44,44))
	TextEtImg.WriteAll()
	Ecran.partial_update()

	#print("$" + "".join(price) + " | TX Unconfirmed: " + str(result["unconfirmed_txs"]))
	Order = 0
	time.sleep(30)
	Ordre(Order)

Ecran = Papirus()
TextEtImg = PapirusComposite(False)

TextEtImg.AddText("$ BTC", 64, 22, Id="Bitcoin", fontPath="Ubuntu.ttf" , size = 44)

Crypto()


