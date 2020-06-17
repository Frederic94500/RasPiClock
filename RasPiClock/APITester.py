import socket, time
import Services as SV

def APICheck(conf, TextPAPIRUS): #Fonction de test de chaque paramètre (sauf Twitch)
	#Test des APIs
	try:
		if TestMeteo() and TestCrypto() and TestMusique() and TestTwitter() and TestRATP() and TestTwitch(): return True #Fin de la vérification des API
		else: return False

	except (ValueError, socket.error, socket.gaierror, socket.herror, socket.timeout): #Situation d'erreur de connexion
		TextPAPIRUS.Clear()
		TextPAPIRUS.AddText("Erreur de connexion, nouvelle tentative de connexion dans: T", 10, 48, size = 20, fontPath="Ubuntu.ttf", Id="TimerErr")
		for I in range(15):
			TextPAPIRUS.UpdateText("TimerErr", "Erreur de connexion, \nnouvelle tentative de connexion dans: " + str(15 - I), fontPath="Ubuntu.ttf")
			TextPAPIRUS.WriteAll(True)
			time.sleep(1)
		TextPAPIRUS.Clear()
		APICheck()

def TestCrypto():
	if conf["CRYPTO"]["CryptoAPI"] != "":
		i = 1
		ReponseCrypto = SV.SVCrypto(conf, "coin" + str(i))
		try:
			if ReponseCrypto.json()["Response"] == "Error":
				ErrorConfig("Erreur dans la config Crypto, veuillez vérifier votre saisie!")
				return False
		except: return True
	else: return True

def TestMeteo():
	if conf["WEATHER"]["MeteoAPI"] != "":
		ReponseMeteo = SV.SVMeteo(conf)
		if ReponseMeteo.status_code == 200: return True
		else:
			ErrorConfig("Erreur dans la config Météo, veuillez vérifier votre saisie!")
			return False
	else: return True

def TestMusique():
	if conf["LASTFM"]["LastFmAPI"] != "":
		ReponseLastFM = SV.SVMusique(conf)
		if ReponseLastFM.status_code == 200: return True
		else: 
			ErrorConfig("Erreur dans la config LastFM, veuillez vérifier votre saisie!")
			return False
	else: return True

def TestTwitter():
	if conf["TWITTER"]["TwitterAPI"] != "" and conf["TWITTER"]["twitterapisecret"] != "":
		BearerRAW = SV.SVTwitterGetToken(conf)
		if BearerRAW.status_code == 200: 
			BearerAUTH = BearerRAW.json()['access_token']
			ReponseTwitter = SV.SVTwitter(conf, BearerAUTH)
			if ReponseTwitter.status_code == 200:
				return True
			else:
				ErrorConfig("Erreur dans la config Twitter, veuillez vérifier votre saisie!")
				return False
		else:
			ErrorConfig("Erreur lors de la création du token Twitter, veuillez vérifier votre saisie!")
			return False
	else: return True

def TestRATP():
	if conf["RATP"]["typetrans1"] != "" and conf["RATP"]["line1"] != "" and conf["RATP"]["station1"] != "" and conf["RATP"]["sens1"] != "":
		i = 1
		ReponseRATP = SV.SVRATP(conf, "typetrans" + str(i), "line" + str(i), "station" + str(i), "sens" + str(i))
		if ReponseRATP.status_code == 200:
			if conf["RATP"]["typetrans2"] != "" and conf["RATP"]["line2"] != "" and conf["RATP"]["station2"] != "" and conf["RATP"]["sens2"] != "":
				i += 1
				ReponseRATP = SV.SVRATP(conf, "typetrans" + str(i), "line" + str(i), "station" + str(i), "sens" + str(i))
				if ReponseRATP.status_code == 200:
						return True
				else:
					ErrorConfig("Erreur dans la config RATP 2, veuillez vérifier votre saisie!")
					return False
			else: return True
		else:
			ErrorConfig("Erreur dans la config RATP 1, veuillez vérifier votre saisie!")
			return False
	else: return True

def TestTwitch():
	if conf["TWITCH"]["twitchapiclientid"] != "":
		i = 1
		ReponseID = SV.SVTwitchGetID(conf, "TwitchSt" + str(i))
		if ReponseID.status_code == 200:
			if conf["TWITCH"]["TwitchSt2"] != "":
				i += 1
				ReponseID = SV.SVTwitchGetID(conf, "TwitchSt" + str(i))
				if ReponseID.status_code == 200:
					return True
				else:
					ErrorConfig("Erreur dans la config Twitch, veuillez vérifier votre saisie!")
					return False
			else: return True
		else: 
			ErrorConfig("Erreur dans la config Twitch, veuillez vérifier votre saisie!")
			return False
	else: return True

def ErrorConfig(ERROR):
	print(ERROR)

