# -*- encoding: utf-8 -*-

import time, json, configparser, requests
import Services as SV

def Crypto(conf, TextPAPIRUS): #Fonction Crypto (CryproCompare)
	SV.SVCrypto(conf)

	PCTC1 = list(str(SV.DataCrypto["RAW"][conf["CRYPTO"]["Coin1"]][conf["CRYPTO"]["Currency"]]["CHANGEPCT24HOUR"]))
	del PCTC1[-14:-1]
	PCTC2 = list(str(SV.DataCrypto["RAW"][conf["CRYPTO"]["Coin2"]][conf["CRYPTO"]["Currency"]]["CHANGEPCT24HOUR"]))
	del PCTC2[-14:-1]

	TextPAPIRUS.AddText("Crypto:", 10, 10, size = 20, fontPath="Ubuntu.ttf")
	TextPAPIRUS.AddText(conf["CRYPTO"]["Coin1"] + ": " + conf["CRYPTO"]["Currency"] + " " + str(SV.DataCrypto["RAW"][conf["CRYPTO"]["Coin1"]][conf["CRYPTO"]["Currency"]]["PRICE"]), 10, 44, size = 25, fontPath="Ubuntu.ttf")
	TextPAPIRUS.AddText(conf["CRYPTO"]["Coin2"] + ": " + conf["CRYPTO"]["Currency"] + " " + str(SV.DataCrypto["RAW"][conf["CRYPTO"]["Coin2"]][conf["CRYPTO"]["Currency"]]["PRICE"]), 10, 114, size = 25, fontPath="Ubuntu.ttf")
	TextPAPIRUS.AddText("".join(PCTC1) + "%", 10, 74, size = 15, fontPath="Ubuntu.ttf")
	TextPAPIRUS.AddText("".join(PCTC2) + "%", 10, 144, size = 15, fontPath="Ubuntu.ttf")

	TextPAPIRUS.AddText(time.strftime("%H:%M", time.localtime()), 200, 10, size = 20, fontPath="Ubuntu.ttf")

	TextPAPIRUS.WriteAll(True)
	time.sleep(10)
	TextPAPIRUS.Clear()

def Meteo(conf, TextPAPIRUS, Units): #Fonction Météo (OpenWeatherMap)
	SV.SVMeteo(conf)

	TextPAPIRUS.AddText("Météo:", 10, 10, size = 20, fontPath="Ubuntu.ttf")
	TextPAPIRUS.AddText("Température: " + str(SV.DataMeteo["main"]["temp"]) + "°C", 10, 40, size = 25, fontPath="Ubuntu.ttf")
	TextPAPIRUS.AddText("Temp. Min: " + str(SV.DataMeteo["main"]["temp_min"]) + "°C" + " Temp. Max: " + str(SV.DataMeteo["main"]["temp_max"]) + Units, 10, 65, size = 12, fontPath="Ubuntu.ttf")
	TextPAPIRUS.AddText("Temps: " + SV.DataMeteo["weather"][0]["description"].capitalize(), 10, 85, size = 25, fontPath="Ubuntu.ttf") 

	TextPAPIRUS.AddText(time.strftime("%H:%M", time.localtime()), 200, 10, size = 20, fontPath="Ubuntu.ttf")

	TextPAPIRUS.WriteAll(True)
	time.sleep(10)
	TextPAPIRUS.Clear()

def Musique(conf, TextPAPIRUS): #Fonction Musique (Last.fm)
	SV.SVMusique(conf)

	TextPAPIRUS.AddText("Last.fm:", 10, 10, size = 20, fontPath="Ubuntu.ttf")

	try:
		if SV.DataLast["recenttracks"]["track"][0]["@attr"]["nowplaying"] == "true":
			TextPAPIRUS.AddText("Actuellement:", 10, 40, size = 25, fontPath="Ubuntu.ttf")
			TextPAPIRUS.AddText(SV.DataLast["recenttracks"]["track"][0]["artist"]["#text"] + " - " + SV.DataLast["recenttracks"]["track"][0]["name"], 10, 65, size = 15, fontPath="Ubuntu.ttf")
			TextPAPIRUS.AddText(SV.DataLast["recenttracks"]["track"][0]["album"]["#text"], 10, 95, size = 10, fontPath="Ubuntu.ttf")

			TextPAPIRUS.AddText("Précédent:", 10, 115, size = 25, fontPath="Ubuntu.ttf")
			TextPAPIRUS.AddText(SV.DataLast["recenttracks"]["track"][1]["artist"]["#text"] + " - " + SV.DataLast["recenttracks"]["track"][1]["name"], 10, 140, size = 15, fontPath="Ubuntu.ttf")
	except:
		TextPAPIRUS.AddText("Précédent:", 10, 40, size = 25, fontPath="Ubuntu.ttf")
		TextPAPIRUS.AddText(SV.DataLast["recenttracks"]["track"][0]["artist"]["#text"] + " - " + SV.DataLast["recenttracks"]["track"][0]["name"], 10, 65, size = 15, fontPath="Ubuntu.ttf")
		TextPAPIRUS.AddText(SV.DataLast["recenttracks"]["track"][0]["album"]["#text"], 10, 95, size = 10, fontPath="Ubuntu.ttf")
	finally:
		TextPAPIRUS.AddText(time.strftime("%H:%M", time.localtime()), 200, 10, size = 20, fontPath="Ubuntu.ttf")
		TextPAPIRUS.WriteAll(True)
		time.sleep(10)
		TextPAPIRUS.Clear()

