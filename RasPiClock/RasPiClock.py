# -*- encoding: utf-8 -*-
#RasPiClock - Frédéric94500, EliottCheypeplus, ParsaEtz

import time, json, sys, os, socket, configparser, hashlib, webbrowser, threading
import requests as rq
from tkinter import *
from tkinter.messagebox import *
from tkinter import ttk
from PIL import Image, ImageTk

Metric = "°C"
Imperial = "°F"

#Fonction Main
def Main():
	try:
		while True:
			global STOP
			if STOP: #BUG
				break;
			else:
				Crypto()
				Meteo()
				Musique()
				Twitch()
				Twitter()
	except (ValueError, socket.error, socket.gaierror, socket.herror, socket.timeout): #Situation d'erreur de connexion
		TextEtImg.Clear()
		TextEtImg.AddText("ERREUR de connexion, nouvelle tentative de connexion dans: T", 10, 48, size = 20, fontPath="Ubuntu.ttf", Id="TimerErr")
		for I in range(15):
			TextEtImg.UpdateText("TimerErr", "ERREUR de connexion, \nnouvelle tentative de connexion dans: " + str(15 - I), fontPath="Ubuntu.ttf")
			TextEtImg.WriteAll(True)
			time.sleep(1)
		TextEtImg.Clear()
		Main()
	except KeyboardInterrupt: #BASH ONLY
		print("Vous avez arrêté le processus, nettoyage de l'écran")
		os.system("papirus-clear")
		sys.exit()
	#finally: #GUI ONLY et BUG
		#os.system("papirus-clear")
		#sys.exit()

def HashSave():
	with open("config.cfg","rb") as f:
		bytes = f.read()
		hashconf = hashlib.sha256(bytes).hexdigest()

	hash = open("hash.txt", "w")
	hash.write(hashconf)
	hash.close
	Main()

def HashVerify():
	with open('config.cfg', "rb") as FC:
		bytes = FC.read()
		HashNew = hashlib.sha256(bytes).hexdigest()
	
	FH = open('hash.txt', "r")
	HashOld = FH.read()

	if HashOld != HashNew:
		APICheck()
	if HashOld == HashNew:
		Main()

#Fonction de test de chaque paramètre (sauf Twitch)
def APICheck():
	Check = 0
	ReponseCrypto = rq.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=" + conf["CRYPTO"]["Coin1"] + "," + conf["CRYPTO"]["Coin2"] + "&tsyms=" + conf["CRYPTO"]["Currency"] + "&api_key=" + conf["CRYPTO"]["CryptoAPI"])
	DataCrypto = json.loads(ReponseCrypto.text)
	ReponseMeteo = rq.get("https://api.openweathermap.org/data/2.5/weather?q=" + conf["WEATHER"]["City"] + "&units=" + conf["WEATHER"]["Units"] + "&lang=" + conf["WEATHER"]["Lang"] + "&appid=" + conf["WEATHER"]["MeteoAPI"])
	DataMeteo = json.loads(ReponseMeteo.text)
	ReponseLastFM = rq.get("http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=" + conf["LASTFM"]["UserFM"] + "&limit=1&format=json&api_key=" + conf["LASTFM"]["LastFmAPI"])
	DataLast = json.loads(ReponseLastFM.text)
	ReponseTwitter = rq.get("https://api.twitter.com/1.1/users/show.json?screen_name=" + conf["SOCIAL"]["UserTW"], headers={'Authorization': "Bearer " + conf["TWITTER"]["TwitterAPI"]})
	DataTwitter = json.loads(ReponseTwitter.text)

	try:
		try: #Test des APIs
			if DataCrypto["Response"] == "Error":
				ERROR = "Erreur dans la config Crypto, veuiller vérifier votre saisie!"
				ErrorConfig(ERROR)
		except (KeyError):
			Check += 1
		try:
			if DataMeteo["cod"] == range(400, 599):
				ERROR = "Erreur dans la config Météo, veuiller vérifier votre saisie!"
				ErrorConfig(ERROR)
		except (KeyError):
			Check += 1
		try:
			if DataLast["error"] == range(2, 29):
				ERROR = "Erreur dans la config LastFM, veuiller vérifier votre saisie!"
				ErrorConfig(ERROR)
		except (KeyError):
			Check += 1
		try:
			if DataTwitter["errors"][0]["code"] == range(49, 599):
				ERROR = "Erreur dans la config Twitter, veuiller vérifier votre saisie!"
				ErrorConfig(ERROR)
		except (KeyError):
			Check += 1

	except (ValueError, socket.error, socket.gaierror, socket.herror, socket.timeout): #Situation d'erreur de connexion
		TextEtImg.Clear()
		TextEtImg.AddText("ERREUR de connexion, nouvelle tentative de connexion dans: T", 10, 48, size = 20, fontPath="Ubuntu.ttf", Id="TimerErr")
		for I in range(15):
			TextEtImg.UpdateText("TimerErr", "ERREUR de connexion, \nnouvelle tentative de connexion dans: " + str(15 - I), fontPath="Ubuntu.ttf")
			TextEtImg.WriteAll(True)
			time.sleep(1)
		TextEtImg.Clear()
		APICheck()

	finally: #Fin de la vérification des API
		if Check == 4:
			HashSave()

