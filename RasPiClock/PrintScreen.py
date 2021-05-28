# -*- encoding: utf-8 -*-

import time
import Request as RQ

def crypto(conf, textPAPIRUS): #Fonction Crypto (Binance)
	textPAPIRUS.AddText("Crypto:", 10, 10, size = 20, fontPath="Ubuntu.ttf")

	x = 10
	y = 45

	for i in range(2):
		reponseCrypto = RQ.crypto(conf, "pair" + str(i+1))
		textPAPIRUS.AddText(reponseCrypto.json()["symbol"] + ": " + f'{float(reponseCrypto.json()["lastPrice"]):.2f}', x, y, size = 25, fontPath="Ubuntu.ttf", Id="pair" + str(i+1))
		textPAPIRUS.AddText(reponseCrypto.json()["priceChangePercent"] + "%", x, y+25+5, size = 15, fontPath="Ubuntu.ttf", Id="pairpct" + str(i+1))
		y = y+25+5+15+25

	textPAPIRUS.AddText(time.strftime("%H:%M:%S", time.localtime()), 180, 10, size = 20, fontPath="Ubuntu.ttf", Id="time")

	textPAPIRUS.WriteAll(True)

def cryptoUpdate(conf, textPAPIRUS): #Fonction Crypto (Binance)
	for i in range(2):
		reponseCrypto = RQ.crypto(conf, "pair" + str(i+1))
		textPAPIRUS.UpdateText("pair" + str(i+1), reponseCrypto.json()["symbol"] + ": " + f'{float(reponseCrypto.json()["lastPrice"]):.2f}', fontPath="Ubuntu.ttf")
		textPAPIRUS.UpdateText("pairpct" + str(i+1), reponseCrypto.json()["priceChangePercent"] + "%", fontPath="Ubuntu.ttf")

	textPAPIRUS.UpdateText("time", time.strftime("%H:%M:%S", time.localtime()), fontPath="Ubuntu.ttf")

	textPAPIRUS.WriteAll(True)
