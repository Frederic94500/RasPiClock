# -*- encoding: utf-8 -*-
#Frédéric94500 - RasPiClock GUI Mode TEST - Pris du programme Résistance-ISN

import time, json, sys, os, socket, configparser, hashlib, webbrowser
import requests as rq
from tkinter import *
from tkinter.messagebox import *
from tkinter import ttk
from PIL import Image, ImageTk
import threading

conf = configparser.ConfigParser()
conf.read("config.cfg")

#Fonction "Quand on appuie sur "enter""
def Enter(event):
	Afficher()

def Afficher():
	global BoutonAfficher
	global BoutonArreter

	BoutonAfficher.configure(state=DISABLED)
	BoutonArreter.configure(state=NORMAL)

	global STOP
	STOP = False
	threadRas = threading.Thread(target=test)
	threadRas.start()


def test():
	while True:
		global STOP
		if STOP:
			break;
		else:
			print("HEHEHEH") 
			time.sleep(2)
		
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