def ErrorConfig(ERROR):
	if conf["GENERAL"]["GUI"] == "1":
		WARN = showerror("Attention!", ERROR)
	else:
		print(ERROR)
		sys.exit()

def Save(): #Fonction d'enregistrement du fichier de conf
	ZoneTexte = ["CryptoAPI", "MeteoAPI", "LastFmAPI", "TwitchAPI", "TwitterAPI", "Currency", "Coin1", "Coin2", "City", "Units", "Lang", "UserFM", "TwitchSt1", "TwitchSt2", "UserTW"]
	CONFCat = ["CRYPTO", "WEATHER", "LASTFM", "TWITCH", "TWITTER"]
	NBArg = [4, 4, 2, 3, 2]
	TEXTConfig = [["CryptoAPI", "Currency", "Coin1", "Coin2"],["MeteoAPI", "City", "Units", "Lang"],["LastFmAPI", "UserFM"],["TwitchAPI", "TwitchSt1", "TwitchSt2"],["TwitterAPI", "UserTW"]]
	ZoneTexte = ["CryptoAPI", "Currency", "Coin1", "Coin2", "MeteoAPI", "City", "Units", "Lang", "LastFmAPI", "UserFM", "TwitchAPI", "TwitchSt1", "TwitchSt2", "TwitterAPI", "UserTW"]
	I2 = 0

	for I0 in range(5):
		for I1 in range(NBArg[I0]):
			conf[CONFCat[I0]][TEXTConfig[I0][I1]] = ZoneTexte[I2]
			I2 += 1

	with open('config.cfg', 'w') as configfile:
		configfile.write(configfile)

	HashVerify()

def Crypto(): #Fonction Crypto (CryproCompare)
	TextEtImg.AddText("Crypto:", 10, 10, size = 20, fontPath="Ubuntu.ttf")

	ReponseCrypto = rq.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=" + conf["CRYPTO"]["Coin1"] + "," + conf["CRYPTO"]["Coin2"] + "&tsyms=" + conf["CRYPTO"]["Currency"] + "&api_key=" + conf["CRYPTO"]["CryptoAPI"])
	DataCrypto = json.loads(ReponseCrypto.text)

	PCTC1 = list(str(DataCrypto["RAW"][conf["CRYPTO"]["Coin1"]][conf["CRYPTO"]["Currency"]]["CHANGEPCT24HOUR"]))
	del PCTC1[-14:-1]
	PCTC2 = list(str(DataCrypto["RAW"][conf["CRYPTO"]["Coin2"]][conf["CRYPTO"]["Currency"]]["CHANGEPCT24HOUR"]))
	del PCTC2[-14:-1]

	TextEtImg.AddText(conf["CRYPTO"]["Coin1"] + " " + conf["CRYPTO"]["Currency"] + " " + str(DataCrypto["RAW"][conf["CRYPTO"]["Coin1"]][conf["CRYPTO"]["Currency"]]["PRICE"]), 10, 44, size = 25, fontPath="Ubuntu.ttf")
	TextEtImg.AddText(conf["CRYPTO"]["Coin2"] + " " + conf["CRYPTO"]["Currency"] + " " + str(DataCrypto["RAW"][conf["CRYPTO"]["Coin2"]][conf["CRYPTO"]["Currency"]]["PRICE"]), 10, 114, size = 25, fontPath="Ubuntu.ttf")
	TextEtImg.AddText("".join(PCTC1) + "%", 10, 74, size = 15, fontPath="Ubuntu.ttf")
	TextEtImg.AddText("".join(PCTC2) + "%", 10, 144, size = 15, fontPath="Ubuntu.ttf")

	TextEtImg.AddText(time.strftime("%H:%M", time.localtime()), 200, 10, size = 20, fontPath="Ubuntu.ttf")

	TextEtImg.WriteAll(True)
	time.sleep(10)
	TextEtImg.Clear()

