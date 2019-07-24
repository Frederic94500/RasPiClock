def Crypto(): #Fonction Crypto (CryproCompare)
	TextPAPIRUS.AddText("Crypto:", 10, 10, size = 20, fontPath="Ubuntu.ttf")

	ReponseCrypto = rq.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=" + conf["CRYPTO"]["Coin1"] + "," + conf["CRYPTO"]["Coin2"] + "&tsyms=" + conf["CRYPTO"]["Currency"] + "&api_key=" + conf["CRYPTO"]["CryptoAPI"])
	DataCrypto = json.loads(ReponseCrypto.text)

	PCTC1 = list(str(DataCrypto["RAW"][conf["CRYPTO"]["Coin1"]][conf["CRYPTO"]["Currency"]]["CHANGEPCT24HOUR"]))
	del PCTC1[-14:-1]
	PCTC2 = list(str(DataCrypto["RAW"][conf["CRYPTO"]["Coin2"]][conf["CRYPTO"]["Currency"]]["CHANGEPCT24HOUR"]))
	del PCTC2[-14:-1]

	TextPAPIRUS.AddText(conf["CRYPTO"]["Coin1"] + ": " + conf["CRYPTO"]["Currency"] + " " + str(DataCrypto["RAW"][conf["CRYPTO"]["Coin1"]][conf["CRYPTO"]["Currency"]]["PRICE"]), 10, 44, size = 25, fontPath="Ubuntu.ttf")
	TextPAPIRUS.AddText(conf["CRYPTO"]["Coin2"] + ": " + conf["CRYPTO"]["Currency"] + " " + str(DataCrypto["RAW"][conf["CRYPTO"]["Coin2"]][conf["CRYPTO"]["Currency"]]["PRICE"]), 10, 114, size = 25, fontPath="Ubuntu.ttf")
	TextPAPIRUS.AddText("".join(PCTC1) + "%", 10, 74, size = 15, fontPath="Ubuntu.ttf")
	TextPAPIRUS.AddText("".join(PCTC2) + "%", 10, 144, size = 15, fontPath="Ubuntu.ttf")

	TextPAPIRUS.AddText(time.strftime("%H:%M", time.localtime()), 200, 10, size = 20, fontPath="Ubuntu.ttf")

	TextPAPIRUS.WriteAll(True)
	time.sleep(10)
	TextPAPIRUS.Clear()

def Meteo(): #Fonction Météo (OpenWeatherMap)
	global Units
	ReponseMeteo = rq.get("https://api.openweathermap.org/data/2.5/weather?q=" + conf["WEATHER"]["City"] + "&units=" + conf["WEATHER"]["Units"] + "&lang=" + conf["WEATHER"]["Lang"] + "&appid=" + conf["WEATHER"]["MeteoAPI"])
	DataMeteo = json.loads(ReponseMeteo.text)

	TextPAPIRUS.AddText("Météo:", 10, 10, size = 20, fontPath="Ubuntu.ttf")
	TextPAPIRUS.AddText("Température: " + str(DataMeteo["main"]["temp"]) + "°C", 10, 40, size = 25, fontPath="Ubuntu.ttf")
	TextPAPIRUS.AddText("Temp. Min: " + str(DataMeteo["main"]["temp_min"]) + "°C" + " Temp. Max: " + str(DataMeteo["main"]["temp_max"]) + Units, 10, 65, size = 12, fontPath="Ubuntu.ttf")
	TextPAPIRUS.AddText("Temps: " + DataMeteo["weather"][0]["description"].capitalize(), 10, 85, size = 25, fontPath="Ubuntu.ttf") 

	TextPAPIRUS.AddText(time.strftime("%H:%M", time.localtime()), 200, 10, size = 20, fontPath="Ubuntu.ttf")

	TextPAPIRUS.WriteAll(True)
	time.sleep(10)
	TextPAPIRUS.Clear()

def Musique(): #Fonction Musique (Last.fm)
	ReponseLastFM = rq.get("http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=" + conf["LASTFM"]["UserFM"] + "&limit=1&format=json&api_key=" + conf["LASTFM"]["LastFmAPI"])
	DataLast = json.loads(ReponseLastFM.text)

	TextPAPIRUS.AddText("Last.fm:", 10, 10, size = 20, fontPath="Ubuntu.ttf")
	try:
		if DataLast["recenttracks"]["track"][0]["@attr"]["nowplaying"] == "true":
			TextPAPIRUS.AddText("Actuellement:", 10, 40, size = 25, fontPath="Ubuntu.ttf")
			TextPAPIRUS.AddText(DataLast["recenttracks"]["track"][0]["artist"]["#text"] + " - " + DataLast["recenttracks"]["track"][0]["name"], 10, 65, size = 15, fontPath="Ubuntu.ttf")
			TextPAPIRUS.AddText(DataLast["recenttracks"]["track"][0]["album"]["#text"], 10, 95, size = 10, fontPath="Ubuntu.ttf")

			TextPAPIRUS.AddText("Précédent:", 10, 115, size = 25, fontPath="Ubuntu.ttf")
			TextPAPIRUS.AddText(DataLast["recenttracks"]["track"][1]["artist"]["#text"] + " - " + DataLast["recenttracks"]["track"][1]["name"], 10, 140, size = 15, fontPath="Ubuntu.ttf")
	except:
		TextPAPIRUS.AddText("Précédent:", 10, 40, size = 25, fontPath="Ubuntu.ttf")
		TextPAPIRUS.AddText(DataLast["recenttracks"]["track"][0]["artist"]["#text"] + " - " + DataLast["recenttracks"]["track"][0]["name"], 10, 65, size = 15, fontPath="Ubuntu.ttf")
		TextPAPIRUS.AddText(DataLast["recenttracks"]["track"][0]["album"]["#text"], 10, 95, size = 10, fontPath="Ubuntu.ttf")
	finally:
		TextPAPIRUS.AddText(time.strftime("%H:%M", time.localtime()), 200, 10, size = 20, fontPath="Ubuntu.ttf")
		TextPAPIRUS.WriteAll(True)
		time.sleep(10)
		TextPAPIRUS.Clear()

