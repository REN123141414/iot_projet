"""§5–6 : ajout de SQLite au ClientMQTT développé aux étapes précédentes."""
from threading import Event
from datetime import datetime
from threading import Lock
import math
import sqlite3
import time
from paho.mqtt import client as mqtt_client


class ClientMQTT:
    def __init__(self, ip_address, port, client_id, username='', password='',
                 prefix='/iot', sensor_id=44666, emit=None):
        self.ip_address = ip_address
        self.port = int(port)
        self.client_id = client_id
        self.username = username
        self.password = password
        self.prefix = '/' + prefix.strip('/')
        self.id_capteur = int(sensor_id)
        self.emit = emit or (lambda kind, value: print(f'{kind} : {value}', flush=True))
        self.connected = False
        self.rejected = False
        self.connected_event = Event()
        self.topics = []
        self.version = ''
        self.temperature = None
        self.humidite = None
        self.date_IdO = None
        self.datetime_acq = None
        self.received_at = None
        self._lock = Lock()
        self._pending = {}
        self.conn = None
        self.tablename = 'IOT_DATA'
        self.database_name = None
        self.client = mqtt_client.Client(
            callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2,
            client_id=client_id, protocol=mqtt_client.MQTTv311)
        self.client.connect_timeout = 3
        if username:
            self.client.username_pw_set(username, password)
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message
        self.client.on_subscribe = self._on_subscribe
        self.client.on_publish = self._on_publish

    # §3.2.1
    def connect_mqtt(self):
        self.connected = False
        self.rejected = False
        self.connected_event.clear()
        self.client.connect(self.ip_address, self.port, keepalive=30)
        return self.client

    # §3.2.2
    def disconnect_mqtt(self):
        self.client.disconnect()
        self.connected = False
        self.connected_event.clear()

    # §3.2.3
    def publish_mqtt(self, topic, message, qos=0):
        if not self.connected:
            raise ConnectionError('Le broker MQTT n’est pas connecté')
        info = self.client.publish(topic, str(message), qos=qos, retain=False)
        if info.rc != mqtt_client.MQTT_ERR_SUCCESS:
            raise ConnectionError(f'Échec de publication : {info.rc}')
        self.emit('log', f'Publication : {message} sur {topic}')
        return info

    # §3.2.4 : l’abonnement est rejoué après une reconnexion.
    def subscribe_mqtt(self, topic, qos=0):
        subscription = (topic, qos)
        if subscription not in self.topics:
            self.topics.append(subscription)
        if self.connected:
            result, mid = self.client.subscribe(topic, qos=qos)
            if result != mqtt_client.MQTT_ERR_SUCCESS:
                raise ConnectionError(f'Échec de souscription : {topic}')
            return result, mid
        return None

    # §3.2.5
    def wait_mqtt(self, timeout=0):
        if timeout == 0:
            return self.client.loop_forever()
        return self.client.loop(timeout=timeout)

    def _on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code != 0:
            self.rejected = True
            self.emit('error', f'Connexion refusée : {reason_code}')
            self.connected_event.set()
            return
        self.connected = True
        for topic, qos in self.topics:
            client.subscribe(topic, qos=qos)
        self.connected_event.set()
        self.emit('connected', True)
        self.emit('status', f'Connecté à {self.ip_address}:{self.port}')

    def _on_disconnect(self, client, userdata, flags, reason_code, properties):
        self.connected = False
        self.connected_event.clear()
        self.clear_cycle()
        self.emit('connected', False)
        self.emit('status', f'Déconnecté ({reason_code})')

    def _on_subscribe(self, client, userdata, mid, reasons, properties):
        if any(reason.is_failure for reason in reasons):
            self.emit('error', 'Souscription refusée')
        else:
            self.emit('log', f'Souscription confirmée : {mid}')

    def _on_publish(self, client, userdata, mid, reason_code, properties):
        if reason_code.is_failure:
            self.emit('error', f'Publication refusée : {reason_code}')
        else:
            self.emit('log', f'Acquittement du broker : {mid} (pas un retour matériel)')

    def clear_cycle(self):
        with self._lock:
            self._pending.clear()

    def snapshot(self):
        with self._lock:
            state = {'sensor_id': self.id_capteur, 'version': self.version}
            for key, value in (('temperature', self.temperature), ('humidity', self.humidite),
                               ('date', self.date_IdO), ('received_at', self.received_at)):
                if value is not None:
                    state[key] = value
            return state

    def _on_message(self, client, userdata, msg):
        if not msg.topic.startswith(self.prefix + '/'):
            return
        leaf = msg.topic[len(self.prefix) + 1:]
        kind, _, raw_id = leaf.rpartition('_')
        kind = kind.upper()
        if not raw_id.isdigit() or int(raw_id) != self.id_capteur:
            return
        if kind not in ('VERSION', 'TEMPERATURE', 'HUMIDITY', 'GET_DATE'):
            return
        try:
            value = msg.payload.decode('utf-8').strip()
            row = None
            with self._lock:
                if kind == 'VERSION':
                    self.version = value
                elif kind == 'GET_DATE':
                    date = None
                    for fmt in ('%d/%m/%Y %H:%M:%S', '%Y-%m-%d %H:%M:%S'):
                        try:
                            date = datetime.strptime(value, fmt).strftime('%Y-%m-%d %H:%M:%S')
                            break
                        except ValueError:
                            pass
                    if date is None:
                        raise ValueError('Date du capteur invalide')
                    self.date_IdO = self.datetime_acq = date
                    self._pending['date'] = date
                else:
                    number = float(value.replace(',', '.'))
                    low, high = (-40, 80) if kind == 'TEMPERATURE' else (0, 100)
                    if not math.isfinite(number) or not low <= number <= high:
                        raise ValueError('Valeur du capteur hors limites')
                    if kind == 'TEMPERATURE':
                        self.temperature = number
                        self._pending['temperature'] = number
                    else:
                        self.humidite = number
                        self._pending['humidity'] = number
                self.received_at = time.time()
                if all(key in self._pending for key in ('date', 'temperature', 'humidity')):
                    row = dict(self._pending, sensor_id=self.id_capteur, version=self.version)
                    self._pending.clear()
            self.emit('log', f'Réception : {value} depuis {msg.topic}')
            self.emit('sample', self.snapshot())
            if row is not None:
                self._complete_cycle(row)
        except (ValueError, UnicodeError) as error:
            self.clear_cycle()
            self.emit('error', f'Message ignoré : {error}')
        except Exception as error:
            self.emit('fatal', f'Acquisition : {error}')

    # §5.2 : noms snake_case du squelette p.18 et alias camelCase p.17.
    def connect_sqlite(self, filename, tablename='IOT_DATA'):
        if tablename.upper() != 'IOT_DATA':
            raise ValueError('Table attendue : IOT_DATA')
        from pathlib import Path
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(path), timeout=5)
        self.tablename = 'IOT_DATA'
        self.conn.execute('PRAGMA journal_mode=WAL')
        self.conn.execute('CREATE TABLE IF NOT EXISTS IOT_DATA ('
                          'Id_capteur integer, Date text, Version text, '
                          'Temperature real, Humidite real)')
        self.conn.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_sample '
                          'ON IOT_DATA (Id_capteur, Date, Temperature, Humidite)')
        self.conn.commit()

    def disconnect_sqlite(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def connectSQLite(self, filename, tablename='IOT_DATA'):
        return self.connect_sqlite(filename, tablename)

    def disconnectSQLite(self):
        return self.disconnect_sqlite()

    def _complete_cycle(self, row):
        # p.18 : écrire lorsque le dernier des trois topics de mesure arrive.
        # Le montage REN publie GET_DATE en dernier ; d’autres montages finissent par HUMIDITY.
        if self.conn is None:
            return
        cursor = self.conn.execute('INSERT OR IGNORE INTO IOT_DATA VALUES (?,?,?,?,?)',
            (row['sensor_id'], row['date'], row['version'], row['temperature'], row['humidity']))
        self.conn.commit()
        if cursor.rowcount:
            self.emit('archived', row)
