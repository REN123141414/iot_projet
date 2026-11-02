#include "arduino_secrets.h"

/*
 * Projet IoT - TP 6.1.3
 * Arduino UNO R4 WiFi - TempHumiX
 *
 * WiFi + NTP + RTC + DHT22 + LCD + LED
 *
 * Serveur NTP : 192.168.1.254
 * DHT22       : A0
 * LED_VIE     : D2 (active LOW)
 * LCD         : I2C 16x2
 */

#include <WiFiS3.h>
#include <WiFiUdp.h>
#include <NTPClient.h>
#include <Wire.h>
#include <rgb_lcd.h>
#include <DHT.h>
#include "RTC.h"

// ====================================
// 1. Configuration
// ====================================




#define DHTPIN A0
#define DHTTYPE DHT22
#define LED_VIE 2

DHT dht(DHTPIN, DHTTYPE);
rgb_lcd lcd;

WiFiUDP ntpUDP;

// Nouvelle adresse NTP donnee par le professeur
NTPClient ntp(
  ntpUDP,
  IPAddress(192, 168, 1, 254),
  0,
  60000
);

// ====================================
// 2. Variables globales
// ====================================

bool wifiConnecte = false;
bool ntpDemarre = false;
bool heureSynchronisee = false;
bool rtcDisponible = false;
bool mesuresValides = false;
bool etatLED = false;

float temperature = 0.0;
float humidite = 0.0;

unsigned long dernierLED = 0;
unsigned long derniereMesure = 0;
unsigned long dernierAffichage = 0;
unsigned long derniereTentativeWiFi = 0;
unsigned long derniereTentativeNTP = 0;
unsigned long debutAccueil = 0;

// ====================================
// 3. Verification WiFi
// ====================================

bool wifiOK() {

  if (WiFi.status() != WL_CONNECTED) {
    return false;
  }

  IPAddress ip = WiFi.localIP();

  return ip[0] != 0 ||
         ip[1] != 0 ||
         ip[2] != 0 ||
         ip[3] != 0;
}

// ====================================
// 4. Connexion WiFi
// ====================================

void setup_wifi() {

  Serial.println("Connexion WiFi...");
  Serial.print("SSID : ");
  Serial.println(WIFI_SSID);

  // Connexion au reseau du TP
  WiFi.begin(WIFI_SSID, WIFI_PASS);

  derniereTentativeWiFi = millis();
}

// ====================================
// 5. Gestion WiFi
// ====================================

void gererWiFi() {

  bool connexionOK = wifiOK();

  // Nouvelle connexion reussie
  if (connexionOK && !wifiConnecte) {

    wifiConnecte = true;

    Serial.println("WiFi connecte !");
    Serial.print("Adresse IP : ");
    Serial.println(WiFi.localIP());

    // Initialiser NTP apres connexion WiFi
    ntp.begin();
    ntpDemarre = true;

    // Autoriser une synchronisation immediate
    derniereTentativeNTP = millis() - 15000UL;
  }

  // Perte de connexion
  if (!connexionOK && wifiConnecte) {

    wifiConnecte = false;

    Serial.println("WiFi deconnecte");

    if (ntpDemarre) {
      ntp.end();
      ntpDemarre = false;
    }
  }

  // Reconnexion toutes les 20 secondes
  if (!connexionOK &&
      millis() - derniereTentativeWiFi >= 20000UL) {

    setup_wifi();
  }
}

// ====================================
// 6. Heure d'ete / heure d'hiver
// ====================================

// 0 = dimanche
int jourSemaine(int an, int mois, int jour) {

  const int t[] = {
    0, 3, 2, 5, 0, 3,
    5, 1, 4, 6, 2, 4
  };

  if (mois < 3) {
    an--;
  }

  return (
    an + an / 4 - an / 100 +
    an / 400 + t[mois - 1] + jour
  ) % 7;
}

