
#include <Wire.h>
#include <DHT.h>
#include <LiquidCrystal_AIP31068_I2C.h>
#include <stdio.h>

// ===== Configuration =====

#define DHTPIN A0
#define DHTTYPE DHT22

#define LED_VIE 13
#define BAR_START 3
#define BAR_COUNT 10

DHT dht(DHTPIN, DHTTYPE);
LiquidCrystal_AIP31068_I2C lcd(0x3E, 16, 2);

// ===== Horloge logicielle =====
// Date initiale de demonstration
int jour = 10;
int mois = 2;
int annee = 25;

int heure = 13;
int minute = 42;
int seconde = 29;

// ===== Temporisations =====

unsigned long dernierClignotement = 0;
unsigned long derniereSeconde = 0;
unsigned long derniereMesure = 0;

bool etatLed = false;

// ===== Avancer l'horloge =====

void avancerHorloge() {
  seconde++;

  if (seconde >= 60) {
    seconde = 0;
    minute++;
  }

  if (minute >= 60) {
    minute = 0;
    heure++;
  }

  if (heure >= 24) {
    heure = 0;
    jour++;
  }

  // Chaque mois contient 30 jours
  if (jour > 30) {
    jour = 1;
    mois++;
  }

  if (mois > 12) {
    mois = 1;
    annee++;
  }
}

// ===== Afficher la date et l'heure =====

void afficherHorloge() {
  char texte[18];

  // Adapter le format aux 16 colonnes
  if (mois < 10) {
    snprintf(texte, sizeof(texte),
             "%02d/%d/%02d %02d:%02d:%02d",
             jour, mois, annee,
             heure, minute, seconde);
  } else {
    snprintf(texte, sizeof(texte),
             "%02d/%02d/%02d%02d:%02d:%02d",
             jour, mois, annee,
             heure, minute, seconde);
  }

  lcd.setCursor(0, 0);
  lcd.print("                ");
  lcd.setCursor(0, 0);
  lcd.print(texte);
}

// ===== Afficher les mesures =====

void afficherMesures(float t, float h) {
  lcd.setCursor(0, 1);
  lcd.print("                ");
  lcd.setCursor(0, 1);

  lcd.print("T ");
  lcd.print(t, 1);
  lcd.print("oC/H ");
  lcd.print(h, 1);
  lcd.print("%");
}

// ===== Bargraphe de temperature =====

void afficherBargraphe(float temperature) {
  // 0 a 40 degres -> 0 a 10 LEDs
  int nombre = (int)(temperature / 4.0 + 0.5);
  nombre = constrain(nombre, 0, BAR_COUNT);

  for (int i = 0; i < BAR_COUNT; i++) {
    digitalWrite(BAR_START + i,
                 i < nombre ? HIGH : LOW);
  }
}

// ===== Initialisation =====

void setup() {
  Serial.begin(9600);

  pinMode(LED_VIE, OUTPUT);
  digitalWrite(LED_VIE, LOW);

  for (int i = 0; i < BAR_COUNT; i++) {
    pinMode(BAR_START + i, OUTPUT);
    digitalWrite(BAR_START + i, LOW);
  }

  dht.begin();
  lcd.init();
  lcd.clear();

  afficherHorloge();
  lcd.setCursor(0, 1);
  lcd.print("Attente DHT22...");

  dernierClignotement = millis();
  derniereSeconde = millis();
  derniereMesure = millis();
}

// ===== Boucle principale =====

void loop() {
  unsigned long maintenant = millis();

  // LED de vie : 2 Hz
  if (maintenant - dernierClignotement >= 250) {
    dernierClignotement += 250;

    etatLed = !etatLed;
    digitalWrite(LED_VIE, etatLed);
  }

  // Horloge : chaque seconde
  if (maintenant - derniereSeconde >= 1000) {
    derniereSeconde += 1000;

    avancerHorloge();
    afficherHorloge();
  }

  // DHT22 : toutes les 2 secondes
  if (maintenant - derniereMesure >= 2000) {
    derniereMesure += 2000;

    float t = dht.readTemperature();
    float h = dht.readHumidity();

    if (isnan(t) || isnan(h)) {
      lcd.setCursor(0, 1);
      lcd.print("Erreur DHT22    ");
      Serial.println("Erreur DHT22");
    } else {
      afficherMesures(t, h);
      afficherBargraphe(t);

      // Envoi des mesures par le port serie
      Serial.print(jour);
      Serial.print("/");
      Serial.print(mois);
      Serial.print("/");
      Serial.print(2000 + annee);
      Serial.print(" ");

      Serial.print(heure);
      Serial.print(":");
      Serial.print(minute);
      Serial.print(":");
      Serial.print(seconde);

      Serial.print(" | T=");
      Serial.print(t, 1);
      Serial.print(" C | H=");
      Serial.print(h, 1);
      Serial.println(" %");
    }
  }

  delay(10);
}
