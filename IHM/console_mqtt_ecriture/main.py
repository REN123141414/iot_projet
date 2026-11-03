import sys
from pathlib import Path
if __package__ in (None, ''):
    folder = Path(__file__).resolve().parent
    root = next(path for path in folder.parents if (path / 'config_tp.py').is_file())
    sys.path.insert(0, str(root))
    __package__ = '.'.join(folder.relative_to(root).parts)

from .client_mqtt import ClientMQTT
from config_tp import console_settings
from commandes import command_messages


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
    cfg = console_settings('§3.4–3.5 — Écriture MQTT, sans ThreadMQTT ni SQLite')
    id_pc = cfg['sensor_id']
    mqtt = ClientMQTT(cfg['host'], cfg['port'], f'Client_E{id_pc}',
                      cfg['username'], cfg['password'], cfg['prefix'], id_pc)
    try:
        mqtt.connect_mqtt()
        # Boucle réseau interne à Paho pendant input(), pas la classe du §3.6.
        mqtt.client.loop_start()
        if not mqtt.connected_event.wait(6) or not mqtt.connected:
            raise ConnectionError('Connexion MQTT non confirmée')
        def send(messages):
            for name, value in messages:
                mqtt.publish_mqtt(name, value, qos=1).wait_for_publish(timeout=3)
        menu(send, cfg)
    except (KeyboardInterrupt, EOFError):
        pass
    except (OSError, ConnectionError, RuntimeError) as error:
        print(f'Erreur : {error}')
    finally:
        mqtt.disconnect_mqtt()
        mqtt.client.loop_stop()
        print('Fin de l’application')


if __name__ == '__main__':
    main()
