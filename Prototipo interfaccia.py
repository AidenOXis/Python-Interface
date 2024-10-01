import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import pandas as pd
from matplotlib.widgets import Cursor

class ImpedanceAnalyzerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Analizzatore di Impedenza")
        master.geometry("1200x800")

        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.graph_frame = ttk.Frame(self.main_frame)
        self.graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.control_frame = ttk.Frame(self.main_frame)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.create_graphs()
        self.create_controls()

        self.is_connected = False
        self.battery_level = 100
        self.data = {'frequencies': [], 'magnitude': [], 'phase': [], 'real': [], 'imag': []}
        self.is_acquiring = False

    def create_graphs(self):
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, figsize=(8, 12))

        self.ax1.set_title("Diagramma di Bode (Magnitude)")
        self.ax1.set_xlabel("Frequenza (Hz)")
        self.ax1.set_ylabel("Magnitude (dB)")
        self.ax1.set_xscale("log")

        self.ax2.set_title("Diagramma di Bode (Fase)")
        self.ax2.set_xlabel("Frequenza (Hz)")
        self.ax2.set_ylabel("Fase (gradi)")
        self.ax2.set_xscale("log")

        self.ax3.set_title("Diagramma di Nyquist")
        self.ax3.set_xlabel("Parte Reale")
        self.ax3.set_ylabel("Parte Immaginaria")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.graph_frame)
        self.toolbar.update()

        self.cursor1 = Cursor(self.ax1, useblit=True, color='red', linewidth=1)
        self.cursor2 = Cursor(self.ax2, useblit=True, color='red', linewidth=1)
        self.cursor3 = Cursor(self.ax3, useblit=True, color='red', linewidth=1)

    def create_controls(self):
        ttk.Label(self.control_frame, text="Modalità di Acquisizione").pack()
        self.acquisition_mode = ttk.Combobox(self.control_frame, values=["Singola frequenza", "Sweep Mode"])
        self.acquisition_mode.pack()
        self.acquisition_mode.bind("<<ComboboxSelected>>", self.update_frequency_inputs)

        self.freq_frame = ttk.Frame(self.control_frame)
        self.freq_frame.pack()

        ttk.Label(self.freq_frame, text="Frequenza (Hz)").pack()
        self.frequency_entry = ttk.Entry(self.freq_frame)
        self.frequency_entry.pack()

        self.start_freq_entry = ttk.Entry(self.freq_frame)
        self.end_freq_entry = ttk.Entry(self.freq_frame)
        self.step_freq_entry = ttk.Entry(self.freq_frame)

        ttk.Label(self.control_frame, text="Ampiezza (mV)").pack()
        self.amplitude_entry = ttk.Entry(self.control_frame)
        self.amplitude_entry.pack()

        ttk.Label(self.control_frame, text="Stato Connessione").pack()
        self.connection_status = ttk.Label(self.control_frame, text="Disconnesso")
        self.connection_status.pack()

        ttk.Button(self.control_frame, text="Connetti Bluetooth", command=self.connect_bluetooth).pack()
        ttk.Button(self.control_frame, text="Disconnetti", command=self.disconnect).pack()

        ttk.Button(self.control_frame, text="Esporta Dati", command=self.export_data).pack()
        ttk.Button(self.control_frame, text="Reset Buffer", command=self.reset_buffer).pack()
        ttk.Button(self.control_frame, text="Avvia Acquisizione", command=self.start_acquisition).pack()

        self.progress_bar = ttk.Progressbar(self.control_frame, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.pack()

        #self.battery_label = ttk.Label(self.control_frame, text=f"Batteria: {self.battery_level}%")
        #self.battery_label.pack()

    def update_frequency_inputs(self, event):
        for widget in self.freq_frame.winfo_children():
            widget.pack_forget()

        if self.acquisition_mode.get() == "Singola frequenza":
            ttk.Label(self.freq_frame, text="Frequenza (Hz)").pack()
            self.frequency_entry.pack()
        else:
            ttk.Label(self.freq_frame, text="Frequenza iniziale (Hz)").pack()
            self.start_freq_entry.pack()
            ttk.Label(self.freq_frame, text="Frequenza finale (Hz)").pack()
            self.end_freq_entry.pack()
            ttk.Label(self.freq_frame, text="Step (Hz)").pack()
            self.step_freq_entry.pack()

    def connect_bluetooth(self):
        self.is_connected = True
        self.connection_status.config(text="Connesso via Bluetooth")
        self.simulate_battery_drain()

    def disconnect(self):
        self.is_connected = False
        self.connection_status.config(text="Disconnesso")

    def export_data(self):
        if not self.data['frequencies']:
            messagebox.showwarning("Nessun dato", "Non ci sono dati da esportare.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            df = pd.DataFrame(self.data)
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Esportazione completata", f"Dati esportati in {file_path}")

    def reset_buffer(self):
        self.data = {'frequencies': [], 'magnitude': [], 'phase': [], 'real': [], 'imag': []}
        self.update_graphs()
        messagebox.showinfo("Reset completato", "Il buffer è stato resettato.")

    def start_acquisition(self):
        if not self.is_connected:
            messagebox.showerror("Errore", "Connettiti prima di iniziare l'acquisizione.")
            return

        self.is_acquiring = True
        if self.acquisition_mode.get() == "Singola frequenza":
            self.acquire_single_frequency()
        else:
            self.acquire_sweep()

    def acquire_single_frequency(self):
        try:
            freq = float(self.frequency_entry.get())
            amp = float(self.amplitude_entry.get())
        except ValueError:
            messagebox.showerror("Errore", "Inserisci valori numerici validi per frequenza e ampiezza.")
            return

        # Simulazione dell'acquisizione dati
        magnitude = -20 * np.log10(freq)
        phase = -90
        real = 1 / (1 + freq)
        imag = -freq / (1 + freq)

        self.data['frequencies'].append(freq)
        self.data['magnitude'].append(magnitude)
        self.data['phase'].append(phase)
        self.data['real'].append(real)
        self.data['imag'].append(imag)

        self.update_graphs()

    def acquire_sweep(self):
        try:
            start_freq = float(self.start_freq_entry.get())
            end_freq = float(self.end_freq_entry.get())
            step = float(self.step_freq_entry.get())
            amp = float(self.amplitude_entry.get())
        except ValueError:
            messagebox.showerror("Errore", "Inserisci valori numerici validi per tutte le frequenze e l'ampiezza.")
            return

        frequencies = np.arange(start_freq, end_freq + step, step)
        total_steps = len(frequencies)

        for i, freq in enumerate(frequencies):
            # Simulazione dell'acquisizione dati
            magnitude = -20 * np.log10(freq)
            phase = -90
            real = 1 / (1 + freq)
            imag = -freq / (1 + freq)

            self.data['frequencies'].append(freq)
            self.data['magnitude'].append(magnitude)
            self.data['phase'].append(phase)
            self.data['real'].append(real)
            self.data['imag'].append(imag)

            self.progress_bar['value'] = (i + 1) / total_steps * 100
            self.master.update_idletasks()

        self.update_graphs()

    def update_graphs(self):
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()

        self.ax1.set_title("Diagramma di Bode (Magnitude)")
        self.ax1.set_xlabel("Frequenza (Hz)")
        self.ax1.set_ylabel("Magnitude (dB)")
        self.ax1.set_xscale("log")
        self.ax1.plot(self.data['frequencies'], self.data['magnitude'])

        self.ax2.set_title("Diagramma di Bode (Fase)")
        self.ax2.set_xlabel("Frequenza (Hz)")
        self.ax2.set_ylabel("Fase (gradi)")
        self.ax2.set_xscale("log")
        self.ax2.plot(self.data['frequencies'], self.data['phase'])

        self.ax3.set_title("Diagramma di Nyquist")
        self.ax3.set_xlabel("Parte Reale")
        self.ax3.set_ylabel("Parte Immaginaria")
        self.ax3.plot(self.data['real'], self.data['imag'])

        self.canvas.draw()

    def simulate_battery_drain(self):
        if self.is_connected and self.battery_label:
            self.battery_level = max(0, self.battery_level - 1)
            self.battery_label.config(text=f"Batteria: {self.battery_level}%")
            self.master.after(10000, self.simulate_battery_drain)  # Aggiorna ogni 10 secondi

if __name__ == "__main__":
    root = tk.Tk()
    app = ImpedanceAnalyzerGUI(root)
    root.mainloop()
