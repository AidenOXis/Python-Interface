import tkinter as tk
from tkinter import ttk

class IsulinometroApp(tk.Tk):

    def __init__(self):
        super().__init__()

        #Size iniziale
        self.geometry("800x400")

        #Titolo finestra
        self.title("Insulinometro")

        self.create_widgets()

    def create_widgets(self):
        #Definizione griglia
        #3 colonne a larghezza variabile
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        #Prime 2 righe ad altezza fissa
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, minsize=70, weight=0)
        self.rowconfigure(3, weight=0)
        #1 riga ad altezza fissa
        self.rowconfigure(4, weight=0)
        #1 righe ad altezza variabile
        self.rowconfigure(5, weight=1)
        #1 riga ad altezza fissa
        self.rowconfigure(6, weight=0)
        
        #Tab
        tab=tk.Frame(self, height=60, bg="black")
        tab.grid(column=0, row=0, columnspan=3, rowspan=1, padx=10, pady=2, sticky="nesw")

        #Frame Bluetooth
        bluetooth=tk.Frame(self, bg="blue")
        bluetooth.grid(column=0, row=1, columnspan=1, rowspan=2,padx=10, pady=2, sticky="nesw" )

        #Frame Batteria
        batteria=tk.Frame(self, height=40,  bg="green")
        batteria.grid(column=0, row=3, columnspan=1, rowspan=1,padx=10, pady=2, sticky="nesw" )

        #TestoDatiSalvati
        testo1=tk.Label(self, text="SAVED DATA", bg="lightgrey")
        testo1.grid(column=0, row=4, columnspan=1, rowspan=1, padx=10, pady=2, sticky="nesw" )

        #Frame Dati Salvati
        salvataggi=tk.Frame(self, bg="grey")
        salvataggi.grid(column=0, row=5, columnspan=1, rowspan=2, padx=10, pady=2, sticky="nesw" )

        #Tab modalità frequenziale
        tab2=tk.Frame(self, height=30, bg="black")
        tab2.grid(column=1, row=1, columnspan=2, rowspan=1, padx=10, pady=2, sticky="nesw")

        #Frame dati input
        input=tk.Frame(self, bg="orange")
        input.grid(column=1, row=2, columnspan=2, rowspan=4, padx=10, pady=2, sticky="nesw")

        #Bottone Start
        start=tk.Button(self, text="START", height= 5, width=2, command=self.start_button_click)
        start.grid(column=1, row=6, columnspan=1, rowspan=1, padx=10, pady=2, sticky="nesw")

        #Bottone Exit
        exit=tk.Button(self, text="EXIT", height= 8, width=2, command=self.exit_button_click)
        exit.grid(column=2, row=6, columnspan=1, rowspan=1, padx=10, pady=2, sticky="nesw")
        
                   
    def start_button_click(self):
         pass
        
    def exit_button_click(self):
         pass


        



if __name__ == "__main__":
    app = IsulinometroApp()
    app.mainloop()
