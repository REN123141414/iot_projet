
#include <Wire.h>
#include <LiquidCrystal_AIP31068_I2C.h>

// Adresse I2C : 0x3E
// LCD : 16 colonnes et 2 lignes
LiquidCrystal_AIP31068_I2C lcd(0x3E, 16, 2);

void setup() {
  // Initialisation du LCD
  lcd.init();

  // Effacer l'ecran
  lcd.clear();

  // Premiere ligne
  lcd.setCursor(0, 0);
  lcd.print("HELLO");

  // Deuxieme ligne
  lcd.setCursor(9, 1);
  lcd.print("WORLD");
}

void loop() {
  // Aucun traitement en boucle
}
