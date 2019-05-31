# -*- encoding: utf-8 -*-
#RasPiClock - Frédéric94500, EliottCheypeplus, ParsaEtz

import time, json, sys, os, socket, configparser, hashlib, webbrowser, threading
import requests as rq
from tkinter import *
from tkinter.messagebox import *
from tkinter import ttk
from PIL import Image, ImageTk

Units = "°K"

STOP = False

BearerAUTH = ""

conf = configparser.ConfigParser()
conf.read("config.cfg")

if os.path.exists('/etc/default/epd-fuse'):
	from papirus import Papirus, PapirusTextPos
	Ecran = Papirus()
	TextPAPIRUS = PapirusTextPos(False)
	TextPAPIRUS.Clear()

	def Main(): #Fonction Coeur
		try:
			if conf["TWITTER"]["TwitterAPI"] != "" and conf["TWITTER"]["twitterapisecret"] != "":
				global BearerAUTH
				BearerRAW = os.popen("curl -u '"+ conf["TWITTER"]["TwitterAPI"] + ":" + conf["TWITTER"]["TwitterAPISecret"] + "' --data 'grant_type=client_credentials' 'https://api.twitter.com/oauth2/token'").read()
				BearerJSON = json.loads(BearerRAW)
				BearerAUTH = BearerJSON["access_token"]
			while True:
				global STOP
				if STOP: #GUI ONLY
					BoutonAfficher.configure(state=NORMAL)
					BoutonArreter.configure(state=DISABLED)
					Texte.set("Veuillez saisir vos informations")
					os.system("papirus-clear")
					break;
				else:
					if conf["CRYPTO"]["CryptoAPI"] != "":
						Crypto()
					if conf["WEATHER"]["MeteoAPI"] != "":
						Meteo()
					if conf["LASTFM"]["LastFmAPI"] != "":
						Musique()
					if conf["TWITCH"]["TwitchAPI"] != "":
						Twitch()
					if conf["TWITTER"]["TwitterAPI"] != "" and conf["TWITTER"]["twitterapisecret"] != "":
						Twitter()
		except (ValueError, socket.error, socket.gaierror, socket.herror, socket.timeout): #Situation d'erreur de connexion
			TextPAPIRUS.Clear()
			TextPAPIRUS.AddText("ERREUR de connexion, nouvelle tentative de connexion dans: T", 10, 48, size = 20, fontPath="Ubuntu.ttf", Id="TimerErr")
			for I in range(15):
				TextPAPIRUS.UpdateText("TimerErr", "Erreur de connexion, \nnouvelle tentative de connexion dans: " + str(15 - I), fontPath="Ubuntu.ttf")
				TextPAPIRUS.WriteAll(True)
				time.sleep(1)
			TextPAPIRUS.Clear()
			Main()
		except KeyboardInterrupt: #BASH ONLY
			print("Vous avez arrêté le processus, nettoyage de l'écran")
			os.system("papirus-clear")
			sys.exit()

	def HashSave():
		ConfFile = open("config.cfg","rb")
		bytes = ConfFile.read()
		hashconf = hashlib.sha256(bytes).hexdigest()
		ConfFile.close()

		HashFile = open("hash.txt", "w")
		HashFile.write(hashconf)
		HashFile.close()

		Adaptation()

	def HashVerify():
		ConfFile = open('config.cfg', "rb")
		bytes = ConfFile.read()
		HashNew = hashlib.sha256(bytes).hexdigest()
		ConfFile.close()
	
		HashFile = open('hash.txt', "r")
		HashOld = HashFile.read()
		HashFile.close()

		if HashOld != HashNew:
			APICheck()
		if HashOld == HashNew:
			Adaptation()

	def APICheck(): #Fonction de test de chaque paramètre (sauf Twitch)
		global BearerAUTH
		Check = 0
		#Test des APIs
		try:
			if conf["WEATHER"]["MeteoAPI"] != "":
				ReponseMeteo = rq.get("https://api.openweathermap.org/data/2.5/weather?q=" + conf["WEATHER"]["City"] + "&units=" + conf["WEATHER"]["Units"] + "&lang=" + conf["WEATHER"]["Lang"] + "&appid=" + conf["WEATHER"]["MeteoAPI"])
				DataMeteo = json.loads(ReponseMeteo.text)
				if 400 <= int(DataMeteo["cod"]) <= 599: 
						ERROR = "Erreur dans la config Météo, veuillez vérifier votre saisie!"
						ErrorConfig(ERROR)
				else:
					Check += 1
			else:
				Check += 1

			if conf["CRYPTO"]["CryptoAPI"] != "":
				ReponseCrypto = rq.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=" + conf["CRYPTO"]["Coin1"] + "," + conf["CRYPTO"]["Coin2"] + "&tsyms=" + conf["CRYPTO"]["Currency"] + "&api_key=" + conf["CRYPTO"]["CryptoAPI"])
				DataCrypto = json.loads(ReponseCrypto.text)
				try:
					if DataCrypto["Response"] == "Error":
						ERROR = "Erreur dans la config Crypto, veuillez vérifier votre saisie!"
						ErrorConfig(ERROR)
				except KeyError:
					Check += 1
			else:
				Check += 1

			if conf["LASTFM"]["LastFmAPI"] != "":
				ReponseLastFM = rq.get("http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=" + conf["LASTFM"]["UserFM"] + "&limit=1&format=json&api_key=" + conf["LASTFM"]["LastFmAPI"])
				DataLast = json.loads(ReponseLastFM.text)
				try:
					if 2 <= int(DataLast["error"]) <= 29:
						ERROR = "Erreur dans la config LastFM, veuillez vérifier votre saisie!"
						ErrorConfig(ERROR)
				except KeyError:
					Check += 1
			else:
				Check += 1

			if conf["TWITTER"]["TwitterAPI"] != "":
				try:
					try:
						BearerRAW = os.popen("curl -u '"+ conf["TWITTER"]["TwitterAPI"] + ":" + conf["TWITTER"]["TwitterAPISecret"] + "' --data 'grant_type=client_credentials' 'https://api.twitter.com/oauth2/token'").read()
						BearerJSON = json.loads(BearerRAW)
						BearerAUTH = BearerJSON["access_token"]
					except KeyError:
						ERROR = "Erreur dans la config Twitter, il faut 2 clés API! Veuillez vérifier votre saisie!"
						ErrorConfig(ERROR)
					finally:
						ReponseTwitter = rq.get("https://api.twitter.com/1.1/users/show.json?screen_name=" + conf["TWITTER"]["UserTW"], headers={'Authorization': "Bearer " + BearerAUTH})
						DataTwitter = json.loads(ReponseTwitter.text)
						if 49 <= int(DataTwitter["errors"][0]["code"]) <= 599:
							ERROR = "Erreur dans la config Twitter, veuillez vérifier votre saisie!"
							ErrorConfig(ERROR)
				except KeyError:
					Check += 1
			else:
				Check += 1

		except (ValueError, socket.error, socket.gaierror, socket.herror, socket.timeout): #Situation d'erreur de connexion
			TextPAPIRUS.Clear()
			TextPAPIRUS.AddText("Erreur de connexion, nouvelle tentative de connexion dans: T", 10, 48, size = 20, fontPath="Ubuntu.ttf", Id="TimerErr")
			for I in range(15):
				TextPAPIRUS.UpdateText("TimerErr", "Erreur de connexion, \nnouvelle tentative de connexion dans: " + str(15 - I), fontPath="Ubuntu.ttf")
				TextPAPIRUS.WriteAll(True)
				time.sleep(1)
			TextPAPIRUS.Clear()
			APICheck()

		finally: #Fin de la vérification des API
			if Check == 4:
				HashSave()

	def ErrorConfig(ERROR):
		try:
			if sys.argv[1] == "-bash" or sys.argv[1] == "-b": #BASH ONLY
					print(ERROR)
					sys.exit()
		except IndexError: #GUI ONLY
			WARN = showerror("Erreur!", ERROR)
			Texte.set("Erreur dans l'éxécution!")
			BoutonAfficher.configure(state=NORMAL)
			BoutonArreter.configure(state=DISABLED)

	def Adaptation():
		global Units

		if conf["WEATHER"]["Units"] == "imperial":
			Units = "°F"
		if conf["WEATHER"]["Units"] == "metric":
			Units = "°C"
		else:
			Units = "°K"

		Main()

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

	try:
		if sys.argv[1] == "-bash" or sys.argv[1] == "-b": #BASH ONLY
			HashVerify()
		else: #Erreur d'argument
			print("Erreur, veuillez écrire -b ou -bash ou rien pour éxécuter le programme!")
	except IndexError: #Par défaut
		global ZoneTexte
		TABList = ["tabCrypto", "tabMeteo", "tabMusic", "tabTwitch", "tabTwitter"]
		TABText = ["Crypto", "Météo", "Musique", "Twitch", "Twitter"]
		NBArg = [4, 4, 2, 3, 3]
		TEXTEntry = [["Clé API", "Monnaie fiduciaire", "Cryptomonnaie 1", "Cryptomonnaie 2"],["Clé API", "Ville", "Unité", "Langue"],["Clé API", "Utilisateur"],["Clé API", "Streamer 1", "Streamer 2"],["Clé API", "Clé API Secret", "Utilisateur"]]
		TEXTConfig = [["CryptoAPI", "Currency", "Coin1", "Coin2"],["MeteoAPI", "City", "Units", "Lang"],["LastFmAPI", "UserFM"],["TwitchAPI", "TwitchSt1", "TwitchSt2"],["TwitterAPI", "TwitterAPISecret", "UserTW"]]
		CONFCat = ["CRYPTO", "WEATHER", "LASTFM", "TWITCH", "TWITTER"]
		ZoneTexte = ["CryptoAPI", "Currency", "Coin1", "Coin2", "MeteoAPI", "City", "Units", "Lang", "LastFmAPI", "UserFM", "TwitchAPI", "TwitchSt1", "TwitchSt2", "TwitterAPI", "TwitterAPISecret", "UserTW"]
		I2 = 0
		def Save(): #Fonction d'enregistrement du fichier de conf
			I2 = 0

			for I0 in range(5):
				for I1 in range(NBArg[I0]):
					conf[CONFCat[I0]][TEXTConfig[I0][I1]] = ZoneTexte[I2].get()
					I2 += 1

			with open('config.cfg', 'w') as CFGF:
				conf.write(CFGF)

			HashVerify()

		def Afficher(): #Fonction de démarrage
			BoutonAfficher.configure(state=DISABLED)
			BoutonArreter.configure(state=NORMAL)
			Texte.set("En cours d'éxécution")

			global STOP
			STOP = False
			threadRas = threading.Thread(target=Save)
			threadRas.start()
		
		def Arret(): #Fonction d'arrêt
			BoutonArreter.configure(state=DISABLED)
			Texte.set("En cours d'arrêt")

			global STOP
			STOP = True
	
		#Fonctions Sites web
		def WebProj():
			webbrowser.open_new_tab('https://github.com/Frederic94500/Resistance-ISN')

		def WebAuteurF(event):
			webbrowser.open_new_tab('https://twitter.com/Frederic94500')
		def WebAuteurE(event):
			webbrowser.open_new_tab('https://github.com/EliottCheypeplus')
		def WebAuteurP(event):
			webbrowser.open_new_tab('https://github.com/ParsaEtz')

		def WebLicence(event):
			webbrowser.open_new_tab('https://github.com/Frederic94500/RasPiClock-ISN/blob/master/LICENSE')
		
		def APropos(): #Fonction à propos (créateur + licence)(ouvre une nouvelle fenêtre)
			About = Toplevel()
			About.title("A propos et licence")

			AbText = [0, 1, 2, 3, 4, 5]

			AbText[0] = Label(About, text = "Ce programme a été fait par")
			AbText[1] = Label(About, text = "Frédéric94500,", fg = "blue", cursor = "hand2")
			AbText[2] = Label(About, text = "Eliott,", fg = "blue", cursor = "hand2")
			AbText[3] = Label(About, text = "Parsa", fg = "blue", cursor = "hand2")
			AbText[4] = Label(About, text = "sous la licence")
			AbText[5] = Label(About, text = "GPL-3.0", fg = "blue", cursor = "hand2")

			AbText[1].bind("<Button-1>", WebAuteurF)
			AbText[2].bind("<Button-1>", WebAuteurE)
			AbText[3].bind("<Button-1>", WebAuteurP)
			AbText[5].bind("<Button-1>", WebLicence)

			[AbText[I].pack(side = "left", pady = 10) for I in range(6)]

			photo = ImageTk.PhotoImage(Image.open("gpl.png"))
			img = Label(About, image=photo)
			img.image = photo
			img.pack()

			ico = ImageTk.PhotoImage(file='icon.ico')
			Fenetre.tk.call('wm', 'iconphoto', About._w, ico)

		#Création Fenètre
		Fenetre = Tk()
		Fenetre.title('RasPiClock GUI')

		ico = ImageTk.PhotoImage(file='icon.ico')
		Fenetre.tk.call('wm', 'iconphoto', Fenetre._w, ico)

		#Création barre de menu
		menubar = Menu(Fenetre)

		filemenu = Menu(menubar, tearoff=0)
		menubar.add_cascade(label = "Fichier", menu = filemenu)
		filemenu.add_command(label = "Quitter", command = Fenetre.destroy)

		helpmenu = Menu(menubar, tearoff=0)
		menubar.add_cascade(label = "Aide", menu = helpmenu)
		helpmenu.add_command(label = "Vistez le GitHub", command = WebProj)
		helpmenu.add_separator()
		helpmenu.add_command(label = "A propos et licence", command = APropos)

		Fenetre.config(menu=menubar)

		#Création onglets
		TAB = ttk.Notebook(Fenetre)

		for I in range(5):
			TABList[I] = ttk.Frame(TAB)
			TAB.add(TABList[I], text=TABText[I])

		TAB.pack(expand=1, fill='both')

		#Création Grid
		for I0 in range(5): #Nombre de tab
			for I1 in range(NBArg[I0]): #Nombre d'argument
				Label(TABList[I0], text=TEXTEntry[I0][I1]).grid(row=I1, padx=5, pady=5)

				ARGUMENT = StringVar()
				ARGUMENT.set(conf[CONFCat[I0]][TEXTConfig[I0][I1]])
				ZoneTexte[I2] = Entry(TABList[I0], textvariable=ARGUMENT)
				ZoneTexte[I2].grid(row=I1, column=1, padx=5, pady=5, sticky=E)
				I2 += 1

		#Création bouton fenetre
		BoutonAfficher = Button(Fenetre, text='Afficher', command = Afficher, state=NORMAL)
		BoutonAfficher.pack(side = RIGHT, padx=5, pady=5)

		BoutonArreter = Button(Fenetre, text='Arrêter', command = Arret, state=DISABLED)
		BoutonArreter.pack(side = RIGHT, padx=5, pady=5)

		#Création Texte Annonce
		Texte = StringVar()
		TextAnnonce = Label(Fenetre, textvariable = Texte).pack(side = LEFT)
		Texte.set("Veuillez saisir vos informations")

		#Initialisation du GUI
		Fenetre.mainloop()

else: #Si papirus n'est pas installé
	try:
		if sys.argv[1] == "-bash" or sys.argv[1] == "-b": #BASH ONLY
			print("Attention!, vous n'avez pas installé la biblothèque Papirus, veuillez l'installer via https://github.com/PiSupply/PaPiRus")
			sys.exit()
		else: #Erreur d'argument
			print("Erreur, veuillez écrire -b ou -bash ou rien et installer Papirus (https://github.com/PiSupply/PaPiRus) pour éxécuter le programme!")
	except IndexError: #GUI ONLY
		WARN = showerror("Attention!", "Vous n'avez pas installé la biblothèque Papirus, veuillez l'installer via https://github.com/PiSupply/PaPiRus.")
	
