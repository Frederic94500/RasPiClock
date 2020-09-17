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

def Meteo(conf, TextPAPIRUS, Units): #Fonction Météo (OpenWeatherMap) + Home Assistant pour température intérieur
	ReponseMeteo = SV.SVMeteo(conf)

	TextPAPIRUS.AddText("Météo:", 10, 10, size = 20, fontPath="Ubuntu.ttf")
	TextPAPIRUS.AddText("Température: " + str(ReponseMeteo.json()["main"]["temp"]) + Units, 10, 40, size = 25, fontPath="Ubuntu.ttf")
	TextPAPIRUS.AddText("Temp. Min: " + str(ReponseMeteo.json()["main"]["temp_min"]) + Units + " Temp. Max: " + str(ReponseMeteo.json()["main"]["temp_max"]) + Units, 10, 65, size = 12, fontPath="Ubuntu.ttf")
	TextPAPIRUS.AddText("Temps: " + ReponseMeteo.json()["weather"][0]["description"].capitalize(), 10, 85, size = 25, fontPath="Ubuntu.ttf") 

	if conf["HA"]["token"] != "":
		ReponseHA = SV.SVHA(conf)
		TextPAPIRUS.AddText("Temp. intérieur" + ReponseHA.json()["state"] + Units, 10, 110, size = 20, fontPath="Ubuntu.ttf")

	TextPAPIRUS.AddText(time.strftime("%H:%M", time.localtime()), 200, 10, size = 20, fontPath="Ubuntu.ttf")
	TextPAPIRUS.WriteAll(True)
	time.sleep(10)
	TextPAPIRUS.Clear()

def Musique(conf, TextPAPIRUS): #Fonction Musique (Last.fm)
	ReponseLastFM = SV.SVMusique(conf)

	TextPAPIRUS.AddText("Last.fm:", 10, 10, size = 20, fontPath="Ubuntu.ttf")

	try:
		if ReponseLastFM.json()["recenttracks"]["track"][0]["@attr"]["nowplaying"] == "true":
			TextPAPIRUS.AddText("Actuellement:", 10, 40, size = 25, fontPath="Ubuntu.ttf")
			TextPAPIRUS.AddText(ReponseLastFM.json()["recenttracks"]["track"][0]["artist"]["#text"] + " - " + ReponseLastFM.json()["recenttracks"]["track"][0]["name"], 10, 65, size = 15, fontPath="Ubuntu.ttf")
			TextPAPIRUS.AddText(ReponseLastFM.json()["recenttracks"]["track"][0]["album"]["#text"], 10, 95, size = 10, fontPath="Ubuntu.ttf")

			TextPAPIRUS.AddText("Précédent:", 10, 115, size = 25, fontPath="Ubuntu.ttf")
			TextPAPIRUS.AddText(ReponseLastFM.json()["recenttracks"]["track"][1]["artist"]["#text"] + " - " + ReponseLastFM.json()["recenttracks"]["track"][1]["name"], 10, 140, size = 15, fontPath="Ubuntu.ttf")
	except:
		TextPAPIRUS.AddText("Précédent:", 10, 40, size = 25, fontPath="Ubuntu.ttf")
		TextPAPIRUS.AddText(ReponseLastFM.json()["recenttracks"]["track"][0]["artist"]["#text"] + " - " + ReponseLastFM.json()["recenttracks"]["track"][0]["name"], 10, 65, size = 15, fontPath="Ubuntu.ttf")
		TextPAPIRUS.AddText(ReponseLastFM.json()["recenttracks"]["track"][0]["album"]["#text"], 10, 95, size = 10, fontPath="Ubuntu.ttf")
	finally:
		TextPAPIRUS.AddText(time.strftime("%H:%M", time.localtime()), 200, 10, size = 20, fontPath="Ubuntu.ttf")
		TextPAPIRUS.WriteAll(True)
		time.sleep(10)
		TextPAPIRUS.Clear()

