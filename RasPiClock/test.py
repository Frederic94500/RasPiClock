# -*- encoding: utf-8 -*-
#Frédéric94500 - Résistance-ISN

from tkinter import *
from tkinter import ttk
import webbrowser
from tkinter.messagebox import *
from PIL import Image, ImageTk

#Fonction "Quand on appuie sur "enter""
def Enter(event):
    Afficher()

def WebProj():
	webbrowser.open_new_tab('https://github.com/Frederic94500/Resistance-ISN')

def WebAuteur(event):
	webbrowser.open_new_tab('https://twitter.com/Frederic94500')

def WebLicence(event):
	webbrowser.open_new_tab('https://github.com/Frederic94500/Resistance-ISN/blob/master/LICENSE')

#Fonction à propos (créateur + licence)(ouvre une nouvelle fenêtre)
def APropos():
	About = Toplevel()
	About.title("A propos et licence")

	AbText = [0, 1, 2, 3]

	AbText[0] = Label(About, text = "Ce programme a été fait par")
	AbText[1] = Label(About, text = "Frédéric94500, Eliott et Parsa", fg = "blue", cursor = "hand2")
	AbText[2] = Label(About, text = "sous la licence")
	AbText[3] = Label(About, text = "GPL-3.0", fg = "blue", cursor = "hand2")

	AbText[1].bind("<Button-1>", WebAuteur)
	AbText[3].bind("<Button-1>", WebLicence)

	[AbText[I].pack(side = "left", pady = 10) for I in range(4)]

	'''photo = ImageTk.PhotoImage(Image.open("gpl.png"))
	img = Label(About, image=photo)
	img.image = photo
	img.pack()

	About.iconbitmap('icon.ico')'''

#Création Fenètre
Fenetre = Tk()
Fenetre.title('GUI')
'''Fenetre.iconbitmap('icon.ico')'''

#Création barre de menu
menubar = Menu(Fenetre)

filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label = "Fichier", menu = filemenu)
filemenu.add_command(label = "Quitter", command = Fenetre.destroy)

editmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label = "Edition", menu = editmenu)

helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label = "Aide", menu = helpmenu)
helpmenu.add_command(label = "Vistez le GitHub", command = WebProj)
helpmenu.add_separator()
helpmenu.add_command(label = "A propos et licence", command = APropos)

Fenetre.config(menu=menubar)

#Création Bouton Afficher
#BoutonAfficher = Button(Fenetre, text = 'Afficher', command = Verification).pack(side = LEFT, padx = 5, pady = 5)

'''#Création Zone de Texte
ZoneTexte = Entry(justify = CENTER)
ZoneTexte.focus_set()
ZoneTexte.pack(side = LEFT, fill = BOTH, padx = 5, pady = 5)'''

#Quand on appuie sur "enter"
Fenetre.bind('<Return>', Enter)

#Création Texte et Texte Annonce
Texte = StringVar()
TextAnnonce = Label(Fenetre, textvariable = Texte).pack(side = LEFT)
Texte.set("")

#Création onglets
TABList = ["tabCrypto", "tabMeteo", "tabMusic", "tabTwitch", "tabTwitter"]
TABText = ["Crypto", "Météo", "Musique", "Twitch", "Twitter"]
NBArg = [4, 4, 2, 3, 2]
TEXTEntry = []

TAB = ttk.Notebook(Fenetre)

for I in range(5):
	TABList[I] = ttk.Frame(TAB)
	TAB.add(TABList[I], text=TABText[I])

TAB.pack(expand=1, fill='both')

#Création Grid

for I0 in range(5): #Nombre de tab
	for I1 in range(2): #Nombre de ligne en fonction du tab
		for I2 in range(2): #Nombre d'argument 
			Label(TABList[I0], text="First").grid(row=I2, padx=5, pady=5)
			e1 = Entry(TABList[I0]).grid(row=I2, column=1, padx=5, pady=5)

#Initialisation du GUI
Fenetre.mainloop()
