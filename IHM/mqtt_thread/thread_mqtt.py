"""§3.6 : ThreadMQTT reçoit une instance de ClientMQTT."""
from threading import Thread, Event
from queue import Queue, Empty
import time


class ThreadMQTT(Thread):
    def __init__(self, client_mqtt):
        super().__init__(name='MQTT-lecture', daemon=True)
        self.mqtt = client_mqtt
        self.stop = False
        self._stop_event = Event()
        self.outgoing = Queue()

    def stopthread(self):
        self.stop = True
        self._stop_event.set()

    def send(self, messages):
        if self.stop or not self.mqtt.connected:
            raise ConnectionError('Connecter le broker avant de commander')
        self.outgoing.put(list(messages))

    def _discard_commands(self):
        while True:
            try:
                self.outgoing.get_nowait()
                self.mqtt.emit('error', 'Commande annulée après interruption de la liaison')
            except Empty:
                return

    def run(self):
        try:
            # ARCHIVE_OPEN
            while not self.stop:
                try:
                    self.mqtt.connect_mqtt()
                    deadline = time.monotonic() + 6
                    while not self.stop:
                        code = self.mqtt.wait_mqtt(timeout=0.1)
                        if self.mqtt.rejected:
                            self.stopthread()
                            break
                        if code != 0:
                            raise ConnectionError(f'Liaison perdue : {code}')
                        if not self.mqtt.connected:
                            if time.monotonic() > deadline:
                                raise TimeoutError('Pas de confirmation du broker')
                            continue
                        try:
                            batch = self.outgoing.get_nowait()
                        except Empty:
                            continue
                        for name, value in batch:
                            self.mqtt.publish_mqtt(name, value, qos=1)
                except (OSError, ConnectionError, TimeoutError) as error:
                    self.mqtt.emit('error', f'{error} · nouvelle tentative dans 3 s')
                finally:
                    self.mqtt.disconnect_mqtt()
                    self.mqtt.clear_cycle()
                    self._discard_commands()
                if not self.stop:
                    self._stop_event.wait(3)
        except Exception as error:
            self.mqtt.emit('fatal', str(error))
        finally:
            # ARCHIVE_CLOSE
            self.mqtt.emit('finished', True)
