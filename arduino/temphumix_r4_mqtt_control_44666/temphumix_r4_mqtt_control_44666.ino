#include "arduino_secrets.h"

/*
  IMT Nord Europe - Projet IoT
  TP 6.1.5 - Publication et souscription MQTT
  Arduino UNO R4 WiFi - TempHumiX

  Identifiant : 44666

  DHT22    : A0
  LED_VIE  : D2 (active LOW)
  Bargraph : D3 a D12
  LCD      : Grove I2C 16x2

  NTP  : 192.168.1.254
  MQTT : 192.168.1.1:1883
*/

#include <WiFiS3.h>
#include <WiFiUdp.h>
#include <ArduinoMqttClient.h>
#include <NTPClient.h>
#include <Wire.h>
#include <rgb_lcd.h>
#include <DHT.h>
#include "RTC.h"

// =====================================
// 1. Parametres WiFi et MQTT
// =====================================




IPAddress MQTT_BROKER(192, 168, 1, 1);
const int MQTT_PORT = 1883;

const char MQTT_ID[] = "IdO_Client_44666";



// Topics publies
const char TOPIC_VERSION[] = "/iot/VERSION_44666";
const char TOPIC_TEMP[] = "/iot/TEMPERATURE_44666";
const char TOPIC_HUM[] = "/iot/HUMIDITY_44666";
const char TOPIC_DATE[] = "/iot/GET_DATE_44666";

// Topics souscrits (TP 6.1.5)
const char TOPIC_COMMAND[] = "/iot/COMMAND_44666";
const char TOPIC_BARGRAPH[] = "/iot/BARGRAPH_44666";
const char TOPIC_BLINK[] = "/iot/BLINK_44666";

// =====================================
// 2. Materiel
// =====================================

#define DHTPIN A0
#define DHTTYPE DHT22
#define LED_VIE 2

const int BAR_START = 3;
const int BAR_COUNT = 10;

DHT dht(DHTPIN, DHTTYPE);
rgb_lcd lcd;

WiFiUDP ntpUDP;

NTPClient ntp(
  ntpUDP,
  IPAddress(192, 168, 1, 254),
  0,
  60000
);

WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);

// =====================================
// 3. Variables globales
// =====================================

bool wifiConnecte = false;
bool ntpDemarre = false;
bool rtcOK = false;
bool heureSynchronisee = false;

bool mesuresActives = true;
bool mesuresValides = false;
bool ledAllumee = false;
bool forcerNTP = false;

float temperature = 0;
float humidite = 0;

// Periode totale de clignotement
unsigned long periodeLED = 500;
unsigned long periodePersonnalisee = 500;

unsigned long dernierLED = 0;
unsigned long derniereMesure = 0;
unsigned long dernierLCD = 0;
unsigned long dernierePublication = 0;

unsigned long dernierWiFi = 0;
unsigned long dernierMQTT = 0;
unsigned long dernierNTP = 0;
unsigned long debutAccueil = 0;

// =====================================
// 4. WiFi
// =====================================

bool wifiOK() {
  if (WiFi.status() != WL_CONNECTED) {
    return false;
  }

  IPAddress ip = WiFi.localIP();

  return ip != IPAddress(0, 0, 0, 0);
}

void setup_wifi() {
  Serial.println("Connexion WiFi...");
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  dernierWiFi = millis();
}