// Decalage UTC pour la France
int decalageFrance(const RTCTime &utc) {

  int an = utc.getYear();
  int mois = Month2int(utc.getMonth());
  int jour = utc.getDayOfMonth();
  int heure = utc.getHour();

  // Hiver : UTC+1
  if (mois < 3 || mois > 10) return 1;

  // Ete : UTC+2
  if (mois > 3 && mois < 10) return 2;

  // Dernier dimanche du mois
  int dernierDimanche =
    31 - jourSemaine(an, mois, 31);

  // Passage a l'heure d'ete
  if (mois == 3) {

    if (jour > dernierDimanche) return 2;
    if (jour < dernierDimanche) return 1;

    return heure >= 1 ? 2 : 1;
  }

  // Passage a l'heure d'hiver
  if (jour < dernierDimanche) return 2;
  if (jour > dernierDimanche) return 1;

  return heure < 1 ? 2 : 1;
}

// ====================================
// 7. Lecture de l'heure RTC
// ====================================

bool lireHeureLocale(RTCTime &locale) {

  if (!heureSynchronisee || !rtcDisponible) {
    return false;
  }

  RTCTime utc;

  if (!RTC.getTime(utc)) {
    return false;
  }

  // Convertir UTC en heure francaise
  time_t timestamp =
    utc.getUnixTime() +
    decalageFrance(utc) * 3600L;

  locale = RTCTime(timestamp);

  return true;
}

// ====================================
// 8. Synchronisation NTP
// ====================================

void synchroniserNTP() {

  if (!wifiConnecte ||
      !ntpDemarre ||
      !rtcDisponible) {
    return;
  }

  unsigned long maintenant = millis();

  // En cas d'echec : reessayer apres 15 s
  // Apres succes : synchroniser toutes les 15 min
  unsigned long intervalle =
    heureSynchronisee ? 900000UL : 15000UL;

  if (maintenant - derniereTentativeNTP
      < intervalle) {
    return;
  }

  derniereTentativeNTP = maintenant;

  Serial.println("======================");
  Serial.println("Synchronisation NTP...");
  Serial.println("Serveur : 192.168.1.254");

  // Envoyer une requete NTP
  if (ntp.forceUpdate()) {

    unsigned long epoch = ntp.getEpochTime();

    // Verifier la validite du timestamp
    if (epoch < 1700000000UL) {

      Serial.println("Date NTP invalide");
      return;
    }

    // Stocker l'heure UTC dans le RTC
    RTCTime heureUTC((time_t)epoch);

    if (RTC.setTime(heureUTC)) {

      if (!heureSynchronisee) {
        debutAccueil = millis();
      }

      heureSynchronisee = true;

      Serial.println("NTP OK !");
      Serial.println("RTC mis a jour");

      RTCTime heureLocale;

      if (lireHeureLocale(heureLocale)) {
        Serial.print("Date et heure : ");
        Serial.println(heureLocale.toString());
      }

    } else {

      Serial.println("Erreur RTC");
    }

  } else {

    Serial.println("NTP indisponible");
    Serial.println("Nouvel essai dans 15 s");
  }
}

// ====================================
// 9. Acquisition DHT22
// ====================================

void lireDHT22() {

  float t = dht.readTemperature();
  float h = dht.readHumidity();

  if (isnan(t) || isnan(h)) {

    Serial.println("Erreur DHT22");
    return;
  }

  temperature = t;
  humidite = h;
  mesuresValides = true;

  Serial.print("Temperature : ");
  Serial.print(temperature, 1);
  Serial.print(" C | Humidite : ");
  Serial.print(humidite, 1);
  Serial.println(" %");
}

// ====================================
// 10. Affichage LCD
// ====================================

void afficherLigne(byte ligne, const char *texte) {

  lcd.setCursor(0, ligne);
  lcd.print("                ");

  lcd.setCursor(0, ligne);
  lcd.print(texte);
}

