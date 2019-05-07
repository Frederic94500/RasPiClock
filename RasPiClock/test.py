# -*- encoding: utf-8 -*-
#Frédéric94500 - Résistance-ISN

from tkinter import *
from tkinter import ttk
import webbrowser
from tkinter.messagebox import *
from PIL import Image, ImageTk


#def Afficher():

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

	photo = ImageTk.PhotoImage(Image.open("gpl.png"))
	img = Label(About, image=photo)
	img.image = photo
	img.pack()

	About.iconbitmap('icon.ico')

#Création Fenètre
Fenetre = Tk()
Fenetre.title('GUI')
'''Fenetre.iconbitmap('icon.ico')'''



#Création barre de menu
menubar = Menu(Fenetre)

filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label = "Fichier", menu = filemenu)
filemenu.add_command(label = "Quitter", command = Fenetre.destroy)
Actif = IntVar()
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
tab_parent = ttk.Notebook(Fenetre)
tabCrypto = ttk.Frame(tab_parent)
tabMeteo = ttk.Frame(tab_parent)
tabMusic = ttk.Frame(tab_parent)
tabTwitch = ttk.Frame(tab_parent)
tabTwitter = ttk.Frame(tab_parent)
tab_parent.add(tabCrypto, text="Crypto")
tab_parent.add(tabMeteo, text="Météo")
tab_parent.add(tabMusic, text="Music")
tab_parent.add(tabTwitch, text="Twitch")
tab_parent.add(tabTwitter, text="Twitter")
tab_parent.pack(expand=1, fill='both')

#Création Grid
Label(tabCrypto, text="First").grid(row=0)
Label(tabCrypto, text="Second").grid(row=1)
Label(tabMeteo, text="First").grid(row=0)
Label(tabMeteo, text="Second").grid(row=1)
Label(tabMusic, text="First").grid(row=0)
Label(tabMusic, text="Second").grid(row=1)
Label(tabTwitch, text="First").grid(row=0)
Label(tabTwitch, text="Second").grid(row=1)
Label(tabTwitter, text="First").grid(row=0)
Label(tabTwitter, text="Second").grid(row=1)

e1 = Entry(tabCrypto)
e2 = Entry(tabCrypto)

e3 = Entry(tabMeteo)
e4 = Entry(tabMeteo)

e5 = Entry(tabMusic)
e6 = Entry(tabMusic)

e7 = Entry(tabTwitch)
e8 = Entry(tabTwitch)

e9 = Entry(tabTwitter)
e10 = Entry(tabTwitter)


e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=0, column=1)
e4.grid(row=1, column=1)
e5.grid(row=0, column=1)
e6.grid(row=1, column=1)
e7.grid(row=0, column=1)
e8.grid(row=1, column=1)
e9.grid(row=0, column=1)
e10.grid(row=1, column=1)

#Initialisation du GUI
Fenetre.mainloop()
