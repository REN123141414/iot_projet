# TempHumiX — Projet IoT

**Ruilang REN — IMT Nord Europe**

Ce projet réalise un système de mesure de température et d’humidité, depuis la simulation jusqu’à la supervision d’un Arduino par MQTT.

## Organisation

| Dossier | Contenu |
|---|---|
| `simulide/` | Circuits et programmes de simulation avec Arduino UNO R3 |
| `arduino/` | Programmes pour Arduino UNO R4 WiFi |
| `IHM/` | Applications Python : MQTT, interface graphique, SQLite et courbes |
| `docs/` | Rapport du projet |

[Consulter le rapport PDF](docs/Rapport_Iot_REN%20Ruilang.pdf)

## Matériel et fonctionnalités

Le dispositif utilise un capteur DHT22, un écran LCD I2C et des LED.

- Acquisition et affichage de la température et de l’humidité.
- Publication des mesures via MQTT.
- Synchronisation de l’horloge par NTP.
- Commande à distance des mesures, du clignotement et du bargraphe.
- Archivage SQLite et consultation des courbes historiques.

## Progression de l’IHM

Les programmes intermédiaires sont conservés dans `IHM/` :

1. `console_mqtt_lecture/` : réception MQTT.
2. `console_mqtt_ecriture/` : envoi de commandes.
3. `mqtt_thread/` : communication dans un thread indépendant.
4. `ihm_mqtt_simple/` : interface finale, archivage et historique.

Le Challenge optionnel n’est pas inclus.

## Technologies

Python, PySide6, Qt Designer, QSS, Paho MQTT, SQLite et Matplotlib.

## Lancement de l’interface

Python 3.12 est recommandé. Depuis la racine du dépôt :

### macOS / Linux

```bash
cd IHM
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

### Windows — invite de commandes

```bat
cd IHM
py -3.12 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python main.py
```

Dans PyCharm, sélectionner l’interpréteur de cet environnement et exécuter `IHM/main.py`, avec `IHM/` comme répertoire de travail.

PySide6 est fixé à la version 6.8.3. Le lanceur local `run_temphumix.py` du Mac de l’auteur n’est pas inclus dans le dépôt.

## Connexion MQTT

| Paramètre | Valeur du TP |
|---|---|
| Broker | `192.168.1.1` |
| Port | `1883` |
| Capteur | `44666` |
| Préfixe | `/iot` |
| Topics | MAJUSCULES |
| Serveur NTP du dispositif | `192.168.1.254` |

L’ordinateur et le dispositif doivent avoir accès au réseau de l’expérience. Renseigner les identifiants MQTT du TP dans l’interface.

Cliquer sur **Connecter**, puis **Synchroniser**, et démarrer les mesures. Les commandes permettent ensuite de contrôler le dispositif.

Sans matériel, le mode démonstration permet de découvrir l’interface.

### Topics reçus

- `/iot/TEMPERATURE_44666`
- `/iot/HUMIDITY_44666`
- `/iot/GET_DATE_44666`
- `/iot/VERSION_44666`

### Topics de commande

- `/iot/COMMAND_44666`
- `/iot/BLINK_44666`
- `/iot/BARGRAPH_44666`

Les commandes sont envoyées sans retain. Un acquittement du broker ne garantit pas l’exécution matérielle.

## Base de données et historique

La base `IHM/IOT.db` est créée lors de l’acquisition réelle.

La table `IOT_DATA` contient :
`Id_capteur`, `Date`, `Version`, `Temperature`, `Humidite`.

L’historique permet de sélectionner un intervalle de dates et de tracer les courbes. Effacer les courbes ne supprime pas les données.

Le mode démonstration utilise une base séparée : `IOT_demo.db`. Les bases locales et les environnements Python ne sont pas versionnés.

## Gestion du projet

Git conserve les étapes du développement. La version finale du code et le rapport sont disponibles sur la branche `main`.