def Twitch(conf, TextPAPIRUS): #Fonction Twitch
	TextPAPIRUS.AddText("Twitch:", 10, 10, size = 20, fontPath="Ubuntu.ttf")

	i = 1
	ReponseID = SV.SVTwitchGetID(conf, "TwitchSt" + str(i))
	ReponseTwitchSt = SV.SVTwitchGetStatus(conf, ReponseID)
	try:
		if ReponseTwitchSt.json()["stream"]["broadcast_platform"] == "live":
			TextPAPIRUS.AddText(ReponseTwitchSt.json()["stream"]["channel"]["display_name"] + ": ON", 10, 40, size = 20, fontPath="Ubuntu.ttf")
			TextPAPIRUS.AddText("Jeu: " + ReponseTwitchSt.json()["stream"]["game"], 10, 60, size = 15, fontPath="Ubuntu.ttf")
			TextPAPIRUS.AddText("Titre: " + ReponseTwitchSt.json()["stream"]["channel"]["status"], 10, 75, size = 10, fontPath="Ubuntu.ttf")
	except: TextPAPIRUS.AddText(conf["TWITCH"]["TwitchSt" + str(i)].capitalize() + ": OFF", 10, 40, size = 20, fontPath="Ubuntu.ttf")

	i += 1
	ReponseID = SV.SVTwitchGetID(conf, "TwitchSt" + str(i))
	ReponseTwitchSt = SV.SVTwitchGetStatus(conf, ReponseID)
	try:
		if ReponseTwitchSt.json()["stream"]["broadcast_platform"] == "live":
			TextPAPIRUS.AddText(ReponseTwitchSt.json()["stream"]["channel"]["display_name"] + ": ON", 10, 95, size = 20, fontPath="Ubuntu.ttf")
			TextPAPIRUS.AddText("Jeu: " + ReponseTwitchSt.json()["stream"]["game"], 10, 115, size = 15, fontPath="Ubuntu.ttf")
			TextPAPIRUS.AddText("Titre: " + ReponseTwitchSt.json()["stream"]["channel"]["status"], 10, 130, size = 10, fontPath="Ubuntu.ttf")
	except: TextPAPIRUS.AddText(conf["TWITCH"]["TwitchSt" + str(i)].capitalize() + ": OFF", 10, 95, size = 20, fontPath="Ubuntu.ttf")
	
	TextPAPIRUS.AddText(time.strftime("%H:%M", time.localtime()), 200, 10, size = 20, fontPath="Ubuntu.ttf")
	TextPAPIRUS.WriteAll(True)
	time.sleep(10)
	TextPAPIRUS.Clear()

def Twitter(conf, TextPAPIRUS, BearerAUTH): #Fonction Twitter
	ReponseTwitter = SV.SVTwitter(conf, BearerAUTH)

	TextPAPIRUS.AddText("Twitter:", 10, 10, size = 20, fontPath="Ubuntu.ttf")

	TextPAPIRUS.AddText("Compte: " + ReponseTwitter.json()["name"], 10, 40, size = 20, fontPath="Ubuntu.ttf")
	TextPAPIRUS.AddText(str(ReponseTwitter.json()["followers_count"]) + " abonnés", 10, 65, size = 20, fontPath="Ubuntu.ttf")

	TextPAPIRUS.AddText("Dernier tweet:", 10, 85, size = 20, fontPath="Ubuntu.ttf")
	TextPAPIRUS.AddText(ReponseTwitter.json()["status"]["text"], 10, 105, size = 15, fontPath="Ubuntu.ttf")

	TextPAPIRUS.AddText(time.strftime("%H:%M", time.localtime()), 200, 10, size = 20, fontPath="Ubuntu.ttf")
	TextPAPIRUS.WriteAll(True)
	time.sleep(10)
	TextPAPIRUS.Clear()

