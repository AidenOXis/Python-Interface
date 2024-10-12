import tkinter as tk

class IsulinometroApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.mode=None
    
        #Variabili per i campi di input
        self.voltage_str = tk.StringVar()
        self.frequency_str = tk.StringVar()
        self.min_frequency_str = tk.StringVar() 
        self.max_frequency_str = tk.StringVar()
        self.numberRepetitions_str=tk.StringVar()  
       
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
            self.grid_rowconfigure(0, weight=1)  # Distribuisce il peso tra le righe
            self.grid_columnconfigure(0, weight=1)  # Distribuisce il peso tra le colonne

        # Mostra il frame "home" inizialmente
        self.show_frame(self.home_frame)

    def create_home_frame(self):

        self.grid_propagate(False)
        # Configura layout del frame "home"

        #Calcola la larghezza della prima colonna come il 33% della larghezza totale del frame
        def resize(event):
            col_width = int(event.width * 0.33)
            self.home_frame.columnconfigure(0, minsize=col_width)

        #Associa l'evento di ridimensionamento del frame alla funzione resize così che si aggiorni ogni volta che mmodifico la grandezza della finestra
        self.home_frame.bind("<Configure>", resize)

        self.home_frame.columnconfigure(1, weight=1)
        self.home_frame.columnconfigure(2, weight=1)
        self.home_frame.rowconfigure(0, weight=0)
        self.home_frame.rowconfigure(1, weight=0)
        self.home_frame.rowconfigure(2, weight=0)
        self.home_frame.rowconfigure(2, minsize=50) 
        self.home_frame.rowconfigure(3, weight=0)
        self.home_frame.rowconfigure(3, minsize=50) 
        self.home_frame.rowconfigure(4, weight=0)
        self.home_frame.rowconfigure(5, weight=4)
        self.home_frame.rowconfigure(6, weight=1)

        # Tab per cambiare modalità
        tab = tk.Frame(self.home_frame, height=60, bg="white")
        tab.grid(column=0, row=0, columnspan=3, rowspan=1, padx=10, pady=2, sticky="nesw")

        # Aggiungo configurazione del layout del tab per ridimensionamento
        tab.columnconfigure(0, weight=1)
        tab.columnconfigure(1, weight=1)
        tab.columnconfigure(2, weight=1)  # Aggiunto per il pulsante Help

        # Aggiunta pulsanti switch modalità
        btn_home = tk.Button(tab, text="Home", command=self.home_button_click, height=2, width=10, bg= "gray")
        btn_home.grid(column=0, row=0, sticky="nesw", padx=10, pady=2)

        btn_data = tk.Button(tab, text="Data", command=self.data_button_click, height=2, width=10)
        btn_data.grid(column=1, row=0, sticky="nesw", padx=10, pady=2)

        btn_help = tk.Button(tab, text="Help", command=self.help_button_click, height=2, width=10)
        btn_help.grid(column=2, row=0, sticky="nesw", padx=10, pady=2)

        # Frame Bluetooth
        bluetooth = tk.Frame(self.home_frame, bg="blue")
        bluetooth.grid(column=0, row=1, columnspan=1, rowspan=2, padx=10, pady=2, sticky="nesw")

        bluetooth.columnconfigure(0, weight=1)
        bluetooth.columnconfigure(1, weight=1)
        bluetooth.rowconfigure(0, weight=0)
        bluetooth.rowconfigure(1, weight=0)
        bluetooth.rowconfigure(2, weight=0)
        #oggetti del frame bluetooth

        bluetooth_label=tk.Label(bluetooth, text="Bluetooth", bg="blue")
        bluetooth_label.grid(column=0, row=0, padx=10, pady=2, sticky="nsw")

        connected_device_frame=tk.Frame(bluetooth, height=40, bg="grey")
        connected_device_frame.grid(column=0, row=1, columnspan=2, padx=10, pady=2, sticky="nesw")
        testo_connected_device_frame=tk.Label(connected_device_frame, text="Connected Device", bg="gray")
        testo_connected_device_frame.grid(column=0, row=0, padx=10, pady=2, sticky="nesw")

        connect_button=tk.Button(bluetooth, text="Connect", command=self.connect_button_click ,height=1, width=4)
        connect_button.grid(column=0, row=2,padx=10, pady=2, sticky="nesw")

        disconnect_button=tk.Button(bluetooth, text="Disconnect", command=self.disconnect_button_click, height=1, width=4)
        disconnect_button.grid(column=1, row=2,padx=10, pady=2, sticky="nesw")

        # Frame Batteria
        battery_frame= tk.Frame(self.home_frame, height=40, bg="green")
        battery_frame.grid(column=0, row=3, columnspan=1, rowspan=1, padx=10, pady=2, sticky="nesw")

        battery_frame.columnconfigure(0, weight=0)
        battery_frame.columnconfigure(1, weight=1)
        battery_frame.rowconfigure(0, weight=0)


        battery_label=tk.Label(battery_frame, text="Battery:", bg="green", font=("Arial", 12) )
        battery_label.grid(column=0, row=0, padx=5, pady=2, sticky="nsw")

        battery_percentage=tk.Frame(battery_frame, height=20, bg="lightgreen" )
        battery_percentage.grid(column=1, row=0, padx=5, pady=2, sticky="nesw")
        battery_percentage_label=tk.Label(battery_percentage, text="Battery Percentage", bg="lightgreen")
        battery_percentage_label.grid(column=0, row=0, padx=5, pady=2, sticky="nesw")


       


        # Testo Dati Salvati
        testo1 = tk.Label(self.home_frame, text="SAVED DATA", bg="lightgrey")
        testo1.grid(column=0, row=4, columnspan=1, rowspan=1, padx=10, pady=2, sticky="nesw")

        # Frame Dati Salvati
        salvataggi = tk.Frame(self.home_frame, bg="grey")
        salvataggi.grid(column=0, row=5, columnspan=1, rowspan=2, padx=10, pady=2, sticky="nesw")

        # Testo Frame Dati Salvati
        testo_frame_saved_data = tk.Label(salvataggi, text="Frame dei dati salvati", bg="grey", font=("Arial", 12))
        testo_frame_saved_data.grid(column=0, row=5, columnspan=1, rowspan=1, padx=10, pady=2, sticky="nesw")


        #Frame dati input

        #Funzioni dei due bottoni della tab
        def singlemode_button_click():
            self.mode="Single Mode"
            print("Modalita' Single Mode selezionata")
            input_frame2.grid_forget()
            input_frame.grid(column=1, row=1, columnspan=2, rowspan=5, padx=10, pady=2, sticky="nesw")
            input_frame.grid_propagate(False)
        def sweepmode_button_click():
            self.mode="Sweep Mode"
            print("Modalita' Sweep Mode selezionata")
            input_frame.grid_forget()
            input_frame2.grid(column=1, row=1, columnspan=2, rowspan=5, padx=10, pady=2, sticky="nesw")
            input_frame2.grid_propagate(False)
        # Frame dati input modalità singola (automaticamente attivo)
        input_frame = tk.Frame(self.home_frame, bg="orange")
        input_frame.grid(column=1, row=1, columnspan=2, rowspan=5, padx=10, pady=2, sticky="nesw")



        input_frame.columnconfigure(0, weight=1)
        input_frame.columnconfigure(1, weight=1)
        input_frame.rowconfigure(0,weight=0)
        input_frame.rowconfigure(1,weight=1)
        input_frame.rowconfigure(2,weight=1)
        input_frame.rowconfigure(3,weight=1)
        input_frame.rowconfigure(4,weight=1)

       
        # Tab modalità frequenziale
        tab1 = tk.Frame(input_frame, height=30, bg="white")
        tab1.grid(column=0, row=0, columnspan=2, rowspan=1, padx=0, pady=0, sticky="nesw")
        tab1.columnconfigure(0, weight=1)
        tab1.columnconfigure(1, weight=1)
        singlemode_button=tk.Button(tab1,text="Single Mode",bg="lightgray", height=2, width=5, command=singlemode_button_click)
        singlemode_button.grid(column=0, row=0, columnspan=1, rowspan=1, padx=10, pady=2, sticky="nesw")
        sweepmode_button=tk.Button(tab1,text="Sweep Mode",bg="white", height=2, width=5, command=sweepmode_button_click)
        sweepmode_button.grid(column=1, row=0, columnspan=1, rowspan=1, padx=10, pady=2, sticky="nesw")

        #Dati
        voltage_label=tk.Label(input_frame, text="Voltage(mV):", bg="orange", font=("Arial", 14))
        voltage_label.grid(column=0, row=1, padx=5, pady=2, sticky="nsw")

        voltage_input=tk.Entry(input_frame,textvariable=self.voltage_str, bg="white", font=("Arial", 14))
        voltage_input.grid(column=1, row=1, padx=15, pady=8, sticky="nesw")
       


        frequency_label=tk.Label(input_frame, text="Frequency(Hz):", bg="orange", font=("Arial", 16))
        frequency_label.grid( padx=5, pady=2, sticky="nsw")
        
        frequency_input=tk.Entry(input_frame, textvariable=self.frequency_str,bg="white", font=("Arial", 14))
        frequency_input.grid(column=1, row=2, padx=15, pady=8, sticky="nesw")
       
        # Frame dati input modalità sweep
        input_frame2 = tk.Frame(self.home_frame, bg="orange")

        

        input_frame2.columnconfigure(0, weight=1)
        input_frame2.columnconfigure(1, weight=1)
        input_frame2.rowconfigure(0,weight=0)
        input_frame2.rowconfigure(1,weight=1)
        input_frame2.rowconfigure(2,weight=1)
        input_frame2.rowconfigure(3,weight=1)
        input_frame2.rowconfigure(4,weight=1)

        # Tab modalità frequenziale
        tab2 = tk.Frame(input_frame2, height=30, bg="white")
        tab2.grid(column=0, row=0, columnspan=2, rowspan=1, padx=0, pady=0, sticky="nesw")
        tab2.columnconfigure(0, weight=1)
        tab2.columnconfigure(1, weight=1)
        singlemode_button=tk.Button(tab2,text="Single Mode",bg="white", height=2, width=5, command=singlemode_button_click)
        singlemode_button.grid(column=0, row=0, columnspan=1, rowspan=1, padx=10, pady=2, sticky="nesw")
        sweepmode_button=tk.Button(tab2,text="Sweep Mode",bg="lightgray", height=2, width=5, command=sweepmode_button_click)
        sweepmode_button.grid(column=1, row=0, columnspan=1, rowspan=1, padx=10, pady=2, sticky="nesw")

     
        # Dati
        voltage_label = tk.Label(input_frame2, text="Voltage(mV):", bg="orange", font=("Arial", 16))
        voltage_label.grid(column=0, row=1, padx=5, pady=2, sticky="nsw")
        # Campo di input per il voltage
        voltage_input = tk.Entry(input_frame2, textvariable=self.voltage_str, bg="white", font=("Arial", 16))  # Aggiunto font per migliorare la visibilità
        voltage_input.grid(column=1, row=1, padx=15, pady=8, sticky="nesw")

        # Min Frequency
        minimumFrequency_label = tk.Label(input_frame2, text="Min Frequency(Hz):", bg="orange", font=("Arial", 16))
        minimumFrequency_label.grid(column=0, row=2, padx=5, pady=2, sticky="nsw")

        minimumFrequency_input = tk.Entry(input_frame2, textvariable=self.min_frequency_str, bg="white", font=("Arial", 14))  # Aggiunto font
        minimumFrequency_input.grid(column=1, row=2, padx=15, pady=8, sticky="nesw")

        # Max Frequency
        maximumFrequency_label = tk.Label(input_frame2, text="Max Frequency(Hz):", bg="orange", font=("Arial", 16))
        maximumFrequency_label.grid(column=0, row=3, padx=5, pady=2, sticky="nsw")

        maximumFrequency_input = tk.Entry(input_frame2, textvariable=self.max_frequency_str, bg="white", font=("Arial", 14))  # Aggiunto font
        maximumFrequency_input.grid(column=1, row=3, padx=15, pady=8, sticky="nesw")

        # Number of Repetitions
        numberRepetitions_label = tk.Label(input_frame2, text="Number of repetitions:", bg="orange", font=("Arial", 16))
        numberRepetitions_label.grid(column=0, row=4, pady=2, sticky="nsw")

        numberRepetitions_input = tk.Entry(input_frame2, textvariable=self.numberRepetitions_str, bg="white", font=("Arial", 14))  # Aggiunto font
        numberRepetitions_input.grid(column=1, row=4, padx=15, pady=8, sticky="nesw")


        # Bottone Start
        start = tk.Button(self.home_frame, text="START", height=3, width=2, command=self.start_button_click, bg="yellow", font=("Arial", 12))
        start.grid(column=1, row=6, columnspan=1, rowspan=1, padx=10, pady=2, sticky="nesw")

        # Bottone Exit
        exit_button = tk.Button(self.home_frame, text="EXIT", height=3, width=2, command=self.exit_button_click, bg="gray", font=("Arial", 12))
        exit_button.grid(column=2, row=6, columnspan=1, rowspan=1, padx=10, pady=2, sticky="nesw")

    def create_data_frame(self):

        # Configure layout for the "data" frame
        self.data_frame.columnconfigure(0, weight=1)
        self.data_frame.columnconfigure(1, weight=1)
        self.data_frame.rowconfigure(0, weight=0)  # Row for the tab
        #self.data_frame.rowconfigure(1, weight=1)  # Row for the main content
        self.data_frame.rowconfigure(1, minsize=20)
        self.data_frame.rowconfigure(2, weight=8)
        self.data_frame.rowconfigure(3, weight=8)
        self.data_frame.rowconfigure(4,  weight=2) 
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
        btn_home = tk.Button(tab, text="Home", command=self.home_button_click, height=2, width=10)
        btn_home.grid(column=0, row=0, sticky="nesw", padx=10, pady=2)

        btn_data = tk.Button(tab, text="Data", command=self.data_button_click, height=2, width=10, bg= "gray")
        btn_data.grid(column=1, row=0, sticky="nesw", padx=10, pady=2)

        btn_help = tk.Button(tab, text="Help", command=self.help_button_click, height=2, width=10)
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
        reset_button = tk.Button(lower_left_frame, text="RESET", command=self.reset_button_click, bg="purple", height=2, width=5)
        reset_button.grid(column=0, row=0, padx=5, pady=5, sticky="nesw")
        
        stop_button = tk.Button(lower_left_frame, text="STOP",command=self.stop_button_click, bg="red", height=2, width=5)
        stop_button.grid(column=1, row=0, padx=5, pady=5, sticky="nesw")

        add_marker_button = tk.Button(lower_left_frame, text="ADD MARKER",command=self.addMarker_button_click, bg="lightpink", height=2, width=5)
        add_marker_button.grid(column=0, row=1, padx=5, pady=5, sticky="nesw")

        saveData_button = tk.Button(lower_left_frame, text="SAVE DATA", command=self.saveData_button_click, bg="lightblue", height=2, width=5)
        saveData_button.grid(column=1, row=1, padx=5, pady=5, sticky="nesw")

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
        btn_home = tk.Button(tab, text="Home", command=self.home_button_click, height=2, width=10)
        btn_home.grid(column=0, row=0, sticky="nesw", padx=10, pady=2)

        btn_data = tk.Button(tab, text="Data", command=self.data_button_click, height=2, width=10)
        btn_data.grid(column=1, row=0, sticky="nesw", padx=10, pady=2)

        btn_help = tk.Button(tab, text="Help", command=self.help_button_click, height=2, width=10, bg= "gray")
        btn_help.grid(column=2, row=0, sticky="nesw", padx=10, pady=2)

        # Testo Help
        help_label = tk.Label(self.help_frame, text="Help Section: qui si trova il testo di aiuto (Work in progress)", bg="lightyellow")
        help_label.grid(column=0, row=1, columnspan=3, padx=20, pady=20, sticky="nesw")


    def show_frame(self, frame):
        """ Mostra il frame selezionato """
        frame.tkraise()
        
    #Funzioni dei Bottoni 
    def home_button_click(self):
        self.show_frame(self.home_frame)
        print("Home")
    
    def data_button_click(self):
        self.show_frame(self.data_frame)
        print("Data")
    
    def help_button_click(self):
        self.show_frame(self.help_frame)
        print("Help")

    def connect_button_click(self):
        print("Connect")

    def disconnect_button_click(self):
        print("Disconnect")

    def start_button_click(self):
        print("Start: Visualizzazione dei dati inseriti...\n")
        if self.mode=="Single Mode":  
            voltage=self.voltage_str.get()
            frequency=self.frequency_str.get()
            print(f"Tensione: ",voltage, "mV")
            print(f"Frequenza: ",frequency, "Hz")
        
        else:
            voltage=self.voltage_str.get()
            min_frequency=self.min_frequency_str.get() 
            max_frequency=self.max_frequency_str.get() 
            numberRepetitions=self.numberRepetitions_str.get()
            print(f"Tensione: ",voltage, "mV")
            print(f"Frequenza minima: ",min_frequency, "Hz") 
            print(f"Frequenza massima: ",max_frequency, "Hz") 
            print(f"Numero di Ripetizioni: ", numberRepetitions) 
        self.show_frame(self.data_frame)

    def exit_button_click(self):
        print("Exit")
        self.quit()
            
    def reset_button_click(self):
        print("Reset")

    def stop_button_click(self):
        print("Stop")

    def addMarker_button_click(self):
        print("Add Marker")

    def saveData_button_click(self):
        print("Save Data")

#Fine
if __name__ == "__main__":
    app = IsulinometroApp()
    app.mainloop()
