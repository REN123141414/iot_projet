
#include <Wire.h>
#include <DHT.h>
#include <LiquidCrystal_AIP31068_I2C.h>

// Capteur DHT22 connecte a A0
#define DHTPIN A0
#define DHTTYPE DHT22

// Initialisation du capteur
DHT dht(DHTPIN, DHTTYPE);

// LCD I2C : adresse 0x3E, 16 colonnes, 2 lignes
LiquidCrystal_AIP31068_I2C lcd(0x3E, 16, 2);

void setup() {
  // Initialiser le capteur DHT22
  dht.begin();

  // Initialiser l'ecran LCD
  lcd.init();
  lcd.clear();

  // Afficher le titre sur la premiere ligne
  lcd.setCursor(2, 0);
  lcd.print("IMT NE - PPI");
}

void loop() {
  // Lire temperature et humidite
  float temperature = dht.readTemperature();
  float humidite = dht.readHumidity();

  // Effacer uniquement la deuxieme ligne
  lcd.setCursor(0, 1);
  lcd.print("                ");
  lcd.setCursor(0, 1);

  // Verifier si les mesures sont valides
  if (isnan(temperature) || isnan(humidite)) {
    lcd.print("Erreur DHT22");
  } else {
    // Afficher la temperature
    lcd.print("T ");
    lcd.print(temperature, 1);
    lcd.print("oC/H ");

    // Afficher l'humidite
    lcd.print(humidite, 1);
    lcd.print("%");
  }

  // Actualisation toutes les 2 secondes
  delay(2000);
}
