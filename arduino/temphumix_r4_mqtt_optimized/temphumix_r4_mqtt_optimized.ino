#include "arduino_secrets.h"

/*
  IMT Nord Europe - Projet IoT
  TP 6.1.6 - Optimisation MQTT
  Arduino UNO R4 WiFi - TempHumiX

  Identifiant : 44666

  Publication :
  VERSION     -> apres commande 10 + NTP OK
  TEMPERATURE -> si temperature ou humidite change
  HUMIDITY    -> si temperature ou humidite change
  GET_DATE    -> si temperature ou humidite change

  Souscription :
  COMMAND, BARGRAPH, BLINK

  DHT22 : A0
  LED_VIE : D2 (active LOW)
  Bargraph : D3 a D12
  LCD : Grove 16x2 I2C
*/

#include <WiFiS3.h>
#include <WiFiUdp.h>
#include <ArduinoMqttClient.h>
#include <NTPClient.h>
#include <Wire.h>
#include <rgb_lcd.h>
#include <DHT.h>
#include "RTC.h"
#include <math.h>

// ======================================
// 1. Parametres WiFi et MQTT
// ======================================


IPAddress MQTT_BROKER(192, 168, 1, 1);
const int MQTT_PORT = 1883;

const char MQTT_ID[] = "IdO_Client_44666";


// Topics de publication
const char TOPIC_VERSION[] = "/iot/VERSION_44666";
const char TOPIC_TEMP[] = "/iot/TEMPERATURE_44666";
const char TOPIC_HUM[] = "/iot/HUMIDITY_44666";
const char TOPIC_DATE[] = "/iot/GET_DATE_44666";

// Trois topics de souscription
const char TOPIC_COMMAND[] = "/iot/COMMAND_44666";
const char TOPIC_BARGRAPH[] = "/iot/BARGRAPH_44666";
const char TOPIC_BLINK[] = "/iot/BLINK_44666";

// ======================================
// 2. Materiel
// ======================================

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

// ======================================
// 3. Variables globales
// ======================================

bool wifiConnecte = false;
bool ntpDemarre = false;
bool rtcOK = false;
bool heureSynchronisee = false;

bool mesuresActives = true;
bool mesuresValides = false;
bool ledAllumee = false;

bool forcerNTP = false;

// Nouvelle logique de publication
bool publierVersionApresNTP = false;
bool publicationMesuresEnAttente = false;
bool premierePublication = true;

float temperature = 0;
float humidite = 0;

float derniereTemperaturePubliee = 0;
float derniereHumiditePubliee = 0;

unsigned long periodeLED = 500;
unsigned long periodePersonnalisee = 500;

unsigned long dernierLED = 0;
unsigned long derniereMesure = 0;
unsigned long dernierLCD = 0;
unsigned long dernierWiFi = 0;
unsigned long dernierMQTT = 0;
unsigned long dernierNTP = 0;
unsigned long debutAccueil = 0;

// ======================================
// 4. WiFi
// ======================================

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

  if (!ok &&
      millis() - dernierWiFi >= 20000UL) {
    setup_wifi();
  }
}

// ======================================
// 5. Heure francaise
// ======================================

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

  if (!RTC.getTime(utc)) {
    return false;
  }

  time_t timestamp =
    utc.getUnixTime() +
    decalageFrance(utc) * 3600L;

  locale = RTCTime(timestamp);

  return true;
}

// ======================================
// 6. Synchronisation NTP
// ======================================

void synchroniserNTP() {

  if (!wifiConnecte ||
      !ntpDemarre ||
      !rtcOK) {
    return;
  }

  unsigned long intervalle =
    heureSynchronisee ? 900000UL : 15000UL;

  if (!forcerNTP &&
      millis() - dernierNTP < intervalle) {
    return;
  }

  // Memoriser si la synchro vient de COMMAND 10
  bool commande10 = forcerNTP;
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

      // TP 6.1.6 :
      // VERSION uniquement apres COMMAND 10
      if (commande10) {

        publierVersionApresNTP = true;

        Serial.println(
          "VERSION autorisee apres commande 10"
        );
      }

    } else {
      Serial.println("Erreur RTC");
    }

  } else {
    Serial.println("NTP indisponible");
  }
}

// ======================================
// 7. Mesures DHT22
// ======================================

void lireDHT22() {

  float t = dht.readTemperature();
  float h = dht.readHumidity();

  if (isnan(t) || isnan(h)) {
    Serial.println("Erreur DHT22");
    return;
  }

  // Arrondir a un chiffre decimal
  temperature = roundf(t * 10.0f) / 10.0f;
  humidite = roundf(h * 10.0f) / 10.0f;

  mesuresValides = true;

  Serial.print("Temperature : ");
  Serial.print(temperature, 1);
  Serial.print(" C | Humidite : ");
  Serial.print(humidite, 1);
  Serial.println(" %");

  // ==================================
  // TP 6.1.6 : Detection des changements
  // ==================================

  if (premierePublication ||
      temperature != derniereTemperaturePubliee ||
      humidite != derniereHumiditePubliee) {

    publicationMesuresEnAttente = true;

    Serial.println(
      "Changement detecte : publication demandee"
    );

  } else {

    publicationMesuresEnAttente = false;

    Serial.println(
      "Valeurs identiques : pas de publication"
    );
  }
}

// ======================================
// 8. Affichage LCD
// ======================================

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

