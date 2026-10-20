
#include <DHT.h>

#define DHTPIN A0
#define DHTTYPE DHT22

#define LED_VERTE 3
#define LED_ROUGE 12

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);

  pinMode(LED_VERTE, OUTPUT);
  pinMode(LED_ROUGE, OUTPUT);

  digitalWrite(LED_VERTE, LOW);
  digitalWrite(LED_ROUGE, LOW);

  dht.begin();
}

void loop() {
  float temperature = dht.readTemperature();

  if (isnan(temperature)) {
    Serial.println("Erreur DHT22");

    digitalWrite(LED_VERTE, LOW);
    digitalWrite(LED_ROUGE, LOW);
  }
  else if (temperature < 20.0) {
    // Temperature inferieure a 20 degres
    digitalWrite(LED_VERTE, HIGH);
    digitalWrite(LED_ROUGE, LOW);
  }
  else {
    // Temperature superieure ou egale a 20 degres
    digitalWrite(LED_VERTE, LOW);
    digitalWrite(LED_ROUGE, HIGH);
  }

  delay(2000);
}

