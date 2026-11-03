"""Aide visuelle séparée du TP : messages locaux explicitement simulés."""
from threading import Thread, Event
from queue import Queue, Empty
from types import SimpleNamespace
from datetime import datetime
import math
from .client_mqtt import ClientMQTT
from commandes import topic


class DemoThread(Thread):
    def __init__(self, cfg, events):
        super().__init__(name='DEMO', daemon=True)
        self.cfg, self.events = cfg, events
        self.active = True
        self.stop_event = Event()
        self.commands = Queue()
        self.mqtt = ClientMQTT('simulation', 1883, 'DEMO', prefix=cfg['prefix'],
            sensor_id=cfg['sensor_id'], emit=lambda kind, value: events.put((kind, value)))

    def send(self, messages):
        self.commands.put(list(messages))

    def stopthread(self):
        self.stop_event.set()

    def run(self):
        emit = self.mqtt.emit
        try:
            self.mqtt.connect_sqlite(self.cfg['database'])
            self.mqtt.connected = True
            emit('connected', True)
            emit('status', 'DÉMONSTRATION · données simulées · aucun matériel commandé')
            tick = 0
            while not self.stop_event.is_set():
                while True:
                    try:
                        batch = self.commands.get_nowait()
                    except Empty:
                        break
                    for name, value in batch:
                        emit('log', f'DÉMO TX {name} = {value} (simulation)')
                        if '/COMMAND_' in name.upper():
                            if value == '20': self.active = True
                            elif value == '30': self.active = False
                if self.active:
                    values = [('VERSION', 'DÉMO'),
                              ('TEMPERATURE', f'{22 + math.sin(tick / 7) * 1.8:.1f}'),
                              ('HUMIDITY', f'{48 + math.cos(tick / 9) * 4:.1f}'),
                              ('GET_DATE', datetime.now().strftime('%d/%m/%Y %H:%M:%S'))]
                    for kind, value in values:
                        message = SimpleNamespace(topic=topic(self.cfg['prefix'], kind,
                            self.cfg['sensor_id']), payload=value.encode())
                        self.mqtt._on_message(None, None, message)
                tick += 1
                self.stop_event.wait(2)
        except Exception as error:
            emit('fatal', str(error))
        finally:
            self.mqtt.disconnect_sqlite()
            self.mqtt.connected = False
            emit('connected', False)
            emit('finished', True)
