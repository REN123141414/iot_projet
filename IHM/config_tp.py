"""Paramètres communs ; les classes de chaque étape restent dans leur dossier."""
from pathlib import Path
import argparse
import json
import os

ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / 'config.json'
DEFAULTS = dict(host='192.168.1.1', port=1883, username='mos_user',
                sensor_id=44666, prefix='/iot', uppercase=True, database='IOT.db')

def load_settings():
    values = dict(DEFAULTS)
    try:
        saved = json.loads(CONFIG.read_text(encoding='utf-8'))
        values.update({key: saved[key] for key in DEFAULTS if key in saved})
    except (OSError, ValueError, TypeError):
        pass
    values['password'] = os.environ.get('IOT_MQTT_PASSWORD', 'mos_user')
    return values

def save_settings(values):
    safe = {key: values[key] for key in DEFAULTS if key in values}
    temporary = CONFIG.with_suffix('.tmp')
    temporary.write_text(json.dumps(safe, indent=2, ensure_ascii=False), encoding='utf-8')
    temporary.replace(CONFIG)

def database_path(values):
    path = Path(values['database']).expanduser()
    return path if path.is_absolute() else ROOT / path

def console_settings(description):
    values = load_settings()
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--host', default=values['host'])
    parser.add_argument('--port', type=int, default=values['port'])
    parser.add_argument('--sensor', type=int, default=values['sensor_id'])
    parser.add_argument('--username', default=values['username'])
    parser.add_argument('--lowercase', action='store_true')
    args = parser.parse_args()
    values.update(host=args.host, port=args.port, sensor_id=args.sensor,
                  username=args.username)
    if args.lowercase:
        values['uppercase'] = False
    return values
