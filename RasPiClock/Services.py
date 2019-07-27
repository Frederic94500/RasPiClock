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

def SVTwitch(conf):
	global DataSt1
	global DataSt2
	ReponseTwitchSt1 = requests.get("https://api.twitch.tv/helix/streams?user_login=" + conf["TWITCH"]["TwitchSt1"], headers={"Client-ID": conf["TWITCH"]["TwitchAPI"]})
	ReponseTwitchSt2 = requests.get("https://api.twitch.tv/helix/streams?user_login=" + conf["TWITCH"]["TwitchSt2"], headers={"Client-ID": conf["TWITCH"]["TwitchAPI"]})
	DataSt1 = json.loads(ReponseTwitchSt1.text)
	DataSt2 = json.loads(ReponseTwitchSt2.text)

def SVTwitter(conf, BearerAUTH):
	global DataTwitter
	ReponseTwitter = requests.get("https://api.twitter.com/1.1/users/show.json?screen_name=" + conf["TWITTER"]["UserTW"], headers={'Authorization': "Bearer " + BearerAUTH})
	DataTwitter = json.loads(ReponseTwitter.text)

def SVRATP(conf):
	global OutputA
	global OutputB
	ReponseRATPA = requests.get("https://api-ratp.pierre-grimaud.fr/v4/schedules/" + conf[RATP][typetrans] + "/" + conf[RATP][line] + "/" + conf[RATP][station] + "/A")
	ReponseRATPB = requests.get("https://api-ratp.pierre-grimaud.fr/v4/schedules/" + conf[RATP][typetrans] + "/" + conf[RATP][line] + "/" + conf[RATP][station] + "/B")
	OutputA = json.loads(ReponseRATPA.text)
	OutputB = json.loads(ReponseRATPB.text)