void afficherMesures() {

  lcd.setCursor(0, 1);
  lcd.print("                ");
  lcd.setCursor(0, 1);

  if (!mesuresValides) {

    lcd.print("Attente DHT22");
    return;
  }

  lcd.print("T:");
  lcd.print(temperature, 1);
  lcd.print("C H:");
  lcd.print(humidite, 1);
  lcd.print("%");
}

// ====================================
// 11. Affichage principal
// ====================================

void afficherLCD() {

  // Avant la synchronisation
  if (!heureSynchronisee) {

    if (!wifiConnecte) {
      afficherLigne(0, "WiFi en attente");
    } else {
      afficherLigne(0, "NTP en attente");
    }

    afficherMesures();
    return;
  }

  RTCTime heureLocale;

  if (!lireHeureLocale(heureLocale)) {

    afficherLigne(0, "Erreur RTC");
    afficherMesures();
    return;
  }

  char ligne[17];

  // ==================================
  // Ecran du professeur : 6 secondes
  // ==================================

  if (millis() - debutAccueil < 6000UL) {

    // Ligne 1 : version + date
    snprintf(
      ligne,
      sizeof(ligne),
      "V1.0 %02d/%02d/%04d",
      heureLocale.getDayOfMonth(),
      Month2int(heureLocale.getMonth()),
      heureLocale.getYear()
    );

    afficherLigne(0, ligne);

    // Ligne 2 : adresse IP
    lcd.setCursor(0, 1);
    lcd.print("                ");
    lcd.setCursor(0, 1);
    lcd.print(WiFi.localIP());

  } else {

    // ==================================
    // Affichage normal
    // ==================================

    // Ligne 1 : date et heure
    snprintf(
      ligne,
      sizeof(ligne),
      "%02d/%02d %02d:%02d:%02d",
      heureLocale.getDayOfMonth(),
      Month2int(heureLocale.getMonth()),
      heureLocale.getHour(),
      heureLocale.getMinutes(),
      heureLocale.getSeconds()
    );

    afficherLigne(0, ligne);

    // Ligne 2 : temperature et humidite
    afficherMesures();
  }
}

// ====================================
// 12. Setup
// ====================================

void setup() {

  Serial.begin(9600);

  // LED de vie : active LOW
  pinMode(LED_VIE, OUTPUT);
  digitalWrite(LED_VIE, HIGH);

  // Capteur DHT22
  dht.begin();

  // LCD
  Wire.begin();
  lcd.begin(16, 2);
  lcd.clear();

  afficherLigne(0, "Demarrage...");

  // Initialisation du RTC
  rtcDisponible = RTC.begin();

  if (!rtcDisponible) {
    Serial.println("Erreur initialisation RTC");
  }

  // Demarrer WiFi
  // NTP sera initialise apres la connexion
  setup_wifi();

  // Autoriser une premiere mesure immediate
  derniereMesure = millis() - 2000UL;

  Serial.println("TempHumiX V1.0 demarre");
}

// ====================================
// 13. Loop
// ====================================

void loop() {

  unsigned long maintenant = millis();

  // LED de vie : 2 Hz
  // 250 ms allumee + 250 ms eteinte
  if (maintenant - dernierLED >= 250UL) {

    dernierLED = maintenant;

    etatLED = !etatLED;

    digitalWrite(
      LED_VIE,
      etatLED ? LOW : HIGH
    );
  }

  // DHT22 : mesure toutes les 2 secondes
  if (maintenant - derniereMesure >= 2000UL) {

    derniereMesure = maintenant;
    lireDHT22();
  }

  // Gestion de la connexion WiFi
  gererWiFi();

  // Synchronisation NTP
  synchroniserNTP();

  // LCD : mise a jour chaque seconde
  if (maintenant - dernierAffichage >= 1000UL) {

    dernierAffichage = maintenant;
    afficherLCD();
  }

  delay(10);
}
