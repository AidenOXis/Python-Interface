import tkinter as tk
from tkinter import ttk,messagebox
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from bleak import BleakScanner 
import asyncio,threading
from bleak import BleakClient
import math,random,time
import serial,serial.tools.list_ports_windows

SERVICE_UUID = "12345678_1234_5678_1234_56789abcdef0"
CHARACTERISTIC_UUID_READ = "12345678_1234_5678_1234_56789abcdef1"
CHARACTERISTIC_UUID_WRITE = "12345678_1234_5678_1234_56789abcdef2"

baud_rate = 115200 

class InsulinometroApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.mode="Single Mode"
        
        global popup_scan_aperto
        popup_scan_aperto = False

        global popup_dati_aperto
        popup_dati_aperto = False
        
        global popup_SM_aperto
        popup_SM_aperto=False

        global led_esp_acceso
        led_esp_acceso=False

        self.add_marker_enabled = False
        self.devices = []

        self.ble_address = 0
        self.ble_name = "None"

        self.plotting = False

        self.SERconnected = False

        self.connected = False

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

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

#Funzioni creazione e update Frame
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


        # Frame Bluetooth Caso Disconnesso
        self.disconnected_bluetooth_frame = tk.Frame(self.home_frame, bg="blue")
        self.disconnected_bluetooth_frame.grid(column=0, row=1, columnspan=1, rowspan=2, padx=10, pady=2, sticky="nesw")

        self.disconnected_bluetooth_frame.columnconfigure(0, weight=1)
        self.disconnected_bluetooth_frame.rowconfigure(0, weight=0)
        self.disconnected_bluetooth_frame.rowconfigure(1, weight=0)

        label_bluetooth = tk.Label(self.disconnected_bluetooth_frame, text="Bluetooth: Disconnected", bg="blue",font=("Arial", 14))
        label_bluetooth.grid(column=0, row=0, padx=10, pady=2, sticky="nw")

        scan_button = tk.Button(self.disconnected_bluetooth_frame, text="Scan", command=self.scan_button_click ,height=1, width=4)
        scan_button.grid(column=0, row=1, padx=10, pady=2, sticky="nesw")


        # Frame Bluetooth Caso Connesso
        self.connected_bluetooth_frame = tk.Frame(self.home_frame, bg="blue")
        #self.connected_bluetooth_frame.grid(column=0, row=1, columnspan=1, rowspan=2, padx=10, pady=2, sticky="nesw") #TEST

        self.connected_bluetooth_frame.columnconfigure(0, weight=1)
        self.connected_bluetooth_frame.columnconfigure(1, weight=1)
        self.connected_bluetooth_frame.rowconfigure(0, weight=0)
        self.connected_bluetooth_frame.rowconfigure(1, weight=0)
        self.connected_bluetooth_frame.rowconfigure(2, weight=0)
        self.connected_bluetooth_frame.rowconfigure(3, weight=0)

        label_bluetooth = tk.Label(self.connected_bluetooth_frame, text="Bluetooth: Connected", bg="blue",font=("Arial", 14))
        label_bluetooth.grid(column=0, row=0, columnspan=2 ,padx=10, pady=2, sticky="nw")

        bluetooth_label=tk.Label(self.connected_bluetooth_frame, text= "Device: " + self.ble_name, bg="blue", font=("Arial", 12))
        bluetooth_label.grid(column=0, row=1, columnspan=2, padx=10, pady=2, sticky="nw")

        scan_button = tk.Button(self.connected_bluetooth_frame, text="Scan", command=self.scan_button_click ,height=1, width=4)
        scan_button.grid(column=0, row=2, padx=10, pady=2, sticky="nesw")

        disconnect_button=tk.Button(self.connected_bluetooth_frame, text="Disconnect", command=self.disconnect_button_click, height=1, width=4)
        disconnect_button.grid(column=1, row=2,padx=10, pady=2, sticky="nesw")

        # Frame Batteria
        battery_frame= tk.Frame(self.connected_bluetooth_frame, height=40, bg="green")
        battery_frame.grid(column=0, row=3, columnspan=2, rowspan=1, padx=10, pady=2, sticky="nesw")

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
        testo1.grid(column=0, row=3, columnspan=1, rowspan=1, padx=10, pady=2, sticky="nesw")


        # Frame Dati Salvati 
        salvataggi = tk.Frame(self.home_frame, bg="grey")
        salvataggi.grid(column=0, row=4, columnspan=1, rowspan=3, padx=10, pady=2, sticky="nesw")

        # Testo Frame Dati Salvati : qui andranno mostrati i dati salvati precedentemente all'avvio e durante l'esecuzione dell'app
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
        # Aggiunta della griglia
        self.ax_BM.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')  # Griglia personalizzata
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
        self.ax_BF.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')  # Griglia personalizzata
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

        self.add_marker_button = tk.Button(lower_left_frame, text="Add Marker(disabled)",command=self.toggle_add_marker, bg="yellow", height=2, width=5)
        self.add_marker_button.grid(column=0, row=1, padx=5, pady=5, sticky="nesw")
        # Pulsante per attivare/disattivare la modalità "Add Marker"


        saveData_button = tk.Button(lower_left_frame, text="SAVE DATA", command=self.saveData_button_click, bg="lightblue", height=2, width=5)
        saveData_button.grid(column=1, row=1, padx=5, pady=5, sticky="nesw")

        # Right Column (2 frames)
        # Top frame (same height as the two frames on the left)
        self.x_values_N = []
        self.y_values_N = []

        self.fig_N = Figure()
        self.ax_N = self.fig_N.add_subplot(111)
        self.ax_N.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')  # Griglia personalizzata
        self.canvas_N = FigureCanvasTkAgg(self.fig_N, self.data_frame)
        self.canvas_widget_N = self.canvas_N.get_tk_widget()
        self.canvas_widget_N.grid(column=1, row=2, rowspan=2, padx=10, pady=2, sticky="nesw")

        self.canvas_BM.mpl_connect('button_press_event', self.connect_click_marker)
        self.canvas_BF.mpl_connect('button_press_event', self.connect_click_marker)
        self.canvas_N.mpl_connect('button_press_event', self.connect_click_marker)

        # Creazione delle Tabelle
        #Tab per switchare tra le tabelle
        notebook = ttk.Notebook(self.data_frame)
        notebook.grid(column=1, row=4, padx=10, pady=2, sticky="nesw")

        # Scheda per tutti i punti
        self.all_points_frame = ttk.Frame(notebook)
        notebook.add(self.all_points_frame, text="Tutti i Punti")

        # Scheda per i marker sui grafici di Bode
        self.Bode_markers_frame = ttk.Frame(notebook)
        notebook.add(self.Bode_markers_frame, text="Bode Markers")

        # Scheda per i marker sui grafici di Nyquist
        self.Nyquist_markers_frame = ttk.Frame(notebook)
        notebook.add(self.Nyquist_markers_frame, text="Nyquist Markers")

        #Tabella per i punti
        self.columns=('index', 'value')
        self.tree = ttk.Treeview(self.all_points_frame, columns=self.columns, height =4, show='headings')
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.heading('index', text ='Index')
        self.tree.heading('value', text ='Resistance(Ohm)')
        self.tree_indexes = []
        self.tree_values = []



        #Tabella per i marker sui grafici di Bode
        self.columns_B=('Frequency', 'Amplitude', 'Phase')
        self.Bode_markers_tree = ttk.Treeview(self.Bode_markers_frame, columns=self.columns_B, height =4, show='headings')
        self.Bode_markers_tree.grid(row=0, column=0, sticky="nsew")
        self.Bode_markers_tree.heading('Frequency', text ='Frequency')
        self.Bode_markers_tree.heading('Amplitude', text ='Amplitude')
        self.Bode_markers_tree.heading('Phase', text ='Phase')
        self.Bode_markers_tree_frequencies = []
        self.Bode_markers_tree_amplitudes = []
        self.Bode_markers_tree_phases = []
        
        #Tabella per i marker sul grafico di Nyquist
        self.columns_N=('Real', 'Immaginary')
        self.Nyquist_markers_tree = ttk.Treeview(self.Nyquist_markers_frame, columns=self.columns_N, height =4, show='headings')
        self.Nyquist_markers_tree.grid(row=0, column=0, sticky="nsew")
        self.Nyquist_markers_tree.heading('Real', text ='Real Part')
        self.Nyquist_markers_tree.heading('Immaginary', text ='Immaginary Part')
        self.Nyquist_markers_tree_reals = []
        self.Nyquist_markers_tree_immaginaries = []

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
        help.text= ("""
Help Section: Come utilizzare l'interfaccia di simulazione di un insulinometro

Benvenuto! Questa guida ti aiuterà a familiarizzare con le funzionalità e l'utilizzo del programma.
Segui questi passaggi per utilizzare al meglio l'applicazione.

1. Avvio dell'applicazione
   - Esegui il programma: Una volta avviato, si aprirà una finestra principale dell'interfaccia.
   - Il programma è strutturato su 3 tab: Home,Data ed Help (in cui ti trovi).
     Nella home vedrai le funzionalità principali dell'interfaccia,spiegate di seguito;
     Nella schermata 'data' vedrai le info relative ai grafici plottati sulla misurazione.
                    
2. Connessione ai dispositivi BLE
   - Il programma consente di comunicare con dispositivi Bluetooth Low Energy (BLE):
     * Scansiona i dispositivi:
       - Fai clic sul pulsante `Scan` nella finestra principale.
       - L'applicazione cercherà i dispositivi BLE disponibili nelle vicinanze.
     * Seleziona un dispositivo:
       - Scegli dall’elenco il dispositivo BLE con cui desideri connetterti.
       - Conferma la connessione per procedere.

3. Inserimento dei parametri di simulazione e modalità operativa
    A)Scegli il tipo di modalità operativa:
        * Single mode: 
        -Misurazioni effettuate su frequenza singola scelta.
        * Sweep mode:
        -Misurazioni effettuate su numero di ripetizioni scelte tra minimo a massimo di frequenza.
    B)Configura i parametri della simulazione utilizzando i campi di input:
     * Tensione (Voltage):
       - Inserisci il valore di tensione richiesto per la simulazione (compreso tra 10mV e 500 mV).
     * Frequenza operativa (Frequency) tra 1Hz e 100khz:
       - Imposta la frequenza singola (single mode) o quella minima e massima (sweep mode).
     * Numero di ripetizioni:
       - Specifica quante volte desideri eseguire il test (solo per sweep mode) inserendo un valore minore della 
         differenza tra massima e minima frequenza.

4. Avvio della simulazione
   - Dopo aver configurato i parametri, fai clic sul pulsante `Start ` per avviare la simulazione.
   - Se connessa ad un dispositivo BLE, l’applicazione elaborerà i dati e invierà le istruzioni ad esso.
     In vaso contrario sarà avviata una simulazione inserendo randomicamente (per simulare la ricezione dati) i valori di resistenza tra 1 Ohm e 500 Ohm.

5. Monitoraggio dei risultati
    * Visualizzazione in tempo reale:
     -I dati raccolti o simulati verranno visualizzati su un grafico interattivo nella finestra data.
                    
    * Aggiunta di Marker
    - Su ogni punto del grafico è possibile aggiungere un Marker (contrassegnandolo con un cerchio rosso ) , per farlo:
        1)Clicca sul pulsante 'Add Marker' (spunterà una voce 'enabled');
        2)Clicca sul punto del grafico di interesse (se il clic non avviene correttamente apparirà un errore);
        3)Puoi interrompere la fase di "aggiunta Marker" cliccando nuovamente 
          sul tasto 'Add Marker' (dovrebbe spuntare la voce 'disabled'.)
   * Log dei messaggi:
     - Una sezione dedicata mostrerà lo storico dei comandi e delle risposte (utile per il debug o l’analisi).

6. Funzioni aggiuntive
   - Interrompere la simulazione:
     * Usa il pulsante `Stop` per fermare la raccolta dati in corso (solo se connessi/siulazione in corso).
   - Esportazione dei dati :
     * Salva i risultati della simulazione in un file .csv o .txt per un’analisi successiva (da implementare).

7. Chiudere l’applicazione
   - Per chiudere il programma, utilizza il pulsante `Exit` o chiudi la finestra direttamente.

Suggerimenti utili per la connessione:
   - Assicurati di avere i permessi per il Bluetooth:
     * L’applicazione necessita dell’accesso BLE per funzionare correttamente.
   - Mantieni il dispositivo BLE vicino:
     * La connessione può fallire se il dispositivo è troppo lontano.
"""
    )
        # Widget di testo per visualizzare l'help
        help_label = tk.Text(self.help_frame, wrap="word", bg="white", height=15)
        help_label.insert("1.0", help.text)
        help_label.config(state="disabled", font=("Arial", 12, "normal"))  # Modifica del font (Arial, 12pt, normale)
        help_label.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

        # Scrollbar per il widget di testo
        scrollbar = ttk.Scrollbar(self.help_frame, orient="vertical", command=help_label.yview)
        help_label.config(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=3, sticky="ns")

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

    def show_frame(self, frame):
        """ Mostra il frame selezionato """
        frame.tkraise()
    
    def switch_bluetooth_frame(self, status):
        if status == True:
            self.disconnected_bluetooth_frame.grid_forget()
            self.connected_bluetooth_frame.grid(column=0, row=1, columnspan=1, rowspan=2, padx=10, pady=2, sticky="nesw")
        else:
            self.connected_bluetooth_frame.grid_forget()
            self.disconnected_bluetooth_frame.grid(column=0, row=1, columnspan=1, rowspan=2, padx=10, pady=2, sticky="nesw")
 
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
    
    def scan_button_click(self):
        print("Scanning")
        self.run_scanning()
    
    def disconnect_button_click(self):
        print("Disconnect")
        self.connected = False
        self.switch_bluetooth_frame(False)
        global popup_scan_aperto
        #Check chiusura pop-up scan
        if popup_scan_aperto ==True:
            self.popup_scan.destroy()
            popup_scan_aperto = False
        
        global popup_dati_aperto
        #Check chiusura pop-up dati server
        if popup_dati_aperto==True:
            self.popup_dati.destroy()
            popup_dati_aperto = False

        self.ble_address = 0
        self.ble_name= "None"

    def start_button_click(self):
        print("Start")
         # Configurazione della porta seriale
        esp_port = self.find_esp32()
        if esp_port:
            self.ser = serial.Serial(esp_port, baud_rate, timeout=1)
            print("Connessione stabilita")
            self.SERconnected= True
        else:
            print("Il dispositivo seriale non è stato trovato")
            messagebox.showerror("Errore comunicazione seriale","Nessun dispositivo collegato alla porta seriale,"
                                 "riprovare a connettere.")
        #Controllo se ci sono valori già inseriti per ricordare all'utente
        if self.x_values_N:
            risposta = messagebox.askyesno("Conferma Salvataggio", "Ci sono dati non salvati.\nVuoi salvare?")
            if risposta:  # Se l'utente clicca su "Sì"
                self.saveData_button_click() #salvataggio da implementare
                self.reset_button_click()
            else:  # Se l'utente clicca su "No"
                print("Dati non salvati.")
                self.reset_button_click()

        #Acquisizione dei valori delle entry e controllo su di essi
        success = self.acquire_values()

        if(success == True):
            if self.ble_address != 0:
                messagebox.showerror("Errore", "Connessione ancora non possibile, disconnettersi e provare la simulazione" )
                
                #LETTURA DAL SERVER
                #self.lettura_completata = False
                #self.lettura_fallita = False
                #data = asyncio.run(self.read_data())
                
                #while (self.lettura_completata == False) and (self.lettura_fallita == False):
                    #pass
                
                #VADO IN DATA
                #self.show_frame(self.data_frame)

                #AGGIORNO GRAFICO E TABELLA CON VALORI LETTI
                #cont = 0

                #for element in data:
                    #cont = cont + 1
                    #self.x_values_BM.append(cont)
                    #self.y_values_BM.append(element)
                    #self.x_values_BF.append(cont)
                    #self.y_values_BF.append(element)
                    #self.x_values_N.append(cont)
                    #self.y_values_N.append(element)
                    #self.tree_indexes.append(cont)
                    #self.tree_values.append(element)
                    

                #self.init_graph_and_tree()


            else:
                #AREA TEST
                if(self.SERconnected == True):
                    self.open_popupSM() #apertura monitor seriale per input dati da inviare alla board
                #Passaggio alla schermata Data
                self.show_frame(self.data_frame)
                #self.open_popup_input()   #Per eseguire il test sul plottaggio dei grafici
                self.plotting = True
                thread = threading.Thread(target=lambda: asyncio.run(self.read_and_plot_live()))  # Esegui la scansione
                thread.daemon=True  # Impostiamo il thread come daemon per chiuderlo automaticamente alla fine del programma
                thread.start()
                 
    def acquire_values(self):
        success = False
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
                messagebox.showerror("Errore", e )
            else:
                success = True
                #Approssimo la tensione affinché la risoluzione sia di 10mV
                if ((voltage % 10) < 5):
                    voltage = voltage -(voltage % 10)
                else:
                    voltage = voltage -(voltage % 10) + 10
                
                #Stampa input
                print(f"Visualizzazione dei dati inseriti...\n")
                print(f"Tensione: ",voltage, "mV")
                print(f"Frequenza: ",frequency, "Hz")

            finally:
                return success
        
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
                messagebox.showerror("Errore", e)
            else:
                success = True
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
            finally:
                return success
       
    def exit_button_click(self):
        print("Exit")
        self.on_closing()
        
    def on_closing(self):
        time.sleep(1/10)
        self.destroy()
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

        #Reset tabelle
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.tree_indexes = []
        self.tree_values = []

        for item in self.Bode_markers_tree.get_children():
            self.Bode_markers_tree.delete(item)
        
        self.Bode_markers_tree_frequencies = []
        self.Bode_markers_tree_amplitudes = []
        self.Bode_markers_tree_phases = []

        for item in self.Nyquist_markers_tree.get_children():
            self.Nyquist_markers_tree.delete(item)

        self.Nyquist_markers_tree_reals = []
        self.Nyquist_markers_tree_immaginaries = []

        #PROVVISORIO
        self.ascissa=1

    def stop_button_click(self):
        print("Stop")
        self.plotting = False

    def toggle_add_marker(self):
        """Alterna lo stato di add_marker_enabled quando il pulsante viene premuto."""
        self.add_marker_enabled = not self.add_marker_enabled

        if self.add_marker_enabled:
            self.add_marker_button.config(bg="green", text="Add Marker (Enabled)")  # Cambia il colore e testo
        else:
            self.add_marker_button.config(bg="yellow", text="Add Marker (Disabled)")  # Cambia il colore e testo

    def saveData_button_click(self):
        print("Save Data")
        #TBD: salva dati inseriti in tabelle marker esportando in file csv/txt
        # e mostra il contenuto dei salvataggi nel frame data saved nella home tab

    def update_button_click(self):
        #Cattura del valore della resistenza inserito dal popup
        try:
            resistance=float(self.new_resistance.get())
            if (resistance < 1 or resistance > 500):
                    raise ValueError("il valore della rsistenza deve essere compreso tra 1 Ohm e 500 Ohm")
        except ValueError as e:
                print("Error:",e)
                print("Reinserire il valore")
                messagebox.showerror("Errore", e)
        else:
            self.update_graph_and_tree(resistance)