void gererWiFi() {
  bool ok = wifiOK();

  if (ok && !wifiConnecte) {
    wifiConnecte = true;

    Serial.println("WiFi OK !");
    Serial.print("IP : ");
    Serial.println(WiFi.localIP());

    ntp.begin();
    ntpDemarre = true;

    dernierNTP = millis() - 15000UL;
    dernierMQTT = millis() - 10000UL;
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

  if (!ok && millis() - dernierWiFi >= 20000UL) {
    setup_wifi();
  }
}

// =====================================
// 5. Heure francaise
// =====================================

// 0 = dimanche
int jourSemaine(int an, int mois, int jour) {
  const int t[] = {
    0, 3, 2, 5, 0, 3,
    5, 1, 4, 6, 2, 4
  };

  if (mois < 3) an--;

  return (
    an + an / 4 - an / 100 +
    an / 400 + t[mois - 1] + jour
  ) % 7;
}

int decalageFrance(const RTCTime &utc) {
  int an = utc.getYear();
  int mois = Month2int(utc.getMonth());
  int jour = utc.getDayOfMonth();
  int heure = utc.getHour();

  if (mois < 3 || mois > 10) return 1;
  if (mois > 3 && mois < 10) return 2;

  int dernierDimanche =
    31 - jourSemaine(an, mois, 31);

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

bool lireHeureLocale(RTCTime &locale) {
  if (!heureSynchronisee || !rtcOK) {
    return false;
  }

  RTCTime utc;
  if (!RTC.getTime(utc)) return false;

  time_t timestamp =
    utc.getUnixTime() +
    decalageFrance(utc) * 3600L;

  locale = RTCTime(timestamp);
  return true;
}

// =====================================
// 6. Synchronisation NTP
// =====================================

void synchroniserNTP() {
  if (!wifiConnecte || !ntpDemarre || !rtcOK) {
    return;
  }

  unsigned long intervalle =
    heureSynchronisee ? 900000UL : 15000UL;

  if (!forcerNTP &&
      millis() - dernierNTP < intervalle) {
    return;
  }

  forcerNTP = false;
  dernierNTP = millis();

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

// =====================================
// 7. DHT22
// =====================================

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

// =====================================
// 8. LCD
// =====================================

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

  if (!mesuresActives) {
    lcd.print("Mesure arretee");
    return;
  }

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

  // Ecran d'accueil, comme le professeur
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

// =====================================
// 9. Controle du Bargraph
// =====================================

// 10 bits, valeur entre 0 et 1023
// D3 = bit 0 ; D12 = bit 9

void afficherBargraph(int valeur) {
  for (int i = 0; i < BAR_COUNT; i++) {
    bool actif = (valeur & (1 << i)) != 0;

    digitalWrite(
      BAR_START + i,
      actif ? HIGH : LOW
    );
  }
}

// =====================================
// 10. CALLBACK MQTT : TP 6.1.5
// =====================================

// Fonction appelee a la reception MQTT
void onMqttMessage(int tailleMessage) {

  // A. Acquisition du topic
  String topic = mqttClient.messageTopic();

  // B. Acquisition du message
  String message = "";

  while (mqttClient.available()) {
    char c = (char)mqttClient.read();

    if (message.length() < 20) {
      message += c;
    }
  }

  message.trim();

  Serial.print("MQTT RX ");
  Serial.print(topic);
  Serial.print(" = ");
  Serial.println(message);

  // Verifier le message
  if (tailleMessage <= 0 ||
      tailleMessage > 20 ||
      message.length() == 0) {
    Serial.println("Message invalide");
    return;
  }

  // C. Conversion en entier
  for (unsigned int i = 0; i < message.length(); i++) {
    if (message[i] < '0' || message[i] > '9') {
      Serial.println("Entier attendu");
      return;
    }
  }

  long valeur = message.toInt();

  // D. Topic COMMAND
  if (topic == TOPIC_COMMAND) {
    switch (valeur) {

      case 10:
        // Forcer NTP
        forcerNTP = true;
        Serial.println("Commande 10 : NTP");
        break;

      case 20:
        // Demarrer les mesures
        mesuresActives = true;
        derniereMesure = millis() - 2000UL;
        Serial.println("Commande 20 : START");
        break;

      case 30:
        // Arreter les mesures
        mesuresActives = false;
        Serial.println("Commande 30 : STOP");
        break;

      case 40:
        // Clignotement lent
        periodeLED = 1000UL;
        Serial.println("Commande 40 : LENT");
        break;

      case 50:
        // Clignotement rapide
        periodeLED = 200UL;
        Serial.println("Commande 50 : RAPIDE");
        break;

      case 60:
        // Clignotement personnalise
        periodeLED = periodePersonnalisee;
        Serial.println("Commande 60 : PERSONNALISE");
        break;

      default:
        Serial.println("Commande inconnue");
        break;
    }
  }

  // E. Topic BARGRAPH
  else if (topic == TOPIC_BARGRAPH) {
    if (valeur >= 0 && valeur <= 1023) {
      afficherBargraph((int)valeur);
      Serial.print("BARGRAPH = ");
      Serial.println(valeur);
    } else {
      Serial.println("BARGRAPH hors limites");
    }
  }

  // F. Topic BLINK
  else if (topic == TOPIC_BLINK) {
    if (valeur >= 100 &&
        valeur <= 60000 &&
        valeur % 100 == 0) {

      periodePersonnalisee =
        (unsigned long)valeur;

      Serial.print("BLINK sauvegarde = ");
      Serial.println(periodePersonnalisee);

    } else {
      Serial.println("BLINK invalide (100 ms)");
    }
  }
}

// =====================================
// 11. Initialisation MQTT
// =====================================

// Retourne 0 si OK, erreur sinon
int setup_mqtt() {
  if (!wifiOK()) return -10;

  if (mqttClient.connected()) return 0;

  Serial.println("Connexion MQTT...");

  if (!mqttClient.connect(MQTT_BROKER, MQTT_PORT)) {
    int erreur = mqttClient.connectError();

    Serial.print("Erreur MQTT : ");
    Serial.println(erreur);
    return erreur;
  }

  Serial.println("MQTT connecte !");

  // Souscription aux trois topics du TP
  bool s1 = mqttClient.subscribe(TOPIC_COMMAND, 0);
  bool s2 = mqttClient.subscribe(TOPIC_BARGRAPH, 0);
  bool s3 = mqttClient.subscribe(TOPIC_BLINK, 0);

  if (!s1 || !s2 || !s3) {
    Serial.println("Erreur souscription MQTT");
    mqttClient.stop();
    return -11;
  }

  Serial.println("SUB COMMAND OK");
  Serial.println("SUB BARGRAPH OK");
  Serial.println("SUB BLINK OK");

  return 0;
}

void gererMQTT() {
  if (!wifiConnecte) return;

  if (mqttClient.connected()) {
    // Necessaire pour recevoir les messages
    mqttClient.poll();
  } else if (millis() - dernierMQTT >= 10000UL) {
    dernierMQTT = millis();
    setup_mqtt();
  }
}

// =====================================
// 12. Publication MQTT
// =====================================

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

void publierMQTT() {
  if (!mqttClient.connected()) return;

  // VERSION
  publierChaine(TOPIC_VERSION, "1.0");

  // TEMPERATURE + HUMIDITY
  if (mesuresActives && mesuresValides) {

    mqttClient.beginMessage(TOPIC_TEMP);
    mqttClient.print(temperature, 1);
    mqttClient.endMessage();

    mqttClient.beginMessage(TOPIC_HUM);
    mqttClient.print(humidite, 1);
    mqttClient.endMessage();

    Serial.println("PUB temperature / humidite");
  }

  // GET_DATE
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
  }
}

// =====================================
// 13. SETUP
// =====================================

void setup() {
  Serial.begin(9600);

  // LED de vie : active LOW
  pinMode(LED_VIE, OUTPUT);
  digitalWrite(LED_VIE, HIGH);

  // Bargraph
  for (int i = 0; i < BAR_COUNT; i++) {
    pinMode(BAR_START + i, OUTPUT);
    digitalWrite(BAR_START + i, LOW);
  }

  // DHT22
  dht.begin();

  // LCD
  Wire.begin();
  lcd.begin(16, 2);
  lcd.clear();
  afficherLigne(0, "Demarrage...");

  // RTC
  rtcOK = RTC.begin();

  if (!rtcOK) {
    Serial.println("Erreur RTC");
  }

  // Callback MQTT
  mqttClient.onMessage(onMqttMessage);

  mqttClient.setId(MQTT_ID);
  mqttClient.setUsernamePassword(
    MQTT_USER,
    MQTT_PASS
  );

  mqttClient.setKeepAliveInterval(60000);
  mqttClient.setConnectionTimeout(3000);

  // WiFi
  setup_wifi();

  derniereMesure = millis() - 2000UL;

  Serial.println("TempHumiX 6.1.5 demarre");
}

// =====================================
// 14. LOOP
// =====================================

void loop() {
  unsigned long maintenant = millis();

  // LED_VIE : periode configurable
  if (maintenant - dernierLED >= periodeLED / 2UL) {
    dernierLED = maintenant;

    ledAllumee = !ledAllumee;
    digitalWrite(
      LED_VIE,
      ledAllumee ? LOW : HIGH
    );
  }

  // DHT22 : toutes les 2 secondes
  if (mesuresActives &&
      maintenant - derniereMesure >= 2000UL) {
    derniereMesure = maintenant;
    lireDHT22();
  }

  // Communication
  gererWiFi();
  gererMQTT();
  synchroniserNTP();

  // MQTT : publier toutes les 2 secondes
  if (millis() - dernierePublication >= 2000UL) {
    dernierePublication = millis();
    publierMQTT();
  }

  // LCD : actualisation chaque seconde
  if (millis() - dernierLCD >= 1000UL) {
    dernierLCD = millis();
    afficherLCD();
  }

  delay(10);
}
