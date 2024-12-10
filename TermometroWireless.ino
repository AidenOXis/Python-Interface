#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

// UUID del servizio e della caratteristica
#define SERVICE_UUID        "12345678-1234-1234-1234-123456789abc"
#define CHARACTERISTIC_UUID "abcdefab-cdef-abcd-efab-cdef12345678"
#define NAME "ESP32_Server (Gruppo V)"

#define START "1"
#define STOP "2"


bool state = false;
unsigned long lastSampleTime = 0;   // Timestamp dell'ultimo campionamento
unsigned long sampleInterval = 1000; // Intervallo di campionamento (in millisecondi)

#define LED 2

// Variabile globale per tracciare lo stato di connessione
bool deviceConnected = false;

// Variabile per conservare i dati ricevuti
std::string lastReceivedValue;

// Riferimento globale alla caratteristica BLE
BLECharacteristic *pCharacteristic;

// Classe per gestire i callback del server BLE
class ServerCallbacks : public BLEServerCallbacks {
  void onConnect(BLEServer* pServer) override {
    deviceConnected = true;
    digitalWrite(LED,HIGH);
    Serial.println("Dispositivo connesso.");
  }

  void onDisconnect(BLEServer* pServer) override {
    deviceConnected = false;
    Serial.println("Dispositivo disconnesso.");
    digitalWrite(LED, LOW);
    // Riavvia l'advertising per permettere nuove connessioni
    pServer->getAdvertising()->start();
    Serial.println("Advertising riavviato.");
  }
};

void sendSample(){
  unsigned long currentTime = millis();
  if (currentTime - lastSampleTime >= sampleInterval) {
    lastSampleTime = currentTime;
    // Legge la temperatura interna del sensore
    float chipTemperature = temperatureRead();

    // Stampa il valore su monitor seriale
    Serial.print("Temperatura interna del chip ESP32: ");
    Serial.print(chipTemperature);
    Serial.println(" °C");
    std::string sample = std::to_string(chipTemperature);
    pCharacteristic->setValue(sample);
    pCharacteristic->notify();
    Serial.print("Risposta inviata al client: ");
    Serial.println(sample.c_str());
    // Cambia lo stato del LED
    int ledState = digitalRead(LED);
    digitalWrite(LED, !ledState);

  }
  
}
      
void setup() {
  Serial.begin(115200);
  pinMode(LED, OUTPUT);
  delay(2000);
  Serial.println("Inizializzazione BLE...");

  // Inizializza il dispositivo BLE
  BLEDevice::init(NAME);
  BLEServer *pServer = BLEDevice::createServer();

  // Imposta i callback del server
  pServer->setCallbacks(new ServerCallbacks());

  // Crea un servizio BLE
  BLEService *pService = pServer->createService(SERVICE_UUID);

  // Crea una caratteristica BLE
  pCharacteristic = pService->createCharacteristic(
    CHARACTERISTIC_UUID,
    BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_WRITE | BLECharacteristic::PROPERTY_NOTIFY
  );


  // Avvia il servizio
  pService->start();

  // Avvia l'advertising BLE
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->start();

  Serial.println("ESP32 in modalità advertising BLE.");
}

void loop() {
  if (deviceConnected) {
    // Leggi il valore scritto dal client
    std::string currentValue = pCharacteristic->getValue();

    // Verifica se il valore è stato aggiornato
    if (currentValue != lastReceivedValue) {
      lastReceivedValue = currentValue; // Aggiorna l'ultimo valore ricevuto
      Serial.print("Messaggio ricevuto: ");
      Serial.println(lastReceivedValue.c_str());

      if (currentValue == START ){
        state = true;
        Serial.println("Inizio Campionamento");
      }

      if (currentValue == STOP && state == true){
        state = false;
        Serial.println("Fine Campionamento");
        digitalWrite(LED,HIGH);
      }

      
    }

    if(state){
      sendSample();
    }
    
  }

  delay(100); // Evita di sovraccaricare il loop
}
