#include <Wire.h>
#include <rgb_lcd.h>
#include "RTC.h"

rgb_lcd lcd;

void setup() {
  Serial.begin(9600);

  // Initialisation du LCD
  Wire.begin();
  lcd.begin(16, 2);
  lcd.clear();

  // Initialisation du RTC
  if (!RTC.begin()) {
    lcd.print("Erreur RTC");
    while (true) {}
  }

  // Date et heure initiales (pour le test)
  RTCTime startTime(
    21, Month::OCTOBER, 2026,
    10, 30, 0,
    DayOfWeek::WEDNESDAY,
    SaveLight::SAVING_TIME_ACTIVE
  );

  RTC.setTime(startTime);
}

void loop() {
  RTCTime currentTime;

  // Lecture de la date et de l'heure
  if (RTC.getTime(currentTime)) {
    String dateTime = currentTime.toString();

    // Ligne 1 : date
    lcd.setCursor(0, 0);
    lcd.print(dateTime.substring(0, 10));

    // Ligne 2 : heure
    lcd.setCursor(0, 1);
    lcd.print(dateTime.substring(11, 19));

    Serial.println(dateTime);
  }

  delay(1000);
}