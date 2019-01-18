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

	TextEtImg.AddText("$ " + "".join(price), 64, 88, fontPath="Ubuntu.ttf")
	TextEtImg.AddImg("BTC.bmp", 10, 66, (44,44))
	TextEtImg.WriteAll()
	Ecran.partial_update()

	#print("$" + "".join(price) + " | TX Unconfirmed: " + str(result["unconfirmed_txs"]))
	Order = 0
	time.sleep(30)
	Ordre(Order)

Ecran = Papirus()
TextEtImg = PapirusComposite()

Crypto()


