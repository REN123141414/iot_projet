#include "arduino_secrets.h"

/*
 * IMT Nord Europe - Projet IoT
 * TP 6.1.4 - Publication MQTT
 * Arduino UNO R4 WiFi - TempHumiX
 *
 * Identifiant du capteur : 44666
 * DHT22 : A0
 * LED_VIE : D2 (active LOW)
 * LCD : I2C Grove 16x2
 *
 * WiFi : IoT IMT Nord Europe
 * NTP : 192.168.1.254
 * MQTT : 192.168.1.1:1883
 */

#include <WiFiS3.h>
#include <WiFiUdp.h>
#include <ArduinoMqttClient.h>
#include <NTPClient.h>
#include <Wire.h>
#include <rgb_lcd.h>
#include <DHT.h>
#include "RTC.h"

// ====================================
// 1. Configuration WiFi
// ====================================




// ====================================
// 2. Configuration MQTT
// ====================================

IPAddress MQTT_BROKER(192, 168, 1, 1);
const int MQTT_PORT = 1883;

const char MQTT_CLIENT_ID[] = "IdO_Client_44666";



const char TOPIC_VERSION[] = "/iot/VERSION_44666";
const char TOPIC_TEMP[] = "/iot/TEMPERATURE_44666";
const char TOPIC_HUM[] = "/iot/HUMIDITY_44666";
const char TOPIC_DATE[] = "/iot/GET_DATE_44666";

// ====================================
// 3. Configuration capteur
// ====================================

#define DHTPIN A0
#define DHTTYPE DHT22
#define LED_VIE 2

DHT dht(DHTPIN, DHTTYPE);
rgb_lcd lcd;

// ====================================
// 4. Clients reseau
// ====================================

WiFiUDP ntpUDP;

NTPClient ntp(
  ntpUDP,
  IPAddress(192, 168, 1, 254),
  0,
  60000
);

WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);

// ====================================
// 5. Variables globales
// ====================================

bool wifiConnecte = false;
bool ntpDemarre = false;
bool rtcDisponible = false;
bool heureSynchronisee = false;
bool mesuresValides = false;
bool etatLED = false;

float temperature = 0.0;
float humidite = 0.0;

unsigned long dernierLED = 0;
unsigned long derniereMesure = 0;
unsigned long dernierLCD = 0;

unsigned long derniereTentativeWiFi = 0;
unsigned long derniereTentativeNTP = 0;
unsigned long derniereTentativeMQTT = 0;

unsigned long dernierePublication = 0;
unsigned long debutAccueil = 0;

// ====================================
// 6. Verification WiFi
// ====================================

bool wifiOK() {

  if (WiFi.status() != WL_CONNECTED) {
    return false;
  }

  IPAddress ip = WiFi.localIP();

  return ip != IPAddress(0, 0, 0, 0);
}

// ====================================
// 7. Initialisation WiFi
// ====================================

void setup_wifi() {

  Serial.println("Connexion WiFi...");

  WiFi.begin(WIFI_SSID, WIFI_PASS);

  derniereTentativeWiFi = millis();
}

// ====================================
// 8. Gestion WiFi
// ====================================

void gererWiFi() {

  bool ok = wifiOK();

  if (ok && !wifiConnecte) {

    wifiConnecte = true;

    Serial.println("WiFi connecte !");
    Serial.print("IP : ");
    Serial.println(WiFi.localIP());

    // Demarrer NTP apres WiFi
    ntp.begin();
    ntpDemarre = true;

    derniereTentativeNTP =
      millis() - 15000UL;

    derniereTentativeMQTT =
      millis() - 10000UL;
  }

  if (!ok && wifiConnecte) {

    wifiConnecte = false;

    Serial.println("WiFi deconnecte");

    if (ntpDemarre) {
      ntp.end();
      ntpDemarre = false;
    }

    mqttClient.stop();
  }

  // Reconnexion toutes les 20 secondes
  if (!ok &&
      millis() - derniereTentativeWiFi >= 20000UL) {

    setup_wifi();
  }
}

// ====================================
// 9. Heure ete / hiver France
// ====================================

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

