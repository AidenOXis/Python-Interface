import dbus
import dbus.mainloop.glib
import gi
from gi.repository import GLib
import random

# Inizializzazione del ciclo principale DBus
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
CHARACTERISTIC_UUID_READ = "12345678-1234-5678-1234-56789abcdef1"
CHARACTERISTIC_UUID_WRITE = "12345678-1234-5678-1234-56789abcdef2"

class Application(dbus.service.Object):
    def _init_(self, bus):
        self.path = "/test/service"
        dbus.service.Object._init_(self, bus, self.path)
        self.add_service()

    def add_service(self):
        self.service = MyService(self.bus, SERVICE_UUID)

class MyService(dbus.service.Object):
    def _init_(self, bus, uuid):
        self.path = "/test/service/myservice"
        dbus.service.Object._init_(self, bus, self.path)
        self.uuid = uuid
        self.characteristics = []

        # Aggiunge caratteristiche di lettura e scrittura
        self.add_characteristic(MyCharacteristic(self.bus, self, CHARACTERISTIC_UUID_READ, "read"))
        self.add_characteristic(MyCharacteristic(self.bus, self, CHARACTERISTIC_UUID_WRITE, "write"))

    def add_characteristic(self, characteristic):
        self.characteristics.append(characteristic)

class MyCharacteristic(dbus.service.Object):
    def _init_(self, bus, service, uuid, mode):
        self.path = f"{service.path}/char_{uuid}"
        dbus.service.Object._init_(self, bus, self.path)
        self.service = service
        self.uuid = uuid
        self.mode = mode
        self.value = [random.randint(0, 255)]

    @dbus.service.method("org.bluez.GattCharacteristic1", in_signature="", out_signature="ay")
    def ReadValue(self):
        if self.mode == "read":
            print("Leggendo il valore...")
            return dbus.ByteArray(self.value)
        return None

    @dbus.service.method("org.bluez.GattCharacteristic1", in_signature="ay")
    def WriteValue(self, value):
        if self.mode == "write":
            self.value = list(value)
            print(f"Nuovo valore scritto: {self.value}")

# Avvio del loop BLE
def main():
    bus = dbus.SystemBus()
    app = Application(bus)
    
    loop = GLib.MainLoop()
    print("Server BLE in esecuzione...")
    loop.run()

if _name_ == "_main_":
    main()
