# -*- encoding: utf-8 -*-

import json, configparser, requests

def SVCrypto(conf):
	global DataCrypto
	ReponseCrypto = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=" + conf["CRYPTO"]["Coin1"] + "," + conf["CRYPTO"]["Coin2"] + "&tsyms=" + conf["CRYPTO"]["Currency"] + "&api_key=" + conf["CRYPTO"]["CryptoAPI"])
	DataCrypto = json.loads(ReponseCrypto.text)

def SVMeteo(conf):
	global DataMeteo
	ReponseMeteo = requests.get("https://api.openweathermap.org/data/2.5/weather?q=" + conf["WEATHER"]["City"] + "&units=" + conf["WEATHER"]["Units"] + "&lang=" + conf["WEATHER"]["Lang"] + "&appid=" + conf["WEATHER"]["MeteoAPI"])
	DataMeteo = json.loads(ReponseMeteo.text)

def SVMusique(conf):
	global DataLast
	ReponseLastFM = requests.get("http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=" + conf["LASTFM"]["UserFM"] + "&limit=1&format=json&api_key=" + conf["LASTFM"]["LastFmAPI"])
	DataLast = json.loads(ReponseLastFM.text)

def SVTwitch(conf, TwitchSt):
	ReponseTwitchSt = requests.get("https://api.twitch.tv/helix/streams?user_login=" + conf["TWITCH"][TwitchSt], headers={"Client-ID": conf["TWITCH"]["TwitchAPI"]})
	DataSt = json.loads(ReponseTwitchSt.text)
	return DataSt

def SVTwitchGame(conf, DataSt):
	ReponseTwitchGameID = requests.get("https://api.twitch.tv/helix/games?id=" + DataSt["data"][0]["game_id"], headers={"Client-ID": conf["TWITCH"]["TwitchAPI"]})
	GameID = json.loads(ReponseTwitchGameID.text)
	return GameID

def SVTwitter(conf, BearerAUTH):
	global DataTwitter
	ReponseTwitter = requests.get("https://api.twitter.com/1.1/users/show.json?screen_name=" + conf["TWITTER"]["UserTW"], headers={'Authorization': "Bearer " + BearerAUTH})
	DataTwitter = json.loads(ReponseTwitter.text)

def SVRATP(conf):
	global OutputA
	global OutputB
	ReponseRATPA = requests.get("https://api-ratp.pierre-grimaud.fr/v4/schedules/" + conf["RATP"]["typetransA"] + "/" + conf["RATP"]["lineA"] + "/" + conf["RATP"]["stationA"] + "/A")
	ReponseRATPB = requests.get("https://api-ratp.pierre-grimaud.fr/v4/schedules/" + conf["RATP"]["typetransB"] + "/" + conf["RATP"]["lineB"] + "/" + conf["RATP"]["stationB"] + "/R")
	OutputA = json.loads(ReponseRATPA.text)
	OutputB = json.loads(ReponseRATPB.text)

