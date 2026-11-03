"""§3.2 : cinq méthodes MQTT ; Paho 2.x, sans archivage ni ThreadMQTT."""
from threading import Event
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

    def _on_message(self, client, userdata, msg):
        value = msg.payload.decode('utf-8', errors='replace')
        self.emit('log', f'Réception : {value} depuis {msg.topic}')