def Meteo(): #Fonction Météo (OpenWeatherMap)
	ReponseMeteo = rq.get("https://api.openweathermap.org/data/2.5/weather?q=" + conf["WEATHER"]["City"] + "&units=" + conf["WEATHER"]["Units"] + "&lang=" + conf["WEATHER"]["Lang"] + "&appid=" + conf["WEATHER"]["MeteoAPI"])
	DataMeteo = json.loads(ReponseMeteo.text)

	TextEtImg.AddText("Météo:", 10, 10, size = 20, fontPath="Ubuntu.ttf")
	TextEtImg.AddText("Température: " + str(DataMeteo["main"]["temp"]) + "°C", 10, 40, size = 25, fontPath="Ubuntu.ttf")
	TextEtImg.AddText("Temp. Min: " + str(DataMeteo["main"]["temp_min"]) + "°C" + " Temp. Max: " + str(DataMeteo["main"]["temp_max"]) + "°C", 10, 65, size = 12, fontPath="Ubuntu.ttf")
	TextEtImg.AddText("Temps: " + DataMeteo["weather"][0]["description"], 10, 85, size = 25, fontPath="Ubuntu.ttf") 

	TextEtImg.AddText(time.strftime("%H:%M", time.localtime()), 200, 10, size = 20, fontPath="Ubuntu.ttf")

	TextEtImg.WriteAll(True)
	time.sleep(10)
	TextEtImg.Clear()

def Musique(): #Fonction Musique (Last.fm)
	ReponseLastFM = rq.get("http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=" + conf["LASTFM"]["UserFM"] + "&limit=1&format=json&api_key=" + conf["LASTFM"]["LastFmAPI"])
	DataLast = json.loads(ReponseLastFM.text)

	TextEtImg.AddText("Last.fm:", 10, 10, size = 20, fontPath="Ubuntu.ttf")
	try:
		if DataLast["recenttracks"]["track"][0]["@attr"]["nowplaying"] == "true":
			TextEtImg.AddText("Actuellement:", 10, 40, size = 25, fontPath="Ubuntu.ttf")
			TextEtImg.AddText(DataLast["recenttracks"]["track"][0]["artist"]["#text"] + " - " + DataLast["recenttracks"]["track"][0]["name"], 10, 65, size = 15, fontPath="Ubuntu.ttf")
			TextEtImg.AddText(DataLast["recenttracks"]["track"][0]["album"]["#text"], 10, 95, size = 10, fontPath="Ubuntu.ttf")

			TextEtImg.AddText("Précédent:", 10, 115, size = 25, fontPath="Ubuntu.ttf")
			TextEtImg.AddText(DataLast["recenttracks"]["track"][1]["artist"]["#text"] + " - " + DataLast["recenttracks"]["track"][1]["name"], 10, 140, size = 15, fontPath="Ubuntu.ttf")
	except:
		TextEtImg.AddText("Précédent:", 10, 40, size = 25, fontPath="Ubuntu.ttf")
		TextEtImg.AddText(DataLast["recenttracks"]["track"][0]["artist"]["#text"] + " - " + DataLast["recenttracks"]["track"][0]["name"], 10, 65, size = 15, fontPath="Ubuntu.ttf")
		TextEtImg.AddText(DataLast["recenttracks"]["track"][0]["album"]["#text"], 10, 95, size = 10, fontPath="Ubuntu.ttf")
	finally:
		TextEtImg.AddText(time.strftime("%H:%M", time.localtime()), 200, 10, size = 20, fontPath="Ubuntu.ttf")
		TextEtImg.WriteAll(True)
		time.sleep(10)
		TextEtImg.Clear()

