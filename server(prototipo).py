import dbus
import dbus.mainloop.glib
import dbus.service
import gi
from gi.repository import GLib
import random

# Inizializzazione del ciclo principale DBus
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

SERVICE_UUID = "12345678_1234_5678_1234_56789abcdef0"
CHARACTERISTIC_UUID_READ = "12345678_1234_5678_1234_56789abcdef1"
CHARACTERISTIC_UUID_WRITE = "12345678_1234_5678_1234_56789abcdef2" 

class Application(dbus.service.Object):
    def __init__(self, bus):
        """Inizializza l'applicazione BLE e aggiunge il servizio."""
        self.path = "/test/service"
        super().__init__(bus, self.path)
        self.bus = bus
        self.add_service()

    def add_service(self):
        """Aggiunge un servizio BLE con un UUID specificato."""
        self.service = MyService(self.bus, SERVICE_UUID)

class MyService(dbus.service.Object):
    def __init__(self, bus, uuid):
        """Inizializza il servizio BLE con l'UUID dato e aggiunge le caratteristiche."""
        self.path = "/test/service/myservice"
        super().__init__(bus, self.path)
        self.uuid = uuid
        self.characteristics = []

        # Aggiunge caratteristiche di lettura e scrittura
        self.add_characteristic(MyCharacteristic(self.bus, self, CHARACTERISTIC_UUID_READ, "read"))
        self.add_characteristic(MyCharacteristic(self.bus, self, CHARACTERISTIC_UUID_WRITE, "write"))

    def add_characteristic(self, characteristic):
        """Aggiunge una caratteristica alla lista delle caratteristiche del servizio."""
        self.characteristics.append(characteristic)

class MyCharacteristic(dbus.service.Object):
    def __init__(self, bus, service, uuid, mode):
        """Inizializza una caratteristica BLE con modalità di lettura o scrittura."""
        if mode not in ["read", "write"]:
            raise ValueError("Il mode deve essere 'read' o 'write'.")

        self.path = f"{service.path}/char_{uuid}"
        super().__init__(bus, self.path)
        self.service = service
        self.uuid = uuid
        self.mode = mode
        self.value = [random.randint(0, 255)]  # Valore iniziale casuale

    @dbus.service.method("org.bluez.GattCharacteristic1", in_signature="", out_signature="ay")
    def ReadValue(self):
        """Legge il valore della caratteristica, se è in modalità 'read'."""
        if self.mode == "read":
            print(f"Leggendo il valore dalla caratteristica {self.uuid}...")
            return dbus.ByteArray(self.value)
        print("Errore: tentativo di lettura su una caratteristica non leggibile.")
        return None

    @dbus.service.method("org.bluez.GattCharacteristic1", in_signature="ay")
    def WriteValue(self, value):
        """Scrive un nuovo valore sulla caratteristica, se è in modalità 'write'."""
        if self.mode == "write":
            self.value = list(value)
            print(f"Nuovo valore scritto sulla caratteristica {self.uuid}: {self.value}")
        else:
            print("Errore: tentativo di scrittura su una caratteristica non scrivibile.")

# Avvio del loop BLE
def main():
    bus = dbus.SystemBus()
    app = Application(bus)
    
    loop = GLib.MainLoop()
    print("Server BLE in esecuzione...")
    loop.run()

if __name__ == "__main__":
    main()
