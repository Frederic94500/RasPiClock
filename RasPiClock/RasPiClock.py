import requests as rq
import time
import json

def Ordre(Order):
	if Order == 0: Crypto()

def Crypto():
	RC = rq.get("https://chain.so/api/v2/get_info/ticker_BTC_USD")
	text = json.loads(RC.text)
	result = text["data"]
	price = list(str(result["price"]))
	del price[-7:-1]
	print("$" + "".join(price) + " | TX Unconfirmed: " + str(result["unconfirmed_txs"]))
	Order = 0
	time.sleep(30)
	Ordre(Order)

prix()