int decalageFrance(const RTCTime &utc) {

  int mois = Month2int(utc.getMonth());
  int jour = utc.getDayOfMonth();
  int heure = utc.getHour();

  if (mois < 3 || mois > 10) return 1;
  if (mois > 3 && mois < 10) return 2;

  int dernierDimanche =
    31 - jourSemaine(utc.getYear(), mois, 31);

  if (mois == 3) {

    return (
      jour > dernierDimanche ||
      (jour == dernierDimanche && heure >= 1)
    ) ? 2 : 1;
  }

  return (
    jour < dernierDimanche ||
    (jour == dernierDimanche && heure < 1)
  ) ? 2 : 1;
}

// ====================================
// 10. Lecture RTC
// ====================================

bool lireHeureLocale(RTCTime &locale) {

  if (!heureSynchronisee || !rtcDisponible) {
    return false;
  }

  RTCTime utc;

  if (!RTC.getTime(utc)) {
    return false;
  }

  time_t timestamp =
    utc.getUnixTime() +
    decalageFrance(utc) * 3600L;

  locale = RTCTime(timestamp);

  return true;
}

// ====================================
// 11. Synchronisation NTP
// ====================================

void synchroniserNTP() {

  if (!wifiConnecte ||
      !ntpDemarre ||
      !rtcDisponible) {
    return;
  }

  unsigned long intervalle =
    heureSynchronisee ? 900000UL : 15000UL;

  if (millis() - derniereTentativeNTP < intervalle) {
    return;
  }

  derniereTentativeNTP = millis();

  Serial.println("Synchronisation NTP...");
  Serial.println("Serveur : 192.168.1.254");

  if (ntp.forceUpdate()) {

    unsigned long epoch = ntp.getEpochTime();

    if (epoch < 1700000000UL) {
      Serial.println("Date NTP invalide");
      return;
    }

    RTCTime heureUTC((time_t)epoch);

    if (RTC.setTime(heureUTC)) {

      if (!heureSynchronisee) {
        debutAccueil = millis();
      }

      heureSynchronisee = true;

      Serial.println("NTP OK !");
      Serial.println("RTC synchronisee");

    } else {

      Serial.println("Erreur RTC");
    }

  } else {

    Serial.println("NTP indisponible");
  }
}

// ====================================
// 12. Acquisition DHT22
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
// 13. Affichage LCD
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

void afficherLCD() {

  if (!wifiConnecte) {

    afficherLigne(0, "WiFi en attente");
    afficherMesures();
    return;
  }

  if (!heureSynchronisee) {

    afficherLigne(0, "NTP en attente");
    afficherMesures();
    return;
  }

  RTCTime locale;

  if (!lireHeureLocale(locale)) {

    afficherLigne(0, "Erreur RTC");
    afficherMesures();
    return;
  }

  char ligne[17];

  // Ecran d'accueil du professeur
  if (millis() - debutAccueil < 6000UL) {

    snprintf(
      ligne,
      sizeof(ligne),
      "V1.0 %02d/%02d/%04d",
      locale.getDayOfMonth(),
      Month2int(locale.getMonth()),
      locale.getYear()
    );

    afficherLigne(0, ligne);

    lcd.setCursor(0, 1);
    lcd.print("                ");
    lcd.setCursor(0, 1);
    lcd.print(WiFi.localIP());

  } else {

    // Date + heure
    snprintf(
      ligne,
      sizeof(ligne),
      "%02d/%02d %02d:%02d:%02d",
      locale.getDayOfMonth(),
      Month2int(locale.getMonth()),
      locale.getHour(),
      locale.getMinutes(),
      locale.getSeconds()
    );

    afficherLigne(0, ligne);
    afficherMesures();
  }
}

// ====================================
// 14. Initialisation MQTT
// ====================================

// 0 si connexion reussie
// Code erreur dans les autres cas

int setup_mqtt() {

  if (!wifiOK()) {
    return -10;
  }

  if (mqttClient.connected()) {
    return 0;
  }

  Serial.println("Connexion MQTT...");
  Serial.println("Broker : 192.168.1.1:1883");

  if (mqttClient.connect(MQTT_BROKER, MQTT_PORT)) {

    Serial.println("MQTT OK !");
    return 0;
  }

  int erreur = mqttClient.connectError();

  Serial.print("Erreur MQTT : ");
  Serial.println(erreur);

  return erreur;
}

