import json
import os

# full path of the dictionary file on disk
DICTIONARY_FILE  = '/home/mario/bExp_Selections/Sel_dictionary.json'

# --------------------------------------------------------------------------------------
def save_dictionary(dictionary):
    try:
        with open(DICTIONARY_FILE, "w", encoding="utf-8") as f:
            # indent=4 rende il file JSON facilmente leggibile anche da un essere umano
            json.dump(dictionary, f, indent=4, ensure_ascii=False)
        # print("Dizionario salvato con successo su disco!")
        return True
    except Exception as e:
        # print(f"Errore durante il salvataggio: {e}")
        return False

# ----------------------------------------------------------------------------------------
def Load_dictionary():
    # Se il file non esiste ancora (es. al primissimo avvio), restituiamo un dictionary di default
    if not os.path.exists(DICTIONARY_FILE):
        # print("File di configurazione non trovato. Carico il dictionary di default.")
        dizionario_default = {
            "Vitto": "/home/tuo_utente/Documenti/Spese/Transact_Vitto.db",
            "Viaggi": "/home/tuo_utente/Documenti/Spese/Transact_Viaggi.db",
            "Vacanze": "/home/tuo_utente/Documenti/Spese/Transact_Vacanze.db",
        }
        # Lo salviamo subito così il file viene creato
        save_dictionary(dizionario_default)
        return dizionario_default

    try:
        with open(DICTIONARY_FILE, "r", encoding="utf-8") as f:
            ditcionary = json.load(f)
        # print("Dizionario caricato correttamente dal disco!")
        return ditcionary
    except Exception as e:
        print(f"Errore durante la lettura del file: {e}")
        return {}

# ------------------------------------------------------------------------------
mydictionary = Load_dictionary()
if mydictionary == {}:
    print("ERROR")
else:
    print(mydictionary["Vitto"])
    print(mydictionary["Viaggi"])
    print(mydictionary["Vacanze"])
    pass

    mydictionary["Vitto"] = 'vitto'
    mydictionary["Viaggi"] = 'Viaggi'
    mydictionary["Vacanze"] = 'Vacanze'
    if save_dictionary(mydictionary):
        mydictionary = Load_dictionary()
        print(mydictionary["Vitto"])
        print(mydictionary["Viaggi"])
        print(mydictionary["Vacanze"])
        pass


# ========================================================================================

# import tkinter
# class theUI():
# 	def __init__(self):
# 		self.root = tkinter.Tk()
# 		self.root.geometry("500x600")
# 		self.mainframe = tkinter.Frame(self.root, height=300,  width=400, bg="green")
# 		self.mainframe.pack(side="left")
#
# 		tkinter.Button(master=self.mainframe, text="e vaiii", command=self.Clk_Test).pack(side="left")
# 		self.root.mainloop()
#
# 	def Clk_Test(self):
# 		print("HO CLICCATO!!!!")
#
# Test = theUI()

# class theUI():
# 	def __init__(self):
# 		self.root = tkinter.Tk()
# 		self.root.geometry("500x600")
# 		self.maincanvas = tkinter.Canvas(self.root, height=300,  width=400, selectforeground="white", bg="skyblue")
# 		self.maincanvas.pack(side="left")
#
# 		self.Btn = tkinter.Button(master=self.maincanvas, text="e vaiii", command=self.Clk_Test)
# 		self.Btn.place(x=100, y=200)
# 		self.root.mainloop()
#
# 	def Clk_Test(self):
# 		print("HO CLICCATO!!!!")
#
# Test = theUI()

# Python Program to make a scrollable frame
# using Tkinter

"""
from tkinter import *

class ScrollBar:

	# constructor
	def __init__(self):
		# create root window
		root = Tk()

		# create a horizontal scrollbar by
		# setting orient to horizontal
		h = Scrollbar(root, orient='horizontal')

		# attach Scrollbar to root window at
		# the bootom
		h.pack(side=BOTTOM, fill=X)

		# create a vertical scrollbar-no need
		# to write orient as it is by
		# default vertical
		v = Scrollbar(root)

		# attach Scrollbar to root window on
		# the side
		v.pack(side=RIGHT, fill=Y)

		# create a Text widget with 15 chars
		# width and 15 lines height
		# here xscrollcomannd is used to attach Text
		# widget to the horizontal scrollbar
		# here yscrollcomannd is used to attach Text
		# widget to the vertical scrollbar
		t = Text(root, width=25, height=15, wrap=NONE,
				 xscrollcommand=h.set,
				 yscrollcommand=v.set)

		# insert some text into the text widget
		for i in range(20):
			t.insert(END, "this is some text 12345678901234567890\n")

		# attach Text widget to root window at top
		t.pack(side=TOP, fill=X)

		# here command represents the method to
		# be executed xview is executed on
		# object 't' Here t may represent any
		# widget
		h.config(command=t.xview)

		# here command represents the method to
		# be executed yview is executed on
		# object 't' Here t may represent any
		# widget
		v.config(command=t.yview)

		# the root window handles the mouse
		# click event
		root.mainloop()


# create an object to Scrollbar class
s = ScrollBar()
"""