import tkinter as tk

class IsulinometroApp(tk.Tk):

    def __init__(self):
        super().__init__()

        # Imposta la geometria della finestra
        self.geometry("800x400")

        self.wm_minsize(600, 300)  # Set minimum window size (600x300)

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
        self.home_frame.rowconfigure(1, weight=0)
        self.home_frame.rowconfigure(2, weight=0)
        self.home_frame.rowconfigure(2, minsize=50) 
        self.home_frame.rowconfigure(3, weight=0)
        self.home_frame.rowconfigure(3, minsize=50) 
        self.home_frame.rowconfigure(4, weight=0)
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
        btn_home = tk.Button(tab, text="Home", command=lambda: self.show_frame(self.home_frame), height=2, width=10, bg= "gray")
        btn_home.grid(column=0, row=0, sticky="nesw", padx=10, pady=2)

        btn_data = tk.Button(tab, text="Data", command=lambda: self.show_frame(self.data_frame), height=2, width=10)
        btn_data.grid(column=1, row=0, sticky="nesw", padx=10, pady=2)

        # Aggiunta pulsante Help
        btn_help = tk.Button(tab, text="Help", command=lambda: self.show_frame(self.help_frame), height=2, width=10)
        btn_help.grid(column=2, row=0, sticky="nesw", padx=10, pady=2)

        # Frame Bluetooth
        bluetooth = tk.Frame(self.home_frame, bg="blue")
        bluetooth.grid(column=0, row=1, columnspan=1, rowspan=2, padx=10, pady=2, sticky="nesw")

        # Testo Frame Bluetooth
        testo_frame_bluetooth = tk.Label(bluetooth, text="Frame Bluetooth", bg="blue", font=("Arial", 12))
        testo_frame_bluetooth.grid(column=0, row=1, columnspan=1, rowspan=1, padx=10, pady=2, sticky="nesw")

        # Frame Batteria
        batteria = tk.Frame(self.home_frame, height=40, bg="green")
        batteria.grid(column=0, row=3, columnspan=1, rowspan=1, padx=10, pady=2, sticky="nesw")

        # Testo Frame Batteria
        testo_frame_batteria = tk.Label(batteria, text="Frame Batteria", bg="green", font=("Arial", 12))
        testo_frame_batteria.grid(column=0, row=1, columnspan=1, rowspan=1, padx=10, pady=2, sticky="nesw")

        # Testo Dati Salvati
        testo1 = tk.Label(self.home_frame, text="SAVED DATA", bg="lightgrey")
        testo1.grid(column=0, row=4, columnspan=1, rowspan=1, padx=10, pady=2, sticky="nesw")

        # Frame Dati Salvati
        salvataggi = tk.Frame(self.home_frame, bg="grey")
        salvataggi.grid(column=0, row=5, columnspan=1, rowspan=2, padx=10, pady=2, sticky="nesw")

        # Testo Frame Dati Salvati
        testo_frame_saved_data = tk.Label(salvataggi, text="Frame dei dati salvati", bg="grey", font=("Arial", 12))
        testo_frame_saved_data.grid(column=0, row=5, columnspan=1, rowspan=1, padx=10, pady=2, sticky="nesw")

        # Tab modalità frequenziale
        #Funzioni dei due bottoni della tab
        def frequenzasingola_click():
            input_frame2.grid_forget()
            input_frame2_text.grid_forget()
            input_frame.grid(column=1, row=2, columnspan=2, rowspan=4, padx=10, pady=2, sticky="nesw")
            input_frame_text.grid(column=0, row=4, columnspan=1, rowspan=1, padx=10, pady=2, sticky="nesw")
        
        def sweepmode_click():
            input_frame.grid_forget()
            input_frame_text.grid_forget()
            input_frame2.grid(column=1, row=2, columnspan=2, rowspan=4, padx=10, pady=2, sticky="nesw")
            input_frame2_text.grid(column=0, row=4, columnspan=1, rowspan=1, padx=10, pady=2, sticky="nesw")

        tab2 = tk.Frame(self.home_frame, height=30, bg="white")
        tab2.grid(column=1, row=1, columnspan=2, rowspan=1, padx=10, pady=2, sticky="nesw")
        frequenzasingola=tk.Button(self.home_frame,text="Frequenza singola",bg="purple", height=2, width=5, command=frequenzasingola_click)
        frequenzasingola.grid(column=1, row=1, columnspan=1, rowspan=1, padx=10, pady=2, sticky="nesw")
        sweepmode=tk.Button(self.home_frame,text="Sweep mode",bg="Green", height=2, width=5, command=sweepmode_click)
        sweepmode.grid(column=2, row=1, columnspan=1, rowspan=1, padx=10, pady=2, sticky="nesw")
        
        # Configura layout del tab2 per ridimensionamento
        tab2.columnconfigure(0, weight=1)
        tab2.columnconfigure(1, weight=1)

        # Frame dati input modalità singola
        input_frame = tk.Frame(self.home_frame, bg="orange")
        input_frame.grid(column=1, row=2, columnspan=2, rowspan=4, padx=10, pady=2, sticky="nesw")

        # Testo Input modaltà singola
        input_frame_text = tk.Label(input_frame, text="Frame di Input modalità singola", bg="orange", font=("Arial", 12))
        input_frame_text.grid(column=0, row=4, columnspan=1, rowspan=1, padx=10, pady=2, sticky="nesw")
        
        # Frame dati input modalità sweep
        input_frame2 = tk.Frame(self.home_frame, bg="orange")
        
        # Testo Input modalità sweep
        input_frame2_text = tk.Label(input_frame2, text="Frame di Input modalità sweep", bg="orange", font=("Arial", 12))


        # Bottone Start
        start = tk.Button(self.home_frame, text="START", height=3, width=2, command=self.start_button_click)
        start.grid(column=1, row=6, columnspan=1, rowspan=1, padx=10, pady=2, sticky="nesw")

        # Bottone Exit
        exit_button = tk.Button(self.home_frame, text="EXIT", height=3, width=2, command=self.exit_button_click)
        exit_button.grid(column=2, row=6, columnspan=1, rowspan=1, padx=10, pady=2, sticky="nesw")

    def create_data_frame(self):

        # Configure layout for the "data" frame
        self.data_frame.columnconfigure(0, weight=1)
        self.data_frame.columnconfigure(1, weight=1)
        self.data_frame.rowconfigure(0, weight=0)  # Row for the tab
        #self.data_frame.rowconfigure(1, weight=1)  # Row for the main content
        self.data_frame.rowconfigure(1, minsize=20)
        self.data_frame.rowconfigure(2, weight=3)
        self.data_frame.rowconfigure(3, weight=3)
        self.data_frame.rowconfigure(4, minsize=50) 
        #self.data_frame.rowconfigure(4, weight=1)
        self.data_frame.rowconfigure(5, weight=1)  # Assign weight to the row for the activity log

        # Tab for mode switching (unchanged)
        tab = tk.Frame(self.data_frame, height=60, bg="white")
        tab.grid(column=0, row=0, columnspan=2, padx=10, pady=2, sticky="nesw")

        # Configure tab layout for resizing
        tab.columnconfigure(0, weight=1)
        tab.columnconfigure(1, weight=1)
        tab.columnconfigure(2, weight=1)  # Added for Help button

        # Add buttons for mode switching
        btn_home = tk.Button(tab, text="Home", command=lambda: self.show_frame(self.home_frame), height=2, width=10)
        btn_home.grid(column=0, row=0, sticky="nesw", padx=10, pady=2)

        btn_data = tk.Button(tab, text="Data", command=lambda: self.show_frame(self.data_frame), height=2, width=10, bg= "gray")
        btn_data.grid(column=1, row=0, sticky="nesw", padx=10, pady=2)

        btn_help = tk.Button(tab, text="Help", command=lambda: self.show_frame(self.help_frame), height=2, width=10)
        btn_help.grid(column=2, row=0, sticky="nesw", padx=10, pady=2)

        # Adding text below buttons in the lower left frame
        graph1_text_label = tk.Label(self.data_frame, text="Rappresentazione in diagramma di Bode", font=("Arial", 12))
        graph1_text_label.grid(column=0, row=1, columnspan=1, padx=10, pady=2, sticky="nsew")

        # Adding text below buttons in the lower left frame
        graph2_text_label = tk.Label(self.data_frame, text="Rappresentazione in diagramma di Nyquist", font=("Arial", 12))
        graph2_text_label.grid(column=1, row=1, columnspan=1, padx=10, pady=2, sticky="nsew")

        # Left Column (3 frames)
        # Upper Frame
        upper_left_frame = tk.Frame(self.data_frame, bg="cyan")
        upper_left_frame.grid(column=0, row=2, padx=10, pady=2, sticky="nesw")
        upper_left_frame.rowconfigure(0, weight=1)
        upper_left_frame.columnconfigure(0, weight=1)

        # Adding text to the upper left frame
        upper_left_label = tk.Label(upper_left_frame, text="Diagramma di Bode, Modulo", bg="cyan", font=("Arial", 14))
        upper_left_label.grid(column=0, row=0, padx=10, pady=10)

        # Middle Frame
        middle_left_frame = tk.Frame(self.data_frame, bg="cyan")
        middle_left_frame.grid(column=0, row=3, padx=10, pady=2, sticky="nesw")
        middle_left_frame.rowconfigure(0, weight=1)
        middle_left_frame.columnconfigure(0, weight=1)

        # Adding text to the middle left frame
        middle_left_label = tk.Label(middle_left_frame, text="Diagramma di Bode, Fase", bg="cyan", font=("Arial", 14))
        middle_left_label.grid(column=0, row=0, padx=10, pady=10)

        # Lower Frame with buttons
        lower_left_frame = tk.Frame(self.data_frame, bg="cyan")
        lower_left_frame.grid(column=0, row=4, padx=10, pady=2, sticky="nesw")
        lower_left_frame.columnconfigure(0, weight=1)
        lower_left_frame.columnconfigure(1, weight=1)
        lower_left_frame.rowconfigure(0, weight=1)
        lower_left_frame.rowconfigure(1, weight=1)

        # Buttons inside the lower left frame
        reset_button = tk.Button(lower_left_frame, text="RESET", bg="purple", height=2, width=5)
        reset_button.grid(column=0, row=0, padx=5, pady=5, sticky="nesw")
        
        stop_button = tk.Button(lower_left_frame, text="STOP", bg="red", height=2, width=5)
        stop_button.grid(column=1, row=0, padx=5, pady=5, sticky="nesw")

        add_marker_button = tk.Button(lower_left_frame, text="ADD MARKER", bg="lightgreen", height=2, width=5)
        add_marker_button.grid(column=0, row=1, padx=5, pady=5, sticky="nesw")

        save_button = tk.Button(lower_left_frame, text="SAVE", bg="lightblue", height=2, width=5)
        save_button.grid(column=1, row=1, padx=5, pady=5, sticky="nesw")

        # Right Column (2 frames)
        # Top frame (same height as the two frames on the left)
        top_right_frame = tk.Frame(self.data_frame, bg="green")
        top_right_frame.grid(column=1, row=2, rowspan=2, padx=10, pady=2, sticky="nesw")  # rowspan=3 to span three rows
        top_right_frame.rowconfigure(0, weight=1)
        top_right_frame.columnconfigure(0, weight=1)

        # Adding text to the top right frame
        top_right_label = tk.Label(top_right_frame, text="Diagramma di Nyquist", bg="green", font=("Arial", 14))
        top_right_label.grid(column=0, row=0, padx=10, pady=10)

        # Bottom frame
        bottom_right_frame = tk.Frame(self.data_frame, bg="yellow")
        bottom_right_frame.grid(column=1, row=4, padx=10, pady=2, sticky="nesw")
        bottom_right_frame.rowconfigure(0, weight=1)
        bottom_right_frame.columnconfigure(0, weight=1)

        # Adding text to the bottom right frame
        bottom_right_label = tk.Label(bottom_right_frame, text="Dati e markers", bg="yellow", font=("Arial", 14))
        bottom_right_label.grid(column=0, row=0, padx=10, pady=10)

        # Activity Log at the bottom (spans across both columns)
        activity_log = tk.Frame(self.data_frame, bg="grey")
        activity_log.grid(column=0, row=5, columnspan=2, padx=10, pady=2, sticky="nesw")

        # Adding text to the activity log
        activity_log_label = tk.Label(activity_log, text="Activity Log", bg="grey", font=("Arial", 14))
        activity_log_label.grid(column=0, row=0, padx=10, pady=10)

        # Allow the bottom activity log to stretch
        activity_log.rowconfigure(0, weight=1)
        activity_log.columnconfigure(0, weight=1)

    def create_help_frame(self):
        """ Creazione del frame Help """
        self.help_frame.columnconfigure(0, weight=1)
        self.help_frame.columnconfigure(1, weight=1)
        self.help_frame.columnconfigure(2, weight=1)
        self.help_frame.rowconfigure(0, weight=0)
        self.help_frame.rowconfigure(1, weight=1)

        # Tab per cambiare modalità (stesso layout degli altri frame)
        tab = tk.Frame(self.help_frame, height=60, bg="white")
        tab.grid(column=0, row=0, columnspan=3, rowspan=1, padx=10, pady=2, sticky="nesw")

        # Aggiungo configurazione del layout del tab per ridimensionamento
        tab.columnconfigure(0, weight=1)
        tab.columnconfigure(1, weight=1)
        tab.columnconfigure(2, weight=1)  # Aggiunto per il pulsante Help

        # Aggiunta pulsanti switch modalità (Home, Data, Help)
        btn_home = tk.Button(tab, text="Home", command=lambda: self.show_frame(self.home_frame), height=2, width=10)
        btn_home.grid(column=0, row=0, sticky="nesw", padx=10, pady=2)

        btn_data = tk.Button(tab, text="Data", command=lambda: self.show_frame(self.data_frame), height=2, width=10)
        btn_data.grid(column=1, row=0, sticky="nesw", padx=10, pady=2)

        btn_help = tk.Button(tab, text="Help", command=lambda: self.show_frame(self.help_frame), height=2, width=10, bg= "gray")
        btn_help.grid(column=2, row=0, sticky="nesw", padx=10, pady=2)

        # Testo Help
        help_label = tk.Label(self.help_frame, text="Help Section: qui si trova il testo di aiuto", bg="lightyellow")
        help_label.grid(column=0, row=1, columnspan=3, padx=20, pady=20, sticky="nesw")


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