// ====================================
// 15. Gestion MQTT
// ====================================

void gererMQTT() {

  if (!wifiConnecte) {
    return;
  }

  if (mqttClient.connected()) {

    // Maintenir la connexion MQTT
    mqttClient.poll();

  } else if (
    millis() - derniereTentativeMQTT >= 10000UL
  ) {

    derniereTentativeMQTT = millis();

    setup_mqtt();
  }
}

// ====================================
// 16. Publier une chaine MQTT
// ====================================

void publierChaine(
  const char *topic,
  const char *message
) {

  mqttClient.beginMessage(topic);

  mqttClient.print(message);

  mqttClient.endMessage();

  Serial.print("PUB ");
  Serial.print(topic);
  Serial.print(" = ");
  Serial.println(message);
}

// ====================================
// 17. Publication MQTT
// ====================================

void publierMQTT() {

  if (!mqttClient.connected()) {
    return;
  }

  // 1. Version
  publierChaine(TOPIC_VERSION, "1.0");

  // 2. Temperature et humidite
  if (mesuresValides) {

    mqttClient.beginMessage(TOPIC_TEMP);
    mqttClient.print(temperature, 1);
    mqttClient.endMessage();

    mqttClient.beginMessage(TOPIC_HUM);
    mqttClient.print(humidite, 1);
    mqttClient.endMessage();

    Serial.println("PUB temperature / humidite");
  }

  // 3. Date et heure
  RTCTime locale;

  if (lireHeureLocale(locale)) {

    char dateHeure[24];

    snprintf(
      dateHeure,
      sizeof(dateHeure),
      "%02d/%02d/%04d %02d:%02d:%02d",
      locale.getDayOfMonth(),
      Month2int(locale.getMonth()),
      locale.getYear(),
      locale.getHour(),
      locale.getMinutes(),
      locale.getSeconds()
    );

    publierChaine(TOPIC_DATE, dateHeure);

  } else {

    Serial.println("Date non disponible");
  }
}

// ====================================
// 18. Setup
// ====================================

void setup() {

  Serial.begin(9600);

  // LED de vie
  pinMode(LED_VIE, OUTPUT);
  digitalWrite(LED_VIE, HIGH);

  // DHT22
  dht.begin();

  // LCD
  Wire.begin();
  lcd.begin(16, 2);
  lcd.clear();

  afficherLigne(0, "Demarrage...");

  // RTC
  rtcDisponible = RTC.begin();

  if (!rtcDisponible) {
    Serial.println("Erreur RTC");
  }

  // Configuration client MQTT
  mqttClient.setId(MQTT_CLIENT_ID);

  mqttClient.setUsernamePassword(
    MQTT_USER,
    MQTT_PASS
  );

  mqttClient.setKeepAliveInterval(60000);
  mqttClient.setConnectionTimeout(3000);

  // WiFi
  setup_wifi();

  derniereMesure = millis() - 2000UL;

  Serial.println("TempHumiX 44666 demarre");
}

// ====================================
// 19. Loop
// ====================================

void loop() {

  unsigned long maintenant = millis();

  // LED 2 Hz
  if (maintenant - dernierLED >= 250UL) {

    dernierLED = maintenant;

    etatLED = !etatLED;

    digitalWrite(
      LED_VIE,
      etatLED ? LOW : HIGH
    );
  }

  // Mesures toutes les 2 secondes
  if (maintenant - derniereMesure >= 2000UL) {

    derniereMesure = maintenant;

    lireDHT22();
  }

  // Gestion reseau
  gererWiFi();

  // Synchronisation RTC
  synchroniserNTP();

  // Gestion connexion MQTT
  gererMQTT();

  // Publication toutes les 2 secondes
  if (millis() - dernierePublication >= 2000UL) {

    dernierePublication = millis();

    publierMQTT();
  }

  // Affichage toutes les secondes
  if (millis() - dernierLCD >= 1000UL) {

    dernierLCD = millis();

    afficherLCD();
  }

  delay(10);
}