#Funzioni Inizializzazione e modifica grafici      
    def init_graph_and_tree(self):
        self.update_graph(self.ax_BM, self.canvas_BM, self.x_values_BM, self.y_values_BM, "Modulo")
        self.update_graph(self.ax_BF, self.canvas_BF, self.x_values_BF, self.y_values_BF, "Fase")
        self.update_graph(self.ax_N, self.canvas_N, self.x_values_N, self.y_values_N, "")

        i = 0
        for element in self.tree_indexes:
            self.tree.insert("","end", values=(self.tree_indexes[i], self.tree_values[i]))
            i = i + 1

    def update_graph(self, ax, canvas, x_values, y_values, title):
        #Aggiorno il grafico
        ax.clear()
        ax.plot(x_values, y_values, marker = '.')
        ax.set_title(title)
        ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')  # Griglia personalizzata
        canvas.draw_idle()

    def update_graph_and_tree(self, new_value):
        #Aggiorno la tabbella
        self.tree.insert("","end", values=(self.ascissa, new_value))
        self.tree_indexes.append(self.ascissa)
        self.tree_values.append(new_value)

        #Aggiorno i gragici
        #Bode Modulo
        self.x_values_BM.append(self.ascissa)   #DA MODIFICARE
        self.y_values_BM.append(new_value)     #DA MODIFICARE

        self.update_graph(self.ax_BM, self.canvas_BM, self.x_values_BM, self.y_values_BM, "Modulo")
            
        #Bode Fase
        self.x_values_BF.append(self.ascissa)   #DA MODIFICARE
        self.y_values_BF.append(new_value)     #DA MODIFICARE

        self.update_graph(self.ax_BF, self.canvas_BF, self.x_values_BF, self.y_values_BF, "Fase")

        #Nyquist
        self.x_values_N.append(self.ascissa)    #DA MODIFICARE
        self.y_values_N.append(new_value)      #DA MODIFICARE

        self.update_graph(self.ax_N, self.canvas_N, self.x_values_N, self.y_values_N, "")

        #Incremento il valore PROVVISORIO dell'ascissa
        self.ascissa=self.ascissa+1

    def connect_click_marker(self, event):
        """Metodo riutilizzabile per gestire il clic su un grafico."""
        if not self.add_marker_enabled:
            return  # Se la modalità non è attivata, non fare nulla

        # Verifica su quale grafico è stato fatto il clic
        if event.inaxes == self.ax_BM or event.inaxes == self.ax_BF:

            pointM = self.add_marker(self.canvas_BM, self.x_values_BM, self.y_values_BM, self.ax_BM, event)
            pointF = self.add_marker(self.canvas_BF, self.x_values_BF, self.y_values_BF, self.ax_BF, event)

            if (pointM is not None) and (pointF is not None):
                frequency = pointM[0]
                amplitude = pointM[1]
                phase = pointF[1]
                if frequency not in self.Bode_markers_tree_frequencies:
                    self.Bode_markers_tree.insert("", "end", values=(frequency, amplitude, phase))
                    self.Bode_markers_tree_frequencies.append(frequency)
                    self.Bode_markers_tree_amplitudes.append(amplitude)
                    self.Bode_markers_tree_phases.append(phase)

        elif event.inaxes == self.ax_N:
            pointN = self.add_marker(self.canvas_N, self.x_values_N, self.y_values_N, self.ax_N, event)

            if pointN is not None:
                real = pointN[0]
                immaginary = pointN[1]
                self.Nyquist_markers_tree.insert("", "end", values=(real, immaginary))
                self.Nyquist_markers_tree_reals.append(real)
                self.Nyquist_markers_tree_immaginaries.append(immaginary)

    def add_marker(self, canvas, x_data, y_data, ax, event,):
        """Aggiungi il marker solo se il clic è vicino ai punti esistenti nel grafico."""
        x_click = event.xdata
        y_click = event.ydata

        if x_click is None or y_click is None:
            print("Clic fuori dal grafico")
            return None

        # Distanza minima per considerare "vicino"
        max = self.tree_indexes[-1]

        threshold = 0.025 * max # Puoi regolare questo valore in base alla densità dei punti

        # Trova il punto più vicino tra i punti definiti
        closest_point = None
        min_distance = float('inf')  # Inizialmente impostata a infinito

        for i in range(len(x_data)):
            # Calcola la distanza euclidea (in R) tra il clic e il punto corrente
            distance = math.sqrt((x_data[i] - x_click) ** 2 )
            if distance < min_distance and distance <= threshold:
                min_distance = distance
                closest_point = (x_data[i], y_data[i])

        if closest_point:
        # Posiziona il marker esattamente sul punto trovato
            print(f"Aggiunto marker su {closest_point}")
            ax.plot(closest_point[0], closest_point[1], 'ro')  # Marker rosso

            # Aggiorna il grafico
            canvas.draw_idle()
            return closest_point

        # Mostra il messaggio di errore se il clic non è abbastanza vicino a nessun punto
        self.show_incorrect_mark()
        return None

    def show_incorrect_mark(self):
        """Mostra un pop-up di errore se il clic non è preciso."""
        messagebox.showerror(
        "Errore", 
        "Clic troppo lontano dai punti esistenti!\nPer favore, clicca più vicino a un punto del grafico."
    )

    #Funzioni di apertura/chiusura popup
    def open_popup_input(self):
        #Creazione del popup
        self.popup_input = tk.Toplevel()
        self.popup_input.title("Aggiunta valori ...")


        self.new_resistance= tk.StringVar()
        

        Testo_popup=tk.Label(self.popup_input, text="Il nuovo valore della Resistenza (deve essere compreso tra 1 e 500 Ohm):")
        Testo_popup.pack(pady=10)
        entry = tk.Entry(self.popup_input, textvariable=self.new_resistance)
        entry.pack(pady=10, padx=5)

        update_button = tk.Button(self.popup_input, text="Aggiorna", command=self.update_button_click)
        update_button.pack(pady=10)

    def open_popup_dati(self):
        # Crea la finestra di popup
        self.popup_dati = tk.Toplevel()
        self.popup_dati.title("Popup Dati")
        self.popup_dati.geometry("400x300")
        self.popup_dati.rowconfigure(0, weight=1)
        self.popup_dati.columnconfigure(1, weight=1)

        global popup_dati_aperto
        popup_dati_aperto = True


        # Frame per i dati
        data_frame = ttk.LabelFrame(self.popup_dati, text="Dati")
        data_frame.grid(column=0, row=0, columnspan=2, padx=10, pady=5, sticky="nesw")

        # Configurazione griglia
        data_frame.rowconfigure(0, weight=1)
        data_frame.rowconfigure(1, weight=0)
        data_frame.columnconfigure(0, weight=1)
        data_frame.columnconfigure(1, weight=1)

        # Area di testo per inserire/leggere dati
        self.data_text = tk.Text(data_frame, wrap="word", height=10, width=40)
        self.data_text.grid(column=0, row=0, columnspan=2, padx=10, pady=5, sticky="nesw")

        # Funzione per leggere i dati dal dispositivo
        async def on_read_data():
            data = await self.read_data()  # Chiama la funzione di lettura async
            self.data_text.delete("1.0", tk.END)  # Pulisci i dati precedenti
            self.data_text.insert(tk.END, str(data))  # Mostra i nuovi dati letti

        # Funzione per scrivere i dati
        async def on_write_data():
            command = b'\x01'  # Esempio di comando
            await self.write_data(command)  # Chiama la funzione di scrittura async

        # Pulsante per leggere i dati
        read_button = ttk.Button(data_frame, text="Leggi Dati", command=lambda: asyncio.run(on_read_data()))
        read_button.grid(column=0, row=1, padx=10, pady=5, sticky="nesw")

        # Pulsante per scrivere i dati
        write_button = ttk.Button(data_frame, text="Scrivi Dati", command=lambda: asyncio.run(on_write_data()))
        write_button.grid(column=1, row=1, padx=10, pady=5, sticky="nesw")

        def close_popup_data():
            print("Chiusura finestra dati")
            global popup_dati_aperto
            popup_dati_aperto = False
            self.popup_dati.destroy()

        self.popup_dati.protocol("WM_DELETE_WINDOW", close_popup_data)

    def open_device_list_popup(self):
        # Crea un nuovo popup
        self.popup_scan = tk.Toplevel(self)
        self.popup_scan.title("Dispositivi trovati")
        self.popup_scan.geometry("300x200")

        # Configura il layout del popup
        self.popup_scan.grid_rowconfigure(0, weight=1)  # Permette al Listbox di espandersi
        self.popup_scan.grid_rowconfigure(1, weight=0)
        self.popup_scan.grid_columnconfigure(0, weight=1)  # Permette al Listbox di espandersi
        self.popup_scan.columnconfigure(1, weight=1)

        # Variabile per memorizzare il nome e l'indirizzo MAC del dispositivo selezionato 
        self.selected_mac = tk.StringVar()
        self.selected_name = tk.StringVar()
        
        # Crea un Listbox per mostrare i dispositivi
        self.device_listbox = tk.Listbox(self.popup_scan)
        self.device_listbox.rowconfigure(0,weight=1)
        self.device_listbox.grid(row=0, columnspan=2, padx=5,pady=2,sticky='nesw')
            
        # Aggiungi i dispositivi trovati al Listbox

        self.device_listbox.insert(tk.END, "Scanning for devices...")  # Aggiungi alla lista
        
        def update_selected_mac(event):
            try:
                # Ottieni l'indice della selezione
                selected_index = self.device_listbox.curselection()[0]
                selected_device = self.found_devices[selected_index]
                self.selected_name.set(selected_device.name)
                self.selected_mac.set(selected_device.address)
                self.connect_button.config(state=tk.NORMAL)  # Abilita il pulsante Connetti
            except IndexError:
                self.selected_mac.set("")
                self.connect_button.config(state=tk.DISABLED)  # Disabilita il pulsante Connetti

        # Associa la funzione di selezione alla Listbox
        self.device_listbox.bind("<<ListboxSelect>>", update_selected_mac)
        
        async def connect_to_device():
            mac_address = self.selected_mac.get()

            if not mac_address:
                messagebox.showwarning("Errore", "Nessun dispositivo selezionato!")
                return

            try:
                # Usa BleakClient per connettersi al dispositivo BLE
                async with BleakClient(mac_address) as client:
                    connected = await client.is_connected()
                    if connected:
                        messagebox.showinfo("Successo", f"Connesso al dispositivo {mac_address}")
                        self.ble_name = self.selected_name.get()
                        self.ble_address = mac_address
                    else:
                        messagebox.showerror("Errore", f"Connessione fallita al dispositivo {mac_address}")
            except Exception as e:
                messagebox.showerror("Errore", f"Errore durante la connessione: {e}")

        def connect_button_handler():
           # asyncio.run(connect_to_device())
            self.ble_address = self.selected_mac
            self.ble_name = self.selected_name
            global popup_dati_aperto

            if self.connected == False or popup_dati_aperto == False:
                self.open_popup_dati()
                self.switch_bluetooth_frame(True)
                self.connected = True
                popup_dati_aperto = True
            else:
                self.popup_dati.destroy()
                self.open_popup_dati()

        #Pulsante per aggiornare il pop up
        self.update_button = tk.Button(self.popup_scan, text="Aggiorna", command=self.update_device_listbox)
        self.update_button.grid(row=1, column=1, padx=10, pady=5, sticky="nesw")  

        #Pulsante per connettersi al dispositivo selezionato
        self.connect_button = tk.Button(self.popup_scan, text="Connetti", command=connect_button_handler)
        self.connect_button.grid(row=1, column=0, padx=10, pady=5, sticky="nesw")  

        #Funzione per la chiusura del popup affinché pop_aperto venga modificato
        def close_popup():
            print("Chiusura finestra bluetooth")
            global popup_scan_aperto
            popup_scan_aperto = False
            self.popup_scan.destroy()
           

        
        #Affinché la variabile popup_aperto si modifichi anche se chiudo la finestra
        self.popup_scan.protocol("WM_DELETE_WINDOW", close_popup)
   
    def open_popupSM(self):
        global popup_SM_aperto

        # Controlla se il popup è già aperto
        if not popup_SM_aperto:
            print("Apertura Monitor Seriale per comunicazione con board.")
            self.create_popup_SM()
        else:
            risposta = messagebox.askyesno(
                "Conferma nuova comunicazione con board", 
                "Esiste una comunicazione in corso.\nVuoi comunque crearne una nuova?"
            )
            if risposta:  # Se l'utente clicca su "Sì"
                self.close_popup_SM()
                self.create_popup_SM()  # Riapre il popup
            else:  # Se l'utente clicca su "No"
                print("Creazione nuova comunicazione fallita.")

    def create_popup_SM(self):
        global popup_SM_aperto
        popup_SM_aperto = True

        self.popup_SM = tk.Toplevel(self)
        self.popup_SM.rowconfigure(0, weight=1)
        self.popup_SM.columnconfigure(0, weight=1)
        self.popup_SM.title("Monitor Seriale in comunicazione con ESP32")

        # Frame per i dati
        data_frame = ttk.LabelFrame(self.popup_SM, text="Dati monitor seriale")
        data_frame.grid(column=0, row=0, columnspan=2, padx=10, pady=5, sticky="nesw")

        # Configurazione griglia
        data_frame.rowconfigure(0, weight=0)
        data_frame.rowconfigure(1, weight=1)
        data_frame.rowconfigure(2, weight=0)
        data_frame.columnconfigure(0, weight=1)
        data_frame.columnconfigure(1, weight=1)

        frequency_label = tk.Label(data_frame, text="Insert semi-period(ms):", font=("Arial", 12))
        frequency_label.grid(column=0, row=0, padx=10, pady=5, sticky="nesw")

        self.frequency_entry = ttk.Entry(data_frame)
        self.frequency_entry.grid(column=1, row=0, padx=10, pady=5, sticky="nesw")

         # Area di testo per inserire/leggere dati
        self.data_text = tk.Text(data_frame, wrap="word", height=10, width=40)
        self.data_text.grid(column=0, row=1, columnspan=2, padx=10, pady=5, sticky="nesw")

        def send_frequency():
            try:
                #Fase di inserimento controllata a valori compresi tra 20 (minimo semi-periodo percettibile in maniera evidente) e 10000
                frequency = float (self.frequency_entry.get())
                if frequency < 20 or frequency >10000:
                    raise ValueError("Il valore del semiperiodo deve essere compreso tra 20 e 10000ms.\n")
                

                self.ser.write(f"{frequency}\n".encode())  # Invia la frequenza come stringa
                print(f"Semiperiodo inviato: {frequency} ms")
                self.data_text.insert(tk.END, f"Semiperiodo inviato: {frequency} ms \n")
                time.sleep(1/10)
        
                # Legge la frequenza corrente dall'ESP32
                if self.ser.in_waiting > 0:
                    try:
                        current_frequency =self. ser.readline().decode('utf-8').strip()
                        if not current_frequency or current_frequency == "E (89) psram: PSRAM ID read error: 0xffffffff" or current_frequency =="eE (89) psram: PSRAM ID read error: 0xffffffff":
                            raise ValueError()
                    except (serial.SerialException, ValueError) as e:
                        current_frequency = self.ser.readline().decode('utf-8').strip()

                            
                    print(f"Semiperiodo corrente ricevuto: {current_frequency} ms")
                    self.data_text.insert(tk.END, f"Semiperiodo corrente ricevuto: {current_frequency} ms \n")
            except ValueError as e:
                print(e)
                self.data_text.insert(tk.END, e)
            
        blinkFrequency_button = ttk.Button(
            data_frame, text="Aggiorna Frequenza Blink",
            command=send_frequency)
        blinkFrequency_button.grid(column=0, row=2, columnspan = 2, padx=20, pady=5, sticky="nesw")

        # Imposta il protocollo per chiudere correttamente la finestra
        self.popup_SM.protocol("WM_DELETE_WINDOW", self.close_popup_SM)

    def close_popup_SM(self):
        global popup_SM_aperto
        print("Chiusura finestra Monitor Seriale")
        popup_SM_aperto = False
        if hasattr(self, 'popup_SM') and self.popup_SM.winfo_exists():
            self.popup_SM.destroy()

