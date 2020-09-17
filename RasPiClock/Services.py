# -*- encoding: utf-8 -*-

import configparser, requests, base64

def SVCrypto(conf, coin):
	ReponseCrypto = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=" + conf["CRYPTO"][coin] + "&tsyms=" + conf["CRYPTO"]["Currency"] + "&api_key=" + conf["CRYPTO"]["CryptoAPI"])
	return ReponseCrypto

def SVMeteo(conf):
	ReponseMeteo = requests.get("https://api.openweathermap.org/data/2.5/weather?q=" + conf["WEATHER"]["City"] + "&units=" + conf["WEATHER"]["Units"] + "&lang=" + conf["WEATHER"]["Lang"] + "&appid=" + conf["WEATHER"]["MeteoAPI"])
	return ReponseMeteo
def SVHA(conf):
	ReponseHA = requests.get("http://" + conf["HA"]["ip"] + ":" + conf["HA"]["port"] + "/api/states/" + conf["HA"]["entityid"] , headers={"content-type": "application/json", "Authorization": "Bearer " + conf["HA"]["token"]})
	return ReponseHA

def SVMusique(conf):
	ReponseLastFM = requests.get("http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=" + conf["LASTFM"]["UserFM"] + "&limit=1&format=json&api_key=" + conf["LASTFM"]["LastFmAPI"])
	return ReponseLastFM

def SVTwitchGetID(conf, TwitchSt):
	ReponseID = requests.get("https://api.twitch.tv/kraken/users?login=" + conf["TWITCH"][TwitchSt], headers={"Accept": "application/vnd.twitchtv.v5+json" ,"Client-ID": conf["TWITCH"]["twitchapiclientid"]})
	return ReponseID
def SVTwitchGetStatus(conf, ReponseID):
	ReponseTwitchSt = requests.get("https://api.twitch.tv/kraken/streams/" + ReponseID.json()["users"][0]["_id"], headers={"Accept": "application/vnd.twitchtv.v5+json" ,"Client-ID": conf["TWITCH"]["twitchapiclientid"]})
	return ReponseTwitchSt

def SVTwitterGetToken(conf):
	key_secret = '{}:{}'.format(conf["TWITTER"]["twitterapi"], conf["TWITTER"]["twitterapisecret"]).encode('ascii')
	b64_encoded_key = base64.b64encode(key_secret)
	b64_encoded_key = b64_encoded_key.decode('ascii')
	BearerRAW = requests.post('https://api.twitter.com/oauth2/token', headers={'Authorization': 'Basic {}'.format(b64_encoded_key), 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}, data={'grant_type': 'client_credentials'})
	return BearerRAW
def SVTwitter(conf, BearerAUTH):
	ReponseTwitter = requests.get("https://api.twitter.com/1.1/users/show.json?screen_name=" + conf["TWITTER"]["UserTW"], headers={'Authorization': "Bearer " + BearerAUTH})
	return ReponseTwitter

def SVRATP(conf, typetrans, line, station, sens):
	ReponseRATP = requests.get("https://api-ratp.pierre-grimaud.fr/v4/schedules/" + conf["RATP"][typetrans] + "/" + conf["RATP"][line] + "/" + conf["RATP"][station] + "/" + conf["RATP"][sens])
	return ReponseRATP