def Twitch(): #Fonction Twitch
	ReponseTwitchSt1 = rq.get("https://api.twitch.tv/helix/streams?user_login=" + conf["TWITCH"]["TwitchSt1"], headers={"Client-ID": conf["TWITCH"]["TwitchAPI"]})
	ReponseTwitchSt2 = rq.get("https://api.twitch.tv/helix/streams?user_login=" + conf["TWITCH"]["TwitchSt2"], headers={"Client-ID": conf["TWITCH"]["TwitchAPI"]})
	DataSt1 = json.loads(ReponseTwitchSt1.text)
	DataSt2 = json.loads(ReponseTwitchSt2.text)

	TextEtImg.AddText("Twitch:", 10, 10, size = 20, fontPath="Ubuntu.ttf")

	try:
		if DataSt1["data"][0]["type"] == "live":
			TextEtImg.AddText(conf["TWITCH"]["TwitchSt1"] + ": ON", 10, 100, size = 20, fontPath="Ubuntu.ttf")
	except IndexError:
		TextEtImg.AddText(conf["TWITCH"]["TwitchSt1"] + ": OFF", 10, 100, size = 20, fontPath="Ubuntu.ttf")
	try:
		if DataSt2["data"][0]["type"] == "live":
			TextEtImg.AddText(conf["TWITCH"]["TwitchSt2"] + ": ON", 10, 130, size = 20, fontPath="Ubuntu.ttf")
	except IndexError:
		TextEtImg.AddText(conf["TWITCH"]["TwitchSt2"] + ": OFF", 10, 130, size = 20, fontPath="Ubuntu.ttf")
	finally:
		TextEtImg.AddText(time.strftime("%H:%M", time.localtime()), 200, 10, size = 20, fontPath="Ubuntu.ttf")
		TextEtImg.WriteAll(True)
		time.sleep(10)
		TextEtImg.Clear()

def Twitter():
	ReponseTwitter = rq.get("https://api.twitter.com/1.1/users/show.json?screen_name=" + conf["TWITTER"]["UserTW"], headers={'Authorization': "Bearer " + conf["TWITTER"]["TwitterAPI"]})
	DataTwitter = json.loads(ReponseTwitter.text)

	TextEtImg.AddText("Twitter:", 10, 10, size = 20, fontPath="Ubuntu.ttf")

	TextEtImg.AddText("Compte de: " + DataTwitter["name"] + " | " + str(DataTwitter["followers_count"]) + " abonnés", 10, 40, size = 15, fontPath="Ubuntu.ttf")

	TextEtImg.AddText("Dernier tweet\n" + DataTwitter["status"]["text"], 10, 65, size = 15, fontPath="Ubuntu.ttf")

	TextEtImg.AddText(time.strftime("%H:%M", time.localtime()), 200, 10, size = 20, fontPath="Ubuntu.ttf")
	TextEtImg.WriteAll(True)
	time.sleep(10)
	TextEtImg.Clear()

	

conf = configparser.ConfigParser()
conf.read("config.cfg")