#Funzioni implementative logica Server-Client
    def run_scanning(self):
        global popup_scan_aperto
        if popup_scan_aperto:
            print("Finestra Bluetooth già aperta, chiudere la finestra prima di effettuare un'altra scansione")
            messagebox.showerror("Error","Finestra Bluetooth già aperta, chiudere la finestra prima di effettuare un'altra scansione!")
            return
        elif popup_scan_aperto == False:
            popup_scan_aperto = True
            self.open_device_list_popup()
            print("Starting scanning...")
            thread = threading.Thread(target=lambda: asyncio.run(self.scan_for_devices_and_update()))  # Esegui la scansione
            thread.start()
            
    def update_device_listbox(self):
            print("Starting scanning...")
            # Esegui una nuova scansione e aggiorna la lista
            thread = threading.Thread(target=lambda: asyncio.run(self.scan_for_devices_and_update()))  # Esegui la scansione
            thread.start()

    async def scan_for_devices_and_update(self):
            self.device_listbox.delete(0, tk.END)  # Cancella la lista precedente
            self.device_listbox.insert(tk.END, "Scanning for devices...")
            self.update_button.config(state=tk.DISABLED)
            self.connect_button.config(state=tk.DISABLED)

            print("Scanning for devices...")
            self.found_devices = await BleakScanner.discover()  # Scansione dei dispositivi
            print("Fine scansione")

            self.device_listbox.delete(0, tk.END)  # Cancella la lista precedente
            for device in self.found_devices:
                self.device_listbox.insert(tk.END, f"{device.name} ({device.address})")  # Aggiungi i nuovi dispositivi
            self.update_button.config(state=tk.NORMAL)
            self.connect_button.config(state=tk.NORMAL)

    async def read_and_plot_live(self):
            while(self.plotting == True):
             self.new_resistance = random.randint(1, 500)
             self.update_graph_and_tree(self.new_resistance)
             if(self.mode == "Single Mode"):
                frequency = int(self.frequency_str.get())
                time.sleep(1 / frequency)
             else:
                frequency = int(self.mfrequency_str.get())
                time.sleep(1 / frequency)

