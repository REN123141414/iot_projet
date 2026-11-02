/*
 * TempHumiX - Phase 2, TP 6.1.1 (Arduino UNO R4 WiFi)
 * Adapte du fichier temphumix.ino de la premiere phase.
 *
 * - DHT22 : acquisition toutes les ~2000 ms
 * - Grove LCD 16x2 (White on Blue) : affichage temperature / humidite
 * - LED : clignotement 2 Hz (250 ms ON, 250 ms OFF)
 * - Une iteration de loop dure environ 500 ms (+ temps de lecture DHT)
 *
 * IMPORTANT : A0 et D13 proviennent du programme de simulation.
 * Il faut verifier que le boitier reel utilise bien ces broches.
 * Le bargraphe D3-D12 n'est PAS pilote tant que le cablage reel
 * n'est pas confirme. Le RTC, le Wi-Fi et MQTT viendront ensuite.
 */

#include <Wire.h>
#include <DHT.h>
#include <rgb_lcd.h>

#define DHTPIN A0
#define DHTTYPE DHT22
#define LED_VIE 2

DHT dht(DHTPIN, DHTTYPE);
rgb_lcd lcd;

unsigned int compteur500ms = 0;

void afficherMesures(float temperature, float humidite) {
  lcd.setCursor(0, 1);
  lcd.print("                "); // Effacer les anciennes valeurs
  lcd.setCursor(0, 1);
  lcd.print("T:");
  lcd.print(temperature, 1);
  lcd.print("C H:");
  lcd.print(humidite, 1);
  lcd.print("%");
}

void lireCapteur() {
  float temperature = dht.readTemperature();
  float humidite = dht.readHumidity();

  if (isnan(temperature) || isnan(humidite)) {
    lcd.setCursor(0, 1);
    lcd.print("Erreur DHT22    ");
    Serial.println("Erreur DHT22 (verifier broche A0)");
    return;
  }

  afficherMesures(temperature, humidite);
  Serial.print("Temperature : ");
  Serial.print(temperature, 1);
  Serial.print(" C | Humidite : ");
  Serial.print(humidite, 1);
  Serial.println(" %");
}

void setup() {
  Serial.begin(9600);

  pinMode(LED_VIE, OUTPUT);
  digitalWrite(LED_VIE, LOW);

  dht.begin();
  Wire.begin();
  lcd.begin(16, 2);
  // Le Grove 16x2 White-on-Blue n'a pas de controle RGB.
  // Ne PAS appeler lcd.setRGB(...).
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("IMT NE - PPI");
  lcd.setCursor(0, 1);
  lcd.print("Attente DHT22...");
}

void loop() {
  // Une periode complete = 500 ms => 2 cycles par seconde = 2 Hz
  digitalWrite(LED_VIE, HIGH);
  delay(250);
  digitalWrite(LED_VIE, LOW);
  delay(250);

  // Machine d'etat : un tick toutes les ~500 ms.
  compteur500ms++;

  // 4 ticks x 500 ms = ~2000 ms entre deux mesures.
  if (compteur500ms >= 4) {
    compteur500ms = 0;
    lireCapteur();
  }
}