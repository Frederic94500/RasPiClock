# -*- encoding: utf-8 -*-

import time, configparser
import Services as SV

conf = configparser.ConfigParser()
conf.read("config.cfg")

def Crypto(conf, TextPAPIRUS): #Fonction Crypto (CryproCompare)
	TextPAPIRUS.AddText("Crypto:", 10, 10, size = 20, fontPath="Ubuntu.ttf")

	i = 1
	ReponseCrypto = SV.SVCrypto(conf, "coin" + str(i))
	PCT = list(str(ReponseCrypto.json()["RAW"][conf["CRYPTO"]["coin" + str(i)]][conf["CRYPTO"]["Currency"]]["CHANGEPCT24HOUR"]))
	del PCT[-14:-1]
	TextPAPIRUS.AddText(conf["CRYPTO"]["coin" + str(i)] + ": " + conf["CRYPTO"]["Currency"] + " " + str(ReponseCrypto.json()["RAW"][conf["CRYPTO"]["coin" + str(i)]][conf["CRYPTO"]["Currency"]]["PRICE"]), 10, 44, size = 25, fontPath="Ubuntu.ttf")
	TextPAPIRUS.AddText("".join(PCT) + "%", 10, 74, size = 15, fontPath="Ubuntu.ttf")

	i += 1
	ReponseCrypto = SV.SVCrypto(conf, "coin" + str(i))
	PCT = list(str(ReponseCrypto.json()["RAW"][conf["CRYPTO"]["coin" + str(i)]][conf["CRYPTO"]["Currency"]]["CHANGEPCT24HOUR"]))
	del PCT[-14:-1]
	TextPAPIRUS.AddText(conf["CRYPTO"]["coin" + str(i)] + ": " + conf["CRYPTO"]["Currency"] + " " + str(ReponseCrypto.json()["RAW"][conf["CRYPTO"]["coin" + str(i)]][conf["CRYPTO"]["Currency"]]["PRICE"]), 10, 114, size = 25, fontPath="Ubuntu.ttf")
	TextPAPIRUS.AddText("".join(PCT) + "%", 10, 144, size = 15, fontPath="Ubuntu.ttf")

	TextPAPIRUS.AddText(time.strftime("%H:%M", time.localtime()), 200, 10, size = 20, fontPath="Ubuntu.ttf")

	TextPAPIRUS.WriteAll(True)
	time.sleep(10)
	TextPAPIRUS.Clear()