// ======================================
// 9. Controle Bargraph
// ======================================

void afficherBargraph(int valeur) {

  for (int i = 0; i < BAR_COUNT; i++) {

    bool actif =
      (valeur & (1 << i)) != 0;

    digitalWrite(
      BAR_START + i,
      actif ? HIGH : LOW
    );
  }
}

// ======================================
// 10. Reception MQTT
// ======================================

// Callback demandee par le professeur
void onMqttMessage(int tailleMessage) {

  String topic = mqttClient.messageTopic();
  String message = "";

  // Acquisition du message
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

  if (tailleMessage <= 0 ||
      tailleMessage > 20 ||
      message.length() == 0) {

    Serial.println("Message invalide");
    return;
  }

  // Conversion du message en entier
  for (unsigned int i = 0; i < message.length(); i++) {

    if (message[i] < '0' || message[i] > '9') {
      Serial.println("Entier attendu");
      return;
    }
  }

  long valeur = message.toInt();

  // ==================================
  // COMMAND
  // ==================================

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
        publicationMesuresEnAttente = false;
        Serial.println("Commande 30 : STOP");
        break;

      case 40:
        // LED lente
        periodeLED = 1000UL;
        Serial.println("Commande 40 : LENT");
        break;

      case 50:
        // LED rapide
        periodeLED = 200UL;
        Serial.println("Commande 50 : RAPIDE");
        break;

      case 60:
        // LED personnalisee
        periodeLED = periodePersonnalisee;
        Serial.println("Commande 60 : PERSONNALISE");
        break;

      default:
        Serial.println("Commande inconnue");
        break;
    }
  }

  // ==================================
  // BARGRAPH
  // ==================================

  else if (topic == TOPIC_BARGRAPH) {

    if (valeur >= 0 && valeur <= 1023) {

      afficherBargraph((int)valeur);

      Serial.print("BARGRAPH = ");
      Serial.println(valeur);

    } else {
      Serial.println("BARGRAPH hors limites");
    }
  }

  // ==================================
  // BLINK
  // ==================================

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

// ======================================
// 11. Connexion MQTT
// ======================================

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

  // Les 3 souscriptions du TP 6.1.5
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

    mqttClient.poll();

  } else if (millis() - dernierMQTT >= 10000UL) {

    dernierMQTT = millis();
    setup_mqtt();
  }
}

// ======================================
// 12. Publication MQTT
// ======================================

bool publierChaine(
  const char *topic,
  const char *message
) {

  if (!mqttClient.connected()) return false;

  if (!mqttClient.beginMessage(topic)) return false;

  mqttClient.print(message);

  if (!mqttClient.endMessage()) return false;

  Serial.print("PUB ");
  Serial.print(topic);
  Serial.print(" = ");
  Serial.println(message);

  return true;
}

// Publier la version apres COMMAND 10
void publierVersion() {

  if (!publierVersionApresNTP) return;
  if (!mqttClient.connected()) return;

  if (publierChaine(TOPIC_VERSION, "1.0")) {

    publierVersionApresNTP = false;

    Serial.println(
      "Version publiee apres NTP"
    );
  }
}

// Publier temperature, humidite et date
// uniquement si changement detecte

void publierMesures() {

  if (!mesuresActives ||
      !mesuresValides ||
      !publicationMesuresEnAttente ||
      !mqttClient.connected()) {
    return;
  }

  RTCTime locale;

  // Attendre une date valide
  if (!lireHeureLocale(locale)) {
    return;
  }

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

  char valeurTemp[16];
  char valeurHum[16];

  dtostrf(temperature, 0, 1, valeurTemp);
  dtostrf(humidite, 0, 1, valeurHum);

  bool okTemp =
    publierChaine(TOPIC_TEMP, valeurTemp);

  bool okHum =
    publierChaine(TOPIC_HUM, valeurHum);

  bool okDate =
    publierChaine(TOPIC_DATE, dateHeure);

  if (okTemp && okHum && okDate) {

    derniereTemperaturePubliee = temperature;
    derniereHumiditePubliee = humidite;

    premierePublication = false;

    publicationMesuresEnAttente = false;

    Serial.println(
      "Publication sur changement : OK"
    );
  }
}

// ======================================
// 13. SETUP
// ======================================

void setup() {

  Serial.begin(9600);

  // LED_VIE
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

  // Configuration MQTT
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

  Serial.println("TempHumiX TP 6.1.6 demarre");
}

// ======================================
// 14. LOOP
// ======================================

void loop() {

  unsigned long maintenant = millis();

  // LED : periode configurable
  if (maintenant - dernierLED >= periodeLED / 2UL) {

    dernierLED = maintenant;
    ledAllumee = !ledAllumee;

    digitalWrite(
      LED_VIE,
      ledAllumee ? LOW : HIGH
    );
  }

  // Acquisition toutes les 2 secondes
  if (mesuresActives &&
      maintenant - derniereMesure >= 2000UL) {

    derniereMesure = maintenant;

    lireDHT22();
  }

  // Connexions
  gererWiFi();
  gererMQTT();

  // Synchronisation NTP
  synchroniserNTP();

  // TP 6.1.6 :
  // Publication sur evenement uniquement
  publierVersion();
  publierMesures();

  // LCD toutes les secondes
  if (millis() - dernierLCD >= 1000UL) {

    dernierLCD = millis();

    afficherLCD();
  }

  delay(10);
}
