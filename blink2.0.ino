int blinkFrequency = 1000;  // Frequenza di lampeggiamento predefinita (ms)
unsigned long previousMillis = 0; 
bool ledState = LOW;

void setup() {
  pinMode(2, OUTPUT);       // Usa il pin 2 per il LED
  Serial.begin(115200);     // Inizializza la comunicazione seriale
}

void loop() {
  // Controlla se c'è un comando in arrivo da Python
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');  // Legge il comando dalla seriale
    int newFrequency = input.toInt();            // Converte in un numero intero
    if (newFrequency > 0) {                      // Aggiorna solo se valido
      blinkFrequency = newFrequency;
      Serial.println(blinkFrequency);
    }
  }

  // Logica di lampeggiamento
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= blinkFrequency) {
    previousMillis = currentMillis;
    ledState = !ledState;          // Cambia stato LED
    digitalWrite(2, ledState);     // Imposta il LED
  }

  
}

