import tkinter as tk

class IsulinometroApp(tk.Tk):

    def __init__(self):
        super().__init__()

        # Imposta la geometria della finestra
        self.geometry("800x400")

        # Permette il ridimensionamento della finestra
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Titolo finestra
        self.title("Insulinometro")

        # Inizializzazione di due frame per le modalità Home e Data
        self.home_frame = tk.Frame(self)
        self.data_frame = tk.Frame(self)
        self.help_frame = tk.Frame(self)  # Aggiunto frame Help

        # Chiamata per la creazione dei widget nei due frame
        self.create_home_frame()
        self.create_data_frame()
        self.create_help_frame()  # Aggiunta chiamata per creare il frame Help

        # Imposta il layout del frame principale
        for frame in (self.home_frame, self.data_frame, self.help_frame):
            frame.grid(row=0, column=0, sticky='nsew')

        # Mostra il frame "home" inizialmente
        self.show_frame(self.home_frame)

    def create_home_frame(self):
        # Configura layout del frame "home"
        self.home_frame.columnconfigure(0, weight=1)
        self.home_frame.columnconfigure(1, weight=1)
        self.home_frame.columnconfigure(2, weight=1)
        self.home_frame.rowconfigure(0, weight=0)
        self.home_frame.rowconfigure(1, weight=1)
        self.home_frame.rowconfigure(2, weight=1)
        self.home_frame.rowconfigure(3, weight=1)
        self.home_frame.rowconfigure(4, weight=1)
        self.home_frame.rowconfigure(5, weight=1)
        self.home_frame.rowconfigure(6, weight=0)

        # Tab per cambiare modalità
        tab = tk.Frame(self.home_frame, height=60, bg="white")
        tab.grid(column=0, row=0, columnspan=3, rowspan=1, padx=10, pady=2, sticky="nesw")

        # Aggiungo configurazione del layout del tab per ridimensionamento
        tab.columnconfigure(0, weight=1)
        tab.columnconfigure(1, weight=1)
        tab.columnconfigure(2, weight=1)  # Aggiunto per il pulsante Help

        # Aggiunta pulsanti switch modalità
        btn_home = tk.Button(tab, text="Home", command=lambda: self.show_frame(self.home_frame), height=2, width=10)
        btn_home.grid(column=0, row=0, sticky="nesw", padx=10, pady=2)

        btn_data = tk.Button(tab, text="Data", command=lambda: self.show_frame(self.data_frame), height=2, width=10)
        btn_data.grid(column=1, row=0, sticky="nesw", padx=10, pady=2)

        # Aggiunta pulsante Help
        btn_help = tk.Button(tab, text="Help", command=lambda: self.show_frame(self.help_frame), height=2, width=10)
        btn_help.grid(column=2, row=0, sticky="nesw", padx=10, pady=2)

        # Frame Bluetooth
        bluetooth = tk.Frame(self.home_frame, bg="blue")
        bluetooth.grid(column=0, row=1, columnspan=1, rowspan=2, padx=10, pady=2, sticky="nesw")

        # Frame Batteria
        batteria = tk.Frame(self.home_frame, height=40, bg="green")
        batteria.grid(column=0, row=3, columnspan=1, rowspan=1, padx=10, pady=2, sticky="nesw")

        # Testo Dati Salvati
        testo1 = tk.Label(self.home_frame, text="SAVED DATA", bg="lightgrey")
        testo1.grid(column=0, row=4, columnspan=1, rowspan=1, padx=10, pady=2, sticky="nesw")

        # Frame Dati Salvati
        salvataggi = tk.Frame(self.home_frame, bg="grey")
        salvataggi.grid(column=0, row=5, columnspan=1, rowspan=2, padx=10, pady=2, sticky="nesw")

        # Tab modalità frequenziale
        tab2 = tk.Frame(self.home_frame, height=30, bg="white")
        tab2.grid(column=1, row=1, columnspan=2, rowspan=1, padx=10, pady=2, sticky="nesw")
        frequenzasingola=tk.Button(self.home_frame,text="Frequenza singola",bg="purple", height=5, width=5)
        frequenzasingola.grid(column=1, row=1, columnspan=1, rowspan=1, padx=10, pady=2, sticky="nesw")
        sweepmode=tk.Button(self.home_frame,text="Sweep mode",bg="Green", height=5, width=5)
        sweepmode.grid(column=2, row=1, columnspan=1, rowspan=1, padx=10, pady=2, sticky="nesw")
        
      

        # Configura layout del tab2 per ridimensionamento
        tab2.columnconfigure(0, weight=1)
        tab2.columnconfigure(1, weight=1)

        # Frame dati input
        input_frame = tk.Frame(self.home_frame, bg="orange")
        input_frame.grid(column=1, row=2, columnspan=2, rowspan=4, padx=10, pady=2, sticky="nesw")

        # Bottone Start
        start = tk.Button(self.home_frame, text="START", height=5, width=2, command=self.start_button_click)
        start.grid(column=1, row=6, columnspan=1, rowspan=1, padx=10, pady=2, sticky="nesw")

        # Bottone Exit
        exit_button = tk.Button(self.home_frame, text="EXIT", height=8, width=2, command=self.exit_button_click)
        exit_button.grid(column=2, row=6, columnspan=1, rowspan=1, padx=10, pady=2, sticky="nesw")

    def create_data_frame(self):
        # Configura layout del frame "data"
        self.data_frame.columnconfigure(0, weight=1)
        self.data_frame.columnconfigure(1, weight=1)
        self.data_frame.columnconfigure(2, weight=1)
        self.data_frame.rowconfigure(0, weight=0)
        self.data_frame.rowconfigure(1, weight=1)
        self.data_frame.rowconfigure(2, minsize=70, weight=1)
        self.data_frame.rowconfigure(3, weight=1)
        self.data_frame.rowconfigure(4, weight=1)
        self.data_frame.rowconfigure(5, weight=1)
        self.data_frame.rowconfigure(6, weight=0)

        # Tab per cambiare modalità
        tab = tk.Frame(self.data_frame, height=60, bg="black")
        tab.grid(column=0, row=0, columnspan=3, rowspan=1, padx=10, pady=2, sticky="nesw")

        # Configura layout del tab per ridimensionamento
        tab.columnconfigure(0, weight=1)
        tab.columnconfigure(1, weight=1)
        tab.columnconfigure(2, weight=1)  # Aggiunto per il pulsante Help

        # Aggiunta pulsanti switch modalità
        btn_home = tk.Button(tab, text="Home", command=lambda: self.show_frame(self.home_frame), height=2, width=10)
        btn_home.grid(column=0, row=0, sticky="nesw", padx=10, pady=2)

        btn_data = tk.Button(tab, text="Data", command=lambda: self.show_frame(self.data_frame), height=2, width=10)
        btn_data.grid(column=1, row=0, sticky="nesw", padx=10, pady=2)

        # Aggiunta pulsante Help
        btn_help = tk.Button(tab, text="Help", command=lambda: self.show_frame(self.help_frame), height=2, width=10)
        btn_help.grid(column=2, row=0, sticky="nesw", padx=10, pady=2)

        # Bode Diagrams
        bode_frame = tk.Frame(self.data_frame, bg="white")
        bode_frame.grid(column=0, row=1, columnspan=3, rowspan=2, padx=10, pady=2, sticky="nesw")

        # Nyquist Diagram
        nyquist_frame = tk.Frame(self.data_frame, bg="white")
        nyquist_frame.grid(column=0, row=3, columnspan=3, rowspan=2, padx=10, pady=2, sticky="nesw")

        # Activity Log
        activity_log = tk.Frame(self.data_frame, bg="grey")
        activity_log.grid(column=0, row=5, columnspan=3, rowspan=1, padx=10, pady=2, sticky="nesw")

        # Bottoni sotto i grafici
        reset_button = tk.Button(self.data_frame, text="RESET BUFFER", bg="purple", height=2, width=15)
        reset_button.grid(column=0, row=6, padx=5, pady=5)
        stop_button = tk.Button(self.data_frame, text="STOP", bg="red", height=2, width=15)
        stop_button.grid(column=1, row=6, padx=5, pady=5)
        save_button = tk.Button(self.data_frame, text="SAVE DATA", bg="lightblue", height=2, width=15)
        save_button.grid(column=2, row=6, padx=5, pady=5)

    def create_help_frame(self):
        """ Creazione del frame Help """
        self.help_frame.columnconfigure(0, weight=1)
        self.help_frame.rowconfigure(0, weight=1)

        help_label = tk.Label(self.help_frame, text="Help Section: qui si trova il testo di aiuto", bg="lightyellow")
        help_label.grid(column=0, row=0, padx=20, pady=20, sticky="nesw")

    def show_frame(self, frame):
        """ Mostra il frame selezionato """
        frame.tkraise()

    def start_button_click(self):
        pass

    def exit_button_click(self):
        self.quit()


if __name__ == "__main__":
    app = IsulinometroApp()
    app.mainloop()
