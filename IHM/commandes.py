"""Commandes du tableau de la page 4 et du menu de la page 9."""
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

def topic(prefix, kind, sensor_id, uppercase=True):
    name = kind.upper() if uppercase else kind.lower()
    return f"/{prefix.strip('/')}/{name}_{int(sensor_id)}"

def subscriptions(prefix, sensor_id, uppercase=True):
    # Quatre données du TP, uniquement pour le capteur configuré.
    return [topic(prefix, kind, sensor_id, uppercase)
            for kind in ('VERSION', 'TEMPERATURE', 'HUMIDITY', 'GET_DATE')]

def command_messages(prefix, sensor_id, action, value=None, uppercase=True):
    command = topic(prefix, 'COMMAND', sensor_id, uppercase)
    codes = {'sync': (10,), 'start': (20, 50), 'stop': (30, 40),
             'slow': (40,), 'fast': (50,)}
    if action in codes:
        return [(command, str(code)) for code in codes[action]]
    if action == 'blink':
        if not isinstance(value, int) or not 100 <= value <= 60000 or value % 100:
            raise ValueError('Période : 100 à 60000 ms, par pas de 100 ms')
        return [(topic(prefix, 'BLINK', sensor_id, uppercase), str(value)), (command, '60')]
    if action == 'bargraph':
        if not isinstance(value, int) or not 0 <= value <= 1023:
            raise ValueError('Bargraphe : entier entre 0 et 1023')
        return [(topic(prefix, 'BARGRAPH', sensor_id, uppercase), str(value))]
    raise ValueError('Commande inconnue')