def Twitch(conf, TextPAPIRUS): #Fonction Twitch
	SV.SVTwitch(conf)

	TextPAPIRUS.AddText("Twitch:", 10, 10, size = 20, fontPath="Ubuntu.ttf")

	try:
		if SV.DataSt1["data"][0]["type"] == "live":
			ReponseTwitchGameID = requests.get("https://api.twitch.tv/helix/games?id=" + SV.DataSt1["data"][0]["game_id"], headers={"Client-ID": conf["TWITCH"]["TwitchAPI"]})
			GameID = json.loads(ReponseTwitchGameID.text)
			TextPAPIRUS.AddText(conf["TWITCH"]["TwitchSt1"].capitalize() + ": ON", 10, 40, size = 20, fontPath="Ubuntu.ttf")
			TextPAPIRUS.AddText("Jeu: " + GameID["data"][0]["name"], 10, 60, size = 15, fontPath="Ubuntu.ttf")
			TextPAPIRUS.AddText("Titre: " + SV.DataSt1["data"][0]["title"], 10, 75, size = 10, fontPath="Ubuntu.ttf")
	except IndexError:
		TextPAPIRUS.AddText(conf["TWITCH"]["TwitchSt1"].capitalize() + ": OFF", 10, 40, size = 20, fontPath="Ubuntu.ttf")
		
	try:
		if SV.DataSt2["data"][0]["type"] == "live":
			ReponseTwitchGameID = requests.get("https://api.twitch.tv/helix/games?id=" + SV.DataSt2["data"][0]["game_id"], headers={"Client-ID": conf["TWITCH"]["TwitchAPI"]})
			GameID = json.loads(ReponseTwitchGameID.text)
			TextPAPIRUS.AddText(conf["TWITCH"]["TwitchSt2"].capitalize() + ": ON", 10, 95, size = 20, fontPath="Ubuntu.ttf")
			TextPAPIRUS.AddText("Jeu: " + GameID["data"][0]["name"], 10, 115, size = 15, fontPath="Ubuntu.ttf")
			TextPAPIRUS.AddText("Titre: " + SV.DataSt2["data"][0]["title"], 10, 130, size = 10, fontPath="Ubuntu.ttf")
	except IndexError:
		TextPAPIRUS.AddText(conf["TWITCH"]["TwitchSt2"].capitalize() + ": OFF", 10, 132, size = 20, fontPath="Ubuntu.ttf")
	finally:
		TextPAPIRUS.AddText(time.strftime("%H:%M", time.localtime()), 200, 10, size = 20, fontPath="Ubuntu.ttf")
		TextPAPIRUS.WriteAll(True)
		time.sleep(10)
		TextPAPIRUS.Clear()

def Twitter(conf, TextPAPIRUS, BearerAUTH): #Fonction Twitter
	SV.SVTwitter(conf, BearerAUTH)

	TextPAPIRUS.AddText("Twitter:", 10, 10, size = 20, fontPath="Ubuntu.ttf")

	TextPAPIRUS.AddText("Compte: " + SV.DataTwitter["name"], 10, 40, size = 20, fontPath="Ubuntu.ttf")
	TextPAPIRUS.AddText(str(SV.DataTwitter["followers_count"]) + " abonnés", 10, 65, size = 20, fontPath="Ubuntu.ttf")

	TextPAPIRUS.AddText("Dernier tweet:", 10, 85, size = 20, fontPath="Ubuntu.ttf")
	TextPAPIRUS.AddText(SV.DataTwitter["status"]["text"], 10, 105, size = 15, fontPath="Ubuntu.ttf")

	TextPAPIRUS.AddText(time.strftime("%H:%M", time.localtime()), 200, 10, size = 20, fontPath="Ubuntu.ttf")
	TextPAPIRUS.WriteAll(True)
	time.sleep(10)
	TextPAPIRUS.Clear()

def RATP(conf, TextPAPIRUS):
	SV.SVRATP(conf)

	TextPAPIRUS.AddText("RATP:", 10, 10, size = 20, fontPath="Ubuntu.ttf")

	TextPAPIRUS.AddText("Station: " + conf["RATP"]["stationA"] + " - " + conf["RATP"]["lineA"], 10, 40, size = 15, fontPath="Ubuntu.ttf")
	TextPAPIRUS.AddText("Prochain: " + SV.OutputA["result"]["schedules"][0]["message"], 10, 55, size = 15, fontPath="Ubuntu.ttf")
	TextPAPIRUS.AddText("Direction: " + SV.OutputA["result"]["schedules"][0]["destination"], 10, 70, size = 15, fontPath="Ubuntu.ttf")

	if conf["RATP"]["typetransB"] != "" and conf["RATP"]["lineB"] != "" and conf["RATP"]["stationB"] != "":
		TextPAPIRUS.AddText("Station: " + conf["RATP"]["stationB"] + " - " + conf["RATP"]["lineB"], 10, 115, size = 15, fontPath="Ubuntu.ttf")
		TextPAPIRUS.AddText("Prochain: " + SV.OutputB["result"]["schedules"][0]["message"], 10, 130, size = 15, fontPath="Ubuntu.ttf")
		TextPAPIRUS.AddText("Direction: " + SV.OutputB["result"]["schedules"][0]["destination"], 10, 145, size = 15, fontPath="Ubuntu.ttf")

	TextPAPIRUS.AddText(time.strftime("%H:%M", time.localtime()), 200, 10, size = 20, fontPath="Ubuntu.ttf")
	TextPAPIRUS.WriteAll(True)
	time.sleep(10)
	TextPAPIRUS.Clear()

#def All(conf, TextPAPIRUS, BearerAUTH):

