import threading as th
import requests as rq
import sys
import time

B = 1

def API():
	try:
		while B == 1:
			global ReponseCrypto
			global ReponseMeteo
			global ReponseLastFM
			global ReponseTwitchMV
			global ReponseTwitchZ
			global ReponseTwitter
			ReponseCrypto = rq.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH&tsyms=USD&api_key=261d6b25933c3a0ccd3b991898b6ed86ac7815ec7ebedda674dd7ff116f23e51")
			ReponseMeteo = rq.get("https://api.openweathermap.org/data/2.5/weather?q=Champigny-sur-Marne,fr&units=metric&lang=fr&appid=b3e6135efddd4b5f7ebc6add6fb003f3")
			ReponseLastFM = rq.get("http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=Frederic94500&api_key=5bf1ea23824ae3745971ec27e036d3fa&limit=1&format=json")
			ReponseTwitter = rq.get("https://api.twitter.com/1.1/users/show.json?screen_name=Frederic94500", headers={'Authorization': "Bearer AAAAAAAAAAAAAAAAAAAAAGRr9QAAAAAApU6cp18UYHWmOtfqvvPZ783n7kI%3DVcwCE2OxcjpJuaR6bFdUAkF6gQQDlBgYHqLpSVYciHgeQRQEfF"})
			ReponseTwitchZ = rq.get("https://api.twitch.tv/helix/streams?user_login=zerator", headers={"Client-ID": "6k8zx7uira85jc67wzh5m03sxzn4xb"})
			ReponseTwitchMV = rq.get("https://api.twitch.tv/helix/streams?user_login=mistermv", headers={"Client-ID": "6k8zx7uira85jc67wzh5m03sxzn4xb"})
			time.sleep(5)
	except KeyboardInterrupt:
		sys.exit()