def Twitch(): #Fonction Twitch
	ReponseTwitchSt1 = rq.get("https://api.twitch.tv/helix/streams?user_login=" + conf["TWITCH"]["TwitchSt1"], headers={"Client-ID": conf["TWITCH"]["TwitchAPI"]})
	ReponseTwitchSt2 = rq.get("https://api.twitch.tv/helix/streams?user_login=" + conf["TWITCH"]["TwitchSt2"], headers={"Client-ID": conf["TWITCH"]["TwitchAPI"]})
	DataSt1 = json.loads(ReponseTwitchSt1.text)
	DataSt2 = json.loads(ReponseTwitchSt2.text)

	TextPAPIRUS.AddText("Twitch:", 10, 10, size = 20, fontPath="Ubuntu.ttf")

	try:
		if DataSt1["data"][0]["type"] == "live":
			ReponseTwitchGameID = rq.get("https://api.twitch.tv/helix/games?id=" + DataSt1["data"][0]["game_id"], headers={"Client-ID": conf["TWITCH"]["TwitchAPI"]})
			GameID = json.loads(ReponseTwitchGameID.text)
			TextPAPIRUS.AddText(conf["TWITCH"]["TwitchSt1"].capitalize() + ": ON", 10, 40, size = 20, fontPath="Ubuntu.ttf")
			TextPAPIRUS.AddText("Jeu: " + GameID["data"][0]["name"], 10, 60, size = 15, fontPath="Ubuntu.ttf")
			TextPAPIRUS.AddText("Titre: " + DataSt1["data"][0]["title"], 10, 75, size = 10, fontPath="Ubuntu.ttf")
	except IndexError:
		TextPAPIRUS.AddText(conf["TWITCH"]["TwitchSt1"].capitalize() + ": OFF", 10, 40, size = 20, fontPath="Ubuntu.ttf")
		
	try:
		if DataSt2["data"][0]["type"] == "live":
			ReponseTwitchGameID = rq.get("https://api.twitch.tv/helix/games?id=" + DataSt2["data"][0]["game_id"], headers={"Client-ID": conf["TWITCH"]["TwitchAPI"]})
			GameID = json.loads(ReponseTwitchGameID.text)
			TextPAPIRUS.AddText(conf["TWITCH"]["TwitchSt2"].capitalize() + ": ON", 10, 95, size = 20, fontPath="Ubuntu.ttf")
			TextPAPIRUS.AddText("Jeu: " + GameID["data"][0]["name"], 10, 115, size = 15, fontPath="Ubuntu.ttf")
			TextPAPIRUS.AddText("Titre: " + DataSt2["data"][0]["title"], 10, 130, size = 10, fontPath="Ubuntu.ttf")
	except IndexError:
		TextPAPIRUS.AddText(conf["TWITCH"]["TwitchSt2"].capitalize() + ": OFF", 10, 132, size = 20, fontPath="Ubuntu.ttf")
	finally:
		TextPAPIRUS.AddText(time.strftime("%H:%M", time.localtime()), 200, 10, size = 20, fontPath="Ubuntu.ttf")
		TextPAPIRUS.WriteAll(True)
		time.sleep(10)
		TextPAPIRUS.Clear()

def Twitter(): #Fonction Twitter
	global BearerAUTH
	ReponseTwitter = rq.get("https://api.twitter.com/1.1/users/show.json?screen_name=" + conf["TWITTER"]["UserTW"], headers={'Authorization': "Bearer " + BearerAUTH})
	DataTwitter = json.loads(ReponseTwitter.text)

	TextPAPIRUS.AddText("Twitter:", 10, 10, size = 20, fontPath="Ubuntu.ttf")

	TextPAPIRUS.AddText("Compte: " + DataTwitter["name"], 10, 40, size = 20, fontPath="Ubuntu.ttf")
	TextPAPIRUS.AddText(str(DataTwitter["followers_count"]) + " abonnés", 10, 65, size = 20, fontPath="Ubuntu.ttf")

	TextPAPIRUS.AddText("Dernier tweet:", 10, 85, size = 20, fontPath="Ubuntu.ttf")
	TextPAPIRUS.AddText(DataTwitter["status"]["text"], 10, 105, size = 15, fontPath="Ubuntu.ttf")

	TextPAPIRUS.AddText(time.strftime("%H:%M", time.localtime()), 200, 10, size = 20, fontPath="Ubuntu.ttf")
	TextPAPIRUS.WriteAll(True)
	time.sleep(10)
	TextPAPIRUS.Clear()
