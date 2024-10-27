import tkinter as tk
from tkinter import ttk,scrolledtext
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from bleak import BleakScanner 
import asyncio
import threading

class InsulinometroApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.mode="Single Mode"
        
        self.devices = []
        #Variabili per i campi di input
        self.voltage_str = tk.StringVar()
        self.frequency_str = tk.StringVar()
        self.min_frequency_str = tk.StringVar() 
        self.max_frequency_str = tk.StringVar()
        self.numberRepetitions_str=tk.StringVar()  
        
       
        # Imposta la geometria della finestra
        self.geometry("1000x500")

        self.wm_minsize(600, 300)  # Set minimum window size (600x300)

        # Permette il ridimensionamento della finestra
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Titolo finestra
        self.title("Insulinometro")

        # Inizializzazione di tre frame per le modalità Home e Data e Help
        self.home_frame = tk.Frame(self)
        self.data_frame = tk.Frame(self)
        self.help_frame = tk.Frame(self)  

        # Chiamata per la creazione dei widget nei tre frame
        self.create_home_frame()
        self.create_data_frame()
        self.create_help_frame()  

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
        tab.columnconfigure(2, weight=1) 

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
        testo1 = tk.Label(self.home_frame, text="SAVED DATA", font=("Arial", 16))
        testo1.grid(column=0, row=4, columnspan=1, rowspan=1, padx=10, pady=2, sticky="nesw")


        # Frame Dati Salvati 
        salvataggi = tk.Frame(self.home_frame, bg="grey")
        salvataggi.grid(column=0, row=5, columnspan=1, rowspan=2, padx=10, pady=2, sticky="nesw")

        # Testo Frame Dati Salvati
        testo_frame_saved_data = tk.Label(salvataggi, text="Frame dei dati salvati", bg="grey", font=("Arial", 12))
        testo_frame_saved_data.grid(column=0, row=5, columnspan=1, rowspan=1, padx=10, pady=2, sticky="nesw")


        #Frame dati 
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
        self.data_frame.rowconfigure(2, weight=1)
        self.data_frame.rowconfigure(3, weight=1)
        self.data_frame.rowconfigure(4,  weight=1, minsize=125) 
        #self.data_frame.rowconfigure(4, weight=1)
        self.data_frame.rowconfigure(5, weight=1, minsize=40)  # Assign weight to the row for the activity log


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

        #Valore iniziale provvisorio per l'asciisa
        self.ascissa=1

        #Grafico di Bode del moulo
        self.x_values_BM = []
        self.y_values_BM = []

        self.fig_BM = Figure()
        self.fig_BM.subplots_adjust(top=0.83, bottom = 0.17)
        self.ax_BM = self.fig_BM.add_subplot(111)
        self.ax_BM.set_title("Modulo")
        self.canvas_BM = FigureCanvasTkAgg(self.fig_BM, self.data_frame)
        self.canvas_widget_BM = self.canvas_BM.get_tk_widget()
        self.canvas_widget_BM.grid(column=0, row=2, padx=10, pady=2, sticky="nesw")

        #Grafico di Bode della Fase
        self.x_values_BF = []
        self.y_values_BF = []

        self.fig_BF = Figure()
        self.fig_BF.subplots_adjust(top=0.83,bottom=0.17)
        self.ax_BF = self.fig_BF.add_subplot(111)
        self.ax_BF.set_title("Fase")
        self.canvas_BF = FigureCanvasTkAgg(self.fig_BF, self.data_frame)
        self.canvas_widget_BF = self.canvas_BF.get_tk_widget()
        self.canvas_widget_BF.grid(column=0, row=3, padx=10, pady=2, sticky="nesw")




        # Lower Frame with buttons
        lower_left_frame = tk.Frame(self.data_frame, bg="cyan")
        lower_left_frame.grid(column=0, row=4, padx=10, pady=2, sticky="nesw")
        lower_left_frame.columnconfigure(0, weight=1)
        lower_left_frame.columnconfigure(1, weight=1)
        lower_left_frame.rowconfigure(0, weight=1)
        lower_left_frame.rowconfigure(1, weight=1)

        # Buttons inside the lower left frame
        reset_button = tk.Button(lower_left_frame, text="RESET", command=self.reset_button_click, bg="blue", height=2, width=5)
        reset_button.grid(column=0, row=0, padx=5, pady=5, sticky="nesw")
        
        stop_button = tk.Button(lower_left_frame, text="STOP",command=self.stop_button_click, bg="red", height=2, width=5)
        stop_button.grid(column=1, row=0, padx=5, pady=5, sticky="nesw")

        add_marker_button = tk.Button(lower_left_frame, text="ADD MARKER",command=self.addMarker_button_click, bg="yellow", height=2, width=5)
        add_marker_button.grid(column=0, row=1, padx=5, pady=5, sticky="nesw")

        saveData_button = tk.Button(lower_left_frame, text="SAVE DATA", command=self.saveData_button_click, bg="lightblue", height=2, width=5)
        saveData_button.grid(column=1, row=1, padx=5, pady=5, sticky="nesw")

        # Right Column (2 frames)
        # Top frame (same height as the two frames on the left)
        self.x_values_N = []
        self.y_values_N = []

        self.fig_N = Figure()
        self.ax_N = self.fig_N.add_subplot(111)
        self.canvas_N = FigureCanvasTkAgg(self.fig_N, self.data_frame)
        self.canvas_widget_N = self.canvas_N.get_tk_widget()
        self.canvas_widget_N.grid(column=1, row=2, rowspan=2, padx=10, pady=2, sticky="nesw")

        # Tabella
        self.columns=('index', 'value')
        self.tree = ttk.Treeview(self.data_frame, columns=self.columns, height =4, show='headings')
        self.tree.grid(column=1, row=4, padx=10, pady=2, sticky="nesw")
        self.tree.heading('index', text ='Index')
        self.tree.heading('value', text ='Resistance(Ohm)')

        # Activity Log at the bottom (spans across both columns)
        activity_log = tk.Frame(self.data_frame, bg="grey")
        activity_log.grid(column=0, row=5, columnspan=2, padx=10, pady=2, sticky="nesw")

        # Adding text to the activity log
        activity_log_label = tk.Label(activity_log, text="Activity Log", bg="grey", font=("Arial", 10))
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
        self.run_scanning()
    
    def disconnect_button_click(self):
        print("Disconnect")

    def start_button_click(self):
        print("Start")

        if self.mode=="Single Mode": 
            try:
                voltage=int(self.voltage_str.get())
                frequency=int(self.frequency_str.get())
                if (voltage < 10 or voltage > 500):
                    raise ValueError("il valore della tensione deve essere compreso tra 10mV e 500mV")
                if (frequency<1 or frequency > 100000):
                    raise ValueError("il valore della frequenza deve essere compreso tra 1Hz e 100kHz")
            except ValueError as e:
                print("Error:",e)
                print("Reinserire i valori")
            else:
                #Approssimo la tensione affinché la risoluzione sia di 10mV
                if ((voltage % 10) < 5):
                    voltage = voltage -(voltage % 10)
                else:
                    voltage = voltage -(voltage % 10) + 10
                
                #Stampa input
                print(f"Visualizzazione dei dati inseriti...\n")
                print(f"Tensione: ",voltage, "mV")
                print(f"Frequenza: ",frequency, "Hz")

                #Passaggio alla schermata Data
                self.show_frame(self.data_frame)
                self.open_popup() #pop up provvisorio per l'inserimento della resistenza da tastiera
        
        else:
            #Sweep Mode
            try:
                voltage=int(self.voltage_str.get())
                min_frequency=int(self.min_frequency_str.get())
                max_frequency=int(self.max_frequency_str.get())
                numberRepetitions=int(self.numberRepetitions_str.get())

                if (voltage < 10 or voltage > 500):
                    raise ValueError("il valore della tensione deve essere compreso tra 10mV e 500mV")
                if ((min_frequency<1 or min_frequency > 100000) or (max_frequency<1 or max_frequency > 100000)):
                    raise ValueError("i valori delle frequenze devono essere compresi tra 1Hz e 100kHz")
                if max_frequency <= min_frequency  :
                    raise ValueError("la frequenza massima deve essere superiore alla frequenza minima")
                max_repetetions = max_frequency - min_frequency + 1
                if numberRepetitions < 2:
                    raise ValueError("il numero di ripetizioni inserito è troppo basso")
                if numberRepetitions > max_repetetions:
                    raise ValueError("troppe ripetizioni richieste per l'intervallo frequenziale scelto")
                
            except ValueError as e:
                print("Error:",e)
                print("Reinserire i valori")
            else:
                #Approssimo la tensione affinché la risoluzione sia di 10mV
                if ((voltage % 10) < 5):
                    voltage = voltage -(voltage % 10)
                else:
                    voltage = voltage -(voltage % 10) + 10
                
                #Stampa degli input
                print(f"Visualizzazione dei dati inseriti...\n")
                print(f"Tensione: ",voltage, "mV")
                print(f"Frequenza minima: ",min_frequency, "Hz") 
                print(f"Frequenza massima: ",max_frequency, "Hz") 
                print(f"Numero di Ripetizioni: ", numberRepetitions) 

                #Passaggio alla schermata Data
                self.show_frame(self.data_frame)
                self.open_popup()
        
    def exit_button_click(self):
        print("Exit")
        self.quit()
            
    def reset_button_click(self):
        #Reset Grafici
        #Reset del grafico del modulo di Bode
        self.x_values_BM = []
        self.y_values_BM = []
        self.update_graph(self.ax_BM, self.canvas_BM, self.x_values_BM, self.y_values_BM, "Modulo")

        #Reset del grafico della fase di Bode
        self.x_values_BF = []
        self.y_values_BF = []
        self.update_graph(self.ax_BF, self.canvas_BF, self.x_values_BF, self.y_values_BF, "Fase")

        #Reset del grafico di Nyquist
        self.x_values_N = []
        self.y_values_N = []
        self.update_graph(self.ax_N, self.canvas_N, self.x_values_N, self.y_values_N, "")

        #Reset tabella
        for item in self.tree.get_children():
            self.tree.delete(item)

        #PROVVISORIO
        self.ascissa=1

    def stop_button_click(self):
        print("Stop")

    def addMarker_button_click(self):
        print("Add Marker")

    def saveData_button_click(self):
        print("Save Data")

    def update_graph(self, ax, canvas, x_values, y_values, title):
        #Aggiorno il grafico
        ax.clear()
        ax.plot(x_values, y_values, marker = 'o')
        ax.set_title(title)
        canvas.draw_idle()

    def update_graph_and_tree(self):
        #Cattura del valore della resistenza inserito dal popup
        try:
            resistance=float(self.new_resistance.get())
            if (resistance < 1 or resistance > 500):
                    raise ValueError("il valore della rsistenza deve essere compreso tra 1 Ohm e 500 Ohm")
        except ValueError as e:
                print("Error:",e)
                print("Reinserire il valore")
        else:
            
            #Aggiorno la tabbella
            self.tree.insert("","end", values=(self.ascissa, resistance))

            #Aggiorno i gragici
            #Bode Modulo
            self.x_values_BM.append(self.ascissa)   #DA MODIFICARE
            self.y_values_BM.append(resistance)     #DA MODIFICARE

            self.update_graph(self.ax_BM, self.canvas_BM, self.x_values_BM, self.y_values_BM, "Modulo")
            
            #Bode Fase
            self.x_values_BF.append(self.ascissa)   #DA MODIFICARE
            self.y_values_BF.append(resistance)     #DA MODIFICARE

            self.update_graph(self.ax_BF, self.canvas_BF, self.x_values_BF, self.y_values_BF, "Fase")

            #Nyquist
            self.x_values_N.append(self.ascissa)    #DA MODIFICARE
            self.y_values_N.append(resistance)      #DA MODIFICARE

            self.update_graph(self.ax_N, self.canvas_N, self.x_values_N, self.y_values_N, "")

           #Incremento il valore PROVVISORIO dell'ascissa
            self.ascissa=self.ascissa+1

    def open_popup(self):
        #Creazione del popup
        popup = tk.Toplevel()
        popup.title("Aggiunta valori ...")


        self.new_resistance= tk.StringVar()
        

        Testo_popup=tk.Label(popup, text="Il nuovo valore della Resistenza (deve essere compreso tra 1 e 500 Ohm):")
        Testo_popup.pack(pady=10)
        entry = tk.Entry(popup, textvariable=self.new_resistance)
        entry.pack(pady=10, padx=5)

        update_button = tk.Button(popup, text="Aggiorna", command=self.update_graph_and_tree)
        update_button.pack(pady=10)
    
    def run_scanning(self):
        print("Starting scanning...")
        thread = threading.Thread(target=lambda: asyncio.run(self.scan_for_devices()))  # Esegui la scansione
        thread.start()

    def open_device_list_popup(self, devices):
        # Crea un nuovo popup
        popup = tk.Toplevel(self)
        popup.title("Dispositivi trovati")
        popup.geometry("300x200")
        # Crea un Listbox per mostrare i dispositivi
        device_listbox = tk.Listbox(popup)
        device_listbox.rowconfigure(0,weight=1)
        device_listbox.grid(row=0,padx=5,pady=2,sticky='nesw')
        
        # Aggiungi i dispositivi trovati al Listbox
        for device in devices:
            device_listbox.insert(tk.END, f"{device.name} ({device.address})")  # Aggiungi alla lista
        
        # Pulsante per chiudere il popup
        close_button = tk.Button(popup, text="Chiudi", command=popup.destroy)
        close_button.grid(row=1, column=0, pady=10)  # Usa grid per il pulsante "Chiudi"

        # Configura il layout del popup
        popup.grid_rowconfigure(0, weight=1)  # Permette al Listbox di espandersi
        popup.grid_columnconfigure(0, weight=1)  # Permette al Listbox di espandersi


    async def scan_for_devices(self):
        print("Scanning for devices...")
        self.devices = await BleakScanner.discover()  # Scansione dei dispositivi
        self.open_device_list_popup(self.devices)  # Apri il popup con i dispositivi trovati

if __name__ == "__main__":
    app = InsulinometroApp()
    app.mainloop()