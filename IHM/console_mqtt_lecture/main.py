import sys
from pathlib import Path
if __package__ in (None, ''):
    folder = Path(__file__).resolve().parent
    root = next(path for path in folder.parents if (path / 'config_tp.py').is_file())
    sys.path.insert(0, str(root))
    __package__ = '.'.join(folder.relative_to(root).parts)

from .client_mqtt import ClientMQTT
from config_tp import console_settings
from commandes import subscriptions


def main():
    cfg = console_settings('§3.3 — Lecture MQTT, sans thread ni SQLite')
    id_pc = cfg['sensor_id']
    mqtt = ClientMQTT(cfg['host'], cfg['port'], f'Client_L{id_pc}',
                      cfg['username'], cfg['password'], cfg['prefix'], id_pc)
    for name in subscriptions(cfg['prefix'], id_pc, cfg['uppercase']):
        mqtt.subscribe_mqtt(name)
    try:
        print('Démarrage de la lecture — Ctrl+C pour quitter', flush=True)
        mqtt.connect_mqtt()
        mqtt.wait_mqtt(timeout=0)
    except KeyboardInterrupt:
        print('Arrêt demandé')
    except OSError as error:
        print(f'Erreur réseau : {error}')
    finally:
        mqtt.disconnect_mqtt()


if __name__ == '__main__':
    main()
