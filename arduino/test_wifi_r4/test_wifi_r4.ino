#include "arduino_secrets.h"

#include <WiFiS3.h>
#include <Wire.h>
#include <rgb_lcd.h>

// =====================================
// 1. Configuration WiFi
// =====================================



// Remplacer par le mot de passe WiFi du TP


// Ecran Grove LCD
rgb_lcd lcd;

// Etat de la connexion
bool wifiConnected = false;


// =====================================
// 2. Verification de l'adresse IP
// =====================================

bool ipValide(IPAddress ip) {
  return ip[0] != 0 ||
         ip[1] != 0 ||
         ip[2] != 0 ||
         ip[3] != 0;
}


// =====================================
// 3. Initialisation du WiFi
// =====================================

bool setup_wifi() {

  Serial.println("Connexion au WiFi...");
  Serial.print("SSID : ");
  Serial.println(ssid);

  // Demarrer la connexion
  WiFi.begin(ssid, password);

  unsigned long debut = millis();

  // Attendre maximum 30 secondes
  while (millis() - debut < 30000) {

    int status = WiFi.status();
    IPAddress ip = WiFi.localIP();

    // WiFi connecte ET adresse IP valide
    if (status == WL_CONNECTED && ipValide(ip)) {

      Serial.println("WiFi connecte !");
      Serial.print("Adresse IP : ");
      Serial.println(ip);

      return true;
    }

    delay(500);
  }

  Serial.println("WiFi : connexion ou DHCP echoue");
  return false;
}


// =====================================
// 4. Affichage sur le LCD
// =====================================

void afficherLCD() {

  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("V1.0");

  lcd.setCursor(0, 1);

  IPAddress ip = WiFi.localIP();

  if (WiFi.status() == WL_CONNECTED && ipValide(ip)) {

    lcd.print(ip);

  } else {

    lcd.print("IP en attente");
  }
}


// =====================================
// 5. Fonction setup()
// =====================================

void setup() {

  Serial.begin(9600);

  // Initialiser LCD
  Wire.begin();
  lcd.begin(16, 2);
  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("Connexion WiFi");

  // Initialiser WiFi
  wifiConnected = setup_wifi();

  afficherLCD();
}


// =====================================
// 6. Fonction loop()
// =====================================

void loop() {

  // Verifier l'etat de la connexion
  int status = WiFi.status();
  IPAddress ip = WiFi.localIP();

  wifiConnected =
    (status == WL_CONNECTED && ipValide(ip));

  // Afficher les informations dans Serial Monitor
  Serial.print("WiFi Status : ");
  Serial.println(status);

  Serial.print("Adresse IP : ");
  Serial.println(ip);

  // Actualiser le LCD
  afficherLCD();

  // Reessayer la connexion si necessaire
  if (!wifiConnected) {

    Serial.println("Nouvelle tentative WiFi...");

    wifiConnected = setup_wifi();
    afficherLCD();
  }

  delay(1000);
}