def RATP(conf, TextPAPIRUS):
	TextPAPIRUS.AddText("RATP:", 10, 10, size = 20, fontPath="Ubuntu.ttf")
	i = 1
	ReponseRATP = SV.SVRATP(conf, "typetrans" + str(i), "line" + str(i), "station" + str(i), "sens" + str(i))
	TextPAPIRUS.AddText("Station: " + conf["RATP"]["station" + str(i)] + " - " + conf["RATP"]["line" + str(i)], 10, 40, size = 15, fontPath="Ubuntu.ttf")
	TextPAPIRUS.AddText("Prochain: " + ReponseRATP.json()["result"]["schedules"][0]["message"], 10, 55, size = 15, fontPath="Ubuntu.ttf")
	TextPAPIRUS.AddText("Direction: " + ReponseRATP.json()["result"]["schedules"][0]["destination"], 10, 70, size = 15, fontPath="Ubuntu.ttf")

	if conf["RATP"]["typetrans2"] != "" and conf["RATP"]["line2"] != "" and conf["RATP"]["station2"] != "" and conf["RATP"]["sens2"] != "":
		i += 1
		ReponseRATP = SV.SVRATP(conf, "typetrans" + str(i), "line" + str(i), "station" + str(i), "sens" + str(i))
		TextPAPIRUS.AddText("Station: " + conf["RATP"]["station" + str(i)] + " - " + conf["RATP"]["line" + str(i)], 10, 115, size = 15, fontPath="Ubuntu.ttf")
		TextPAPIRUS.AddText("Prochain: " + ReponseRATP.json()["result"]["schedules"][0]["message"], 10, 130, size = 15, fontPath="Ubuntu.ttf")
		TextPAPIRUS.AddText("Direction: " + ReponseRATP.json()["result"]["schedules"][0]["destination"], 10, 145, size = 15, fontPath="Ubuntu.ttf")

	TextPAPIRUS.AddText(time.strftime("%H:%M", time.localtime()), 200, 10, size = 20, fontPath="Ubuntu.ttf")
	TextPAPIRUS.WriteAll(True)
	time.sleep(10)
	TextPAPIRUS.Clear()

def AllInit(conf, TextPAPIRUS, BearerAUTH):
	TextPAPIRUS.AddText(time.strftime("%H:%M", time.localtime()), 200, 10, size = 20, fontPath="Ubuntu.ttf")
	
	i = 1

	ReponseCrypto = SV.SVCrypto(conf, "coin" + str(i))
	TextTextPAPIRUS.AddText("Crypto:", 10, 10, size = 15, fontPath="Ubuntu.ttf")

	PCT = list(str(SV.DataCrypto["RAW"][conf["CRYPTO"]["Coin1"]][conf["CRYPTO"]["Currency"]]["CHANGEPCT24HOUR"]))
	del PCT[-14:-1]
	PCT = list(str(SV.DataCrypto["RAW"][conf["CRYPTO"]["Coin2"]][conf["CRYPTO"]["Currency"]]["CHANGEPCT24HOUR"]))
	del PCT[-14:-1]

	TextPAPIRUS.AddText(conf["CRYPTO"]["Coin1"] + ": " + conf["CRYPTO"]["Currency"] + " " + str(SV.DataCrypto["RAW"][conf["CRYPTO"]["Coin1"]][conf["CRYPTO"]["Currency"]]["PRICE"]), 10, 25, size = 15, fontPath="Ubuntu.ttf", Id="Coin1P")
	TextPAPIRUS.AddText(conf["CRYPTO"]["Coin2"] + ": " + conf["CRYPTO"]["Currency"] + " " + str(SV.DataCrypto["RAW"][conf["CRYPTO"]["Coin2"]][conf["CRYPTO"]["Currency"]]["PRICE"]), 100, 25, size = 15, fontPath="Ubuntu.ttf", Id="Coin2P")
	TextPAPIRUS.AddText("".join(PCTC1) + "%", 10, 40, size = 10, fontPath="Ubuntu.ttf", Id="Coin1PCT")
	TextPAPIRUS.AddText("".join(PCTC2) + "%", 100, 40, size = 10, fontPath="Ubuntu.ttf", Id="Coin2PCT")


	SV.SVMeteo(conf)
	TextPAPIRUS.AddText("Météo:", 10, 10, size = 20, fontPath="Ubuntu.ttf")
	TextPAPIRUS.AddText("Température: " + str(SV.DataMeteo["main"]["temp"]) + "°C", 10, 40, size = 25, fontPath="Ubuntu.ttf", Id="Deg")
	TextPAPIRUS.AddText("Temps: " + SV.DataMeteo["weather"][0]["description"].capitalize(), 10, 85, size = 25, fontPath="Ubuntu.ttf", Id="Temps") 

	SV.SVMusique(conf)

	ReponseID = SV.SVTwitchGetID(conf, "TwitchSt" + str(i))
	ReponseTwitchSt = SV.SVTwitchGetStatus(conf, ReponseID)