#Funzione per connessione Server/Client (vedasi codice serverprototipo.py) funzionante ma non implementata causa limitazioni hardware/software
#   async def connect_to_device(address): #richiede l'indirizzo MAC del dispositivo
#        client = BleakClient(address)
#        try:
#            await client.connect()
#            print("Connessione al dispositivo riuscita!")
#        except Exception as e:
#            print(f"Errore di connessione: {e}")
#        return client

    # Funzione per scrivere i dati
    async def write_data(self, command):
        """Scrivi i dati utilizzando un comando"""
        try:
            await self.write_command(self.client, self.characteristic_uuid, command)
            print(f"Comando inviato: {command}")
        except Exception as e:
            print(f"Errore durante l'invio del comando: {e}")

    async def write_command(self, client, characteristic_uuid, command):
        """Invia un comando a una caratteristica GATT"""
        try:
            await client.write_gatt_char(characteristic_uuid, command)
            print(f"Comando inviato: {command}")
        except Exception as e:
            print(f"Errore durante l'invio del comando: {e}")

    # Funzione per leggere i dati
    async def read_data(self):
        """Leggi i dati da una caratteristica GATT"""
        try:
            data = await self.read_command(self.client, self.characteristic_uuid)
            print(f"Dati letti: {data}")
            self.lettura_completata = True
            return data
        except Exception as e:
            print(f"Errore durante la lettura dei dati: {e}")
            self.lettura_fallita = True

    async def read_command(self, client, characteristic_uuid):
        """Leggi i dati da una caratteristica GATT"""
        try:
            data = await client.read_gatt_char(characteristic_uuid)
            print(f"Dati letti: {data}")
            return data
        except Exception as e:
            print(f"Errore durante la lettura dei dati: {e}")

    # Funzione per scrivere i dati
    async def write_data(self, command):
        """Scrivi i dati utilizzando un comando"""
        try:
            await self.write_command(self.client, self.characteristic_uuid, command)
            print(f"Comando inviato: {command}")
        except Exception as e:
            print(f"Errore durante l'invio del comando: {e}")

    async def write_command(self, client, characteristic_uuid, command):
        """Invia un comando a una caratteristica GATT"""
        try:
            await client.write_gatt_char(characteristic_uuid, command)
            print(f"Comando inviato: {command}")
        except Exception as e:
            print(f"Errore durante l'invio del comando: {e}")

    # Funzione per leggere i dati
    async def read_data(self):
        """Leggi i dati da una caratteristica GATT"""
        try:
            data = await self.read_command(self.client, self.characteristic_uuid)
            print(f"Dati letti: {data}")
            return data
        except Exception as e:
            print(f"Errore durante la lettura dei dati: {e}")

    async def read_command(self, client, characteristic_uuid):
        """Leggi i dati da una caratteristica GATT"""
        try:
            data = await client.read_gatt_char(characteristic_uuid)
            print(f"Dati letti: {data}")
            return data
        except Exception as e:
            print(f"Errore durante la lettura dei dati: {e}")

#Funzione lettura porta seriale collegata ad esp32
    def find_esp32(self):
        ports = serial.tools.list_ports_windows.comports()
        for port in ports:
            if "USB" in port.description or "UART" in port.description:
                print(f"Trovato ESP32: {port.device} - {port.description}")
                return port.device
        print("Nessun ESP32 trovato!")
        return None
    
if __name__ == "__main__":
    app = InsulinometroApp()
    app.mainloop()