if os.path.exists('/etc/default/epd-fuse'):
	from papirus import Papirus, PapirusComposite
	Ecran = Papirus()
	TextEtImg = PapirusComposite(False)
	TextEtImg.Clear()
	
	if conf["GENERAL"]["GUI"] == "1":
		#Fonction "Quand on appuie sur "enter""
		def Enter(event):
			Afficher()

		def Afficher():
			BoutonAfficher.configure(state=DISABLED)
			BoutonArreter.configure(state=NORMAL)

			global STOP
			STOP = False
			threadRas = threading.Thread(target=Main)
			threadRas.start()
		
		def Arret():
			BoutonAfficher.configure(state=NORMAL)
			BoutonArreter.configure(state=DISABLED)

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

		#Fonction à propos (créateur + licence)(ouvre une nouvelle fenêtre)
		def APropos():
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

			#About.iconbitmap('icon.ico')

		#Création Fenètre
		Fenetre = Tk()
		Fenetre.title('GUI')
		#Fenetre.iconbitmap('icon.ico')

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

		#Quand on appuie sur "enter"
		#Fenetre.bind('<Enter>', Enter)

		#Création onglets
		TABList = ["tabCrypto", "tabMeteo", "tabMusic", "tabTwitch", "tabTwitter"]
		TABText = ["Crypto", "Météo", "Musique", "Twitch", "Twitter"]
		NBArg = [4, 4, 2, 3, 2]
		TEXTEntry = [["Clé API", "Monnaie fiduciaire", "Cryptomonnaie 1", "Cryptomonnaie 2"],["Clé API", "Ville", "Unité", "Langue"],["Clé API", "Utilisateur"],["Clé API", "Streamer 1", "Streamer 2"],["Clé API", "Utilisateur"]]
		TEXTConfig = [["CryptoAPI", "Currency", "Coin1", "Coin2"],["MeteoAPI", "City", "Units", "Lang"],["LastFmAPI", "UserFM"],["TwitchAPI", "TwitchSt1", "TwitchSt2"],["TwitterAPI", "UserTW"]]
		CONFCat = ["CRYPTO", "WEATHER", "LASTFM", "TWITCH", "TWITTER"]
		ZoneTexte = ["CryptoAPI", "Currency", "Coin1", "Coin2", "MeteoAPI", "City", "Units", "Lang", "LastFmAPI", "UserFM", "TwitchAPI", "TwitchSt1", "TwitchSt2", "TwitterAPI", "UserTW"]

		TAB = ttk.Notebook(Fenetre)

		for I in range(5):
			TABList[I] = ttk.Frame(TAB)
			TAB.add(TABList[I], text=TABText[I])

		TAB.pack(expand=1, fill='both')

		#Création Grid
		I2 = 0
		for I0 in range(5): #Nombre de tab
			for I1 in range(NBArg[I0]): #Nombre d'argument
				Label(TABList[I0], text=TEXTEntry[I0][I1]).grid(row=I1, padx=5, pady=5)

				ARGUMENT = StringVar()
				ARGUMENT.set(conf[CONFCat[I0]][TEXTConfig[I0][I1]])
				ZoneTexte[I2] = Entry(TABList[I0], textvariable=ARGUMENT).grid(row=I1, column=1, padx=5, pady=5, sticky=E)
				I2 += 1

		#Création bouton fenetre
		BoutonAfficher = Button(Fenetre, text='Afficher', command = Afficher, state=NORMAL)
		BoutonAfficher.pack(side = RIGHT, padx=5, pady=5)

		BoutonArreter = Button(Fenetre, text='Arrêter', command = Arret, state=DISABLED)
		BoutonArreter.pack(side = RIGHT, padx=5, pady=5)

		#Création Texte et Texte Annonce
		Texte = StringVar()
		TextAnnonce = Label(Fenetre, textvariable = Texte).pack(side = LEFT)
		Texte.set("Veuillez saisir vos informations.")

		#Initialisation du GUI
		Fenetre.mainloop()

	else: #Par défaut
		HashVerify()

else:
	if conf["GENERAL"]["GUI"] == "1":
		WARN = showerror("Attention!", "Vous n'avez pas installé la biblothèque Papirus, veuillez l'installer via https://github.com/PiSupply/PaPiRus.")
		sys.exit()
	else:
		print("Attention!, vous n'avez pas installé la biblothèque Papirus, veuillez l'installer via https://github.com/PiSupply/PaPiRus")
		sys.exit()
