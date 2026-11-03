import sys
from pathlib import Path
if __package__ in (None, ''):
    folder = Path(__file__).resolve().parent
    root = next(path for path in folder.parents if (path / 'config_tp.py').is_file())
    sys.path.insert(0, str(root))
    __package__ = '.'.join(folder.relative_to(root).parts)

import time
from .client_mqtt import ClientMQTT
from .thread_mqtt import ThreadMQTT
from config_tp import console_settings
from commandes import command_messages, subscriptions


def menu(send, cfg):
    actions = {'1': 'sync', '2': 'start', '3': 'stop', '4': 'slow',
               '5': 'fast', '6': 'blink', '7': 'bargraph'}
    while True:
        print('\nConsole capteur IdO\n-------------------\n'
              '1 - Mise à l’heure\n2 - Démarrage des mesures\n'
              '3 - Arrêt des mesures\n4 - Clignotement lent\n'
              '5 - Clignotement rapide\n6 - Clignotement personnalisé\n'
              '7 - Écriture du bargraphe\nQ - Quitter', flush=True)
        choice = input('Votre choix : ').strip().upper()
        if choice == 'Q':
            return
        if choice not in actions:
            print('Choix inconnu')
            continue
        try:
            action = actions[choice]
            value = None
            if action == 'blink':
                value = int(input('Période en ms (multiple de 100) : '))
            elif action == 'bargraph':
                value = int(input('Valeur du bargraphe (0 à 1023) : '))
            send(command_messages(cfg['prefix'], cfg['sensor_id'], action,
                                  value, cfg['uppercase']))
        except (ValueError, ConnectionError) as error:
            print(f'Erreur : {error}')


def main():
    cfg = console_settings('§3.6 — Lecture et commandes avec ThreadMQTT')
    mqtt = ClientMQTT(cfg['host'], cfg['port'], f"Client_T{cfg['sensor_id']}",
                      cfg['username'], cfg['password'], cfg['prefix'], cfg['sensor_id'])
    for name in subscriptions(cfg['prefix'], cfg['sensor_id'], cfg['uppercase']):
        mqtt.subscribe_mqtt(name)
    thread_mqtt = ThreadMQTT(mqtt)
    thread_mqtt.start()
    try:
        if not mqtt.connected_event.wait(6) or not mqtt.connected:
            raise ConnectionError('Connexion MQTT non confirmée')
        def send(messages):
            for name, value in messages:
                mqtt.publish_mqtt(name, value, qos=1).wait_for_publish(timeout=3)
        menu(send, cfg)
    except (KeyboardInterrupt, EOFError):
        pass
    except ConnectionError as error:
        print(error)
    finally:
        thread_mqtt.stopthread()
        thread_mqtt.join(timeout=4)
        print('Fin du thread MQTT')


if __name__ == '__main__':
    main()
