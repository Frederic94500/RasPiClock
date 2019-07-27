# -*- encoding: utf-8 -*-
#RasPiClock - Frédéric94500, EliottCheypeplus, ParsaEtz

import time, json, sys, os, requests, socket, configparser, hashlib, webbrowser, threading
from tkinter import *
from tkinter.messagebox import *
from tkinter import ttk
from PIL import Image, ImageTk

import PrintScreen as PS
import Services as SV

Units = "°K"
STOP = False
BearerAUTH = ""

conf = configparser.ConfigParser()
conf.read("config.cfg")

if os.path.exists('/etc/default/epd-fuse'):
	from papirus import PapirusTextPos
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
						PS.Crypto(conf, TextPAPIRUS)
					if conf["WEATHER"]["MeteoAPI"] != "":
						PS.Meteo(conf, TextPAPIRUS, Units)
					if conf["LASTFM"]["LastFmAPI"] != "":
						PS.Musique(conf, TextPAPIRUS)
					if conf["TWITCH"]["TwitchAPI"] != "":
						PS.Twitch(conf, TextPAPIRUS)
					if conf["TWITTER"]["TwitterAPI"] != "" and conf["TWITTER"]["twitterapisecret"] != "":
						PS.Twitter(conf, TextPAPIRUS, BearerAUTH)
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
		Check = 0

		#Test des APIs
		try:
			if conf["WEATHER"]["MeteoAPI"] != "":
				SV.SVMeteo(conf)
				if 400 <= int(SV.DataMeteo["cod"]) <= 599: 
						ERROR = "Erreur dans la config Météo, veuillez vérifier votre saisie!"
						ErrorConfig(ERROR)
						return
				else:
					Check += 1
			else:
				Check += 1

			if conf["CRYPTO"]["CryptoAPI"] != "":
				SV.SVCrypto(conf)
				try:
					if SV.DataCrypto["Response"] == "Error":
						ERROR = "Erreur dans la config Crypto, veuillez vérifier votre saisie!"
						ErrorConfig(ERROR)
						return
				except KeyError:
					Check += 1
			else:
				Check += 1

			if conf["LASTFM"]["LastFmAPI"] != "":
				SV.SVMusique(conf)
				try:
					if 2 <= int(SV.DataLast["error"]) <= 29:
						ERROR = "Erreur dans la config LastFM, veuillez vérifier votre saisie!"
						ErrorConfig(ERROR)
						return
				except KeyError:
					Check += 1
			else:
				Check += 1

			if conf["TWITTER"]["TwitterAPI"] != "" and conf["TWITTER"]["twitterapisecret"] != "":
				try:
					BearerRAW = os.popen("curl -u '"+ conf["TWITTER"]["TwitterAPI"] + ":" + conf["TWITTER"]["TwitterAPISecret"] + "' --data 'grant_type=client_credentials' 'https://api.twitter.com/oauth2/token'").read()
					BearerJSON = json.loads(BearerRAW)
					BearerAUTH = BearerJSON["access_token"]
				except KeyError:
					ERROR = "Erreur dans la config Twitter, il faut 2 clés API! Veuillez vérifier votre saisie!"
					ErrorConfig(ERROR)
					return
				finally:
					try:
						SV.SVTwitter(conf, BearerAUTH)
						if 49 <= int(SV.DataTwitter["errors"][0]["code"]) <= 599:
							ERROR = "Erreur dans la config Twitter, veuillez vérifier votre saisie!"
							ErrorConfig(ERROR)
							return
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
