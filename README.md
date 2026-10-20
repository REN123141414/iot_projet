# Projet IoT - Capteur de temperature et d'humidite

## Presentation

Ce projet est realise dans le cadre du TP IoT de l'IMT Nord Europe.

L'objectif est de concevoir et programmer un systeme de mesure de temperature et d'humidite avec un microcontroleur Arduino.

## Objectifs

- Simuler des circuits electroniques avec SimulIDE.
- Programmer un Arduino UNO R3.
- Utiliser un capteur de temperature et d'humidite DHT22.
- Afficher les mesures sur un ecran LCD I2C.
- Transmettre des donnees via une liaison serie.
- Etudier la communication IoT avec le protocole MQTT.

## Organisation du projet

- simulide/clignotement_led/ : premier circuit avec une LED.
- README.md : documentation du projet.
- .gitignore : fichiers exclus du suivi Git.

## Premier exercice : clignotement LED

Le premier circuit contient :
- Un Arduino UNO R3
- Une LED
- Une resistance de 100 ohms

La LED est connectee a la broche D2 de l'Arduino.

Le programme allume la LED pendant 500 ms, puis l'eteint pendant 500 ms.

La frequence de clignotement est de 1 Hz.

## Outils utilises

- SimulIDE 1.1.0-SR2
- Arduino CLI
- Git et GitHub
- macOS Apple Silicon

## Utilisation

Pour compiler le premier programme :

cd simulide/clignotement_led

arduino-cli compile --fqbn arduino:avr:uno --output-dir build clignotement_led.ino

Le fichier HEX genere peut ensuite etre charge dans SimulIDE pour lancer la simulation.
