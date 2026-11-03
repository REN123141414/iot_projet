"""TP §6 : même présentation, fonctions ajoutées dans l’ordre du support."""
import sys
from pathlib import Path
if __package__ in (None, ''):
    folder = Path(__file__).resolve().parent
    root = next(path for path in folder.parents if (path / 'config_tp.py').is_file())
    sys.path.insert(0, str(root))
    __package__ = '.'.join(folder.relative_to(root).parts)
from datetime import datetime
from queue import Queue, Empty
import time
from uuid import uuid4
from PySide6.QtCore import QTimer, QSize
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QScrollArea
from config_tp import load_settings, save_settings, database_path, ROOT
from commandes import command_messages, subscriptions, DATE_FORMAT
from .client_mqtt import ClientMQTT
from .thread_mqtt import ThreadMQTT
from .demo import DemoThread
from .mon_ihm import Ui_MainWindow
from .icons import icon
from .database import Database
from .recent_trend import RecentTrend
from .dialogue_courbe import CourbeDialog


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Navigation indépendante ; seul le contenu défile sur un petit écran.
        self.shellLayout.removeWidget(self.mainContent)
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setWidget(self.mainContent)
        self.shellLayout.addWidget(scroll)
        self.rootLayout.setContentsMargins(26, 24, 26, 18)
        self.rootLayout.setSpacing(20)
        self.dataLayout.setSpacing(14)
        self.chartContainer.setMinimumHeight(100)
        self.connectionBadge.setMaximumHeight(34)
        self.connectionBadge.setMinimumWidth(100)
        self.btnQuickConnect.setMinimumWidth(110)
        self.headerLayout.setStretch(0, 1)
        self.cmbSensor.setMinimumWidth(112)
        self.cmbSensor.setMaximumWidth(150)
        self.logView.setMinimumHeight(250)
        self.trend = RecentTrend(self.chartContainer)
        self.chartLayout.addWidget(self.trend)
        self._trend_key = None
        self.navigation = [self.btnOverview, self.btnHardware, self.btnSettings, self.btnLogs]
        self.nav_labels = {self.btnOverview: 'Vue d’ensemble', self.btnCurves: 'Historique',
                           self.btnHardware: 'Équipement', self.btnSettings: 'Connexion',
                           self.btnLogs: 'Journal'}
        for button, symbol in ((self.btnOverview, 'overview'), (self.btnCurves, 'history'),
                               (self.btnHardware, 'hardware'), (self.btnSettings, 'settings'),
                               (self.btnLogs, 'logs')):
            button.setIcon(icon(symbol, '#7d8493'))
            button.setIconSize(QSize(18, 18))
            button.setToolTip(self.nav_labels[button])
            button.setProperty('navigation', True)
        for index, button in enumerate(self.navigation):
            button.setCheckable(True)
            button.setAutoExclusive(True)
            button.clicked.connect(lambda checked=False, index=index: self.show_page(index))
        self.btnQuickConnect.clicked.connect(self.quick_connection)
        self.btnStartMeasure.setIcon(icon('play', '#ffffff'))
        self.btnStopMeasure.setIcon(icon('pause', '#656b7b'))
        self.show_page(0)
        self.settings = load_settings()
        self.events = Queue()
        self.mqtt = None
        self.thread_mqtt = None
        self.demo_mode = False
        self.connected = False
        self.last_state = {}
        self.database = database_path(self.settings)
        self.restore_settings()
        self.logView.setMaximumBlockCount(350)
        self.lneBlink.setValidator(QIntValidator(100, 60000, self))
        self.lneBargraph.setValidator(QIntValidator(0, 1023, self))
        self.command_buttons = [self.btnSynchroDateTime, self.btnStartMeasure,
            self.btnStopMeasure, self.btnSlowBlink, self.btnFastBlink,
            self.btnBlink, self.btnBargraph]
        self.btnConnect.clicked.connect(self.connectMQTT)
        self.btnDisconnect.clicked.connect(self.disconnectMQTT)
        self.btnDemo.clicked.connect(self.start_demo)
        self.profileCombo.currentIndexChanged.connect(self.choose_profile)
        self.btnSynchroDateTime.clicked.connect(self.updateDateTime)
        self.btnStartMeasure.clicked.connect(self.startMeasure)
        self.btnStopMeasure.clicked.connect(self.stopMeasure)
        self.btnSlowBlink.clicked.connect(self.slowBlink)
        self.btnFastBlink.clicked.connect(self.fastBlink)
        self.btnBlink.clicked.connect(self.customBlink)
        self.btnBargraph.clicked.connect(self.setBargraph)
        # §4.5 p.14–15 : validation du QLineEdit par Entrée.
        self.lneBargraph.returnPressed.connect(self.setBargraph)
        self.lneBlink.returnPressed.connect(self.customBlink)
        self.lneBargraph.textChanged.connect(self.preview_bargraph)
        # §4.5 : ce timer n’est actif que pendant la session d’acquisition.
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.display)
        # Les événements de fin de thread restent traités après l’arrêt du timer d’affichage.
        self.eventTimer = QTimer(self)
        self.eventTimer.timeout.connect(self.process_events)
        self.eventTimer.start(100)
        self.btnCurves.clicked.connect(self.open_curves)
        self.refresh_database()
        self.set_controls(False)
        self.display()
        self.statusbar.showMessage('Prêt · paramètres du réseau dans Connexion')
        self.log('TP : quatre topics du capteur configuré. Démonstration séparée.')

    def show_page(self, index):
        self.pages.setCurrentIndex(index)
        self.navigation[index].setChecked(True)
        copy = [('Vue d’ensemble', 'Votre environnement, en un regard.'),
                ('Équipement', 'Les commandes avancées de votre capteur.'),
                ('Connexion', 'Un espace dédié aux paramètres du réseau.'),
                ('Journal', 'Les événements de la session, dans l’ordre.')]
        title, subtitle = copy[index]
        self.titleLabel.setText(title)
        self.subtitleLabel.setText(subtitle)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not hasattr(self, 'nav_labels'):
            return
        compact = self.width() < 1050
        self.sidebar.setFixedWidth(66 if compact else 196)
        self.brandName.setVisible(not compact)
        self.brandSub.setVisible(not compact)
        self.navCaption.setVisible(not compact)
        self.sidebarFooter.setVisible(not compact)
        for button, label in self.nav_labels.items():
            button.setText('' if compact else label)
        self.sidebarLayout.setContentsMargins(12 if compact else 18, 24,
                                              12 if compact else 18, 22)

    def choose_profile(self, index):
        if index == 0:
            self.lneHost.setText('10.120.2.3')
            self.spnPort.setValue(1883)
            self.lneUsername.setText('mos_user')
            self.lnePassword.setText('mos_user')
            self.caseCombo.setCurrentIndex(1)
        elif index == 1:
            self.lneHost.setText('192.168.1.1')
            self.spnPort.setValue(1883)
            self.caseCombo.setCurrentIndex(0)

    def quick_connection(self):
        if self.thread_mqtt is None:
            self.connectMQTT()
        else:
            self.disconnectMQTT()

    def restore_settings(self):
        cfg = self.settings
        self.profileCombo.setCurrentIndex(2)
        self.lneHost.setText(cfg['host'])
        self.spnPort.setValue(int(cfg['port']))
        self.lneUsername.setText(cfg['username'])
        self.lnePassword.setText(cfg['password'])
        self.spnSensor.setValue(int(cfg['sensor_id']))
        self.cmbSensor.setText(str(cfg['sensor_id']))
        self.lnePrefix.setText(cfg['prefix'])
        self.caseCombo.setCurrentIndex(0 if cfg['uppercase'] else 1)

    def read_settings(self):
        cfg = dict(self.settings)
        cfg.update(host=self.lneHost.text().strip(), port=self.spnPort.value(),
                   username=self.lneUsername.text().strip(), password=self.lnePassword.text(),
                   sensor_id=self.spnSensor.value(), prefix=self.lnePrefix.text().strip(),
                   uppercase=self.caseCombo.currentIndex() == 0)
        if not cfg['host'] or '://' in cfg['host']:
            raise ValueError('Saisir une adresse IP ou un hôte sans mqtt://')
        if not cfg['prefix'].strip('/') or any(c in cfg['prefix'] for c in '#+ '):
            raise ValueError('Préfixe de topic invalide')
        return cfg

    def set_controls(self, connected):
        self.connected = connected
        for button in self.command_buttons:
            button.setEnabled(connected)
        running = self.thread_mqtt is not None
        self.btnConnect.setEnabled(not running)
        self.btnDisconnect.setEnabled(running)
        self.btnDemo.setEnabled(not running)
        self.btnQuickConnect.setText('Déconnecter' if running else 'Connecter')
        self.btnQuickConnect.setEnabled(True)
        for field in (self.profileCombo, self.lneHost, self.spnPort, self.lneUsername,
                      self.lnePassword, self.spnSensor, self.lnePrefix, self.caseCombo):
            field.setEnabled(not running)
        text = '●  DÉMO' if self.demo_mode else ('●  EN LIGNE' if connected else
               '●  CONNEXION…' if running else '●  HORS LIGNE')
        self.connectionBadge.setText(text)
        color, background = ('#94631b', '#fff2d8') if self.demo_mode else (
            ('#167d68', '#e6f5ee') if connected else ('#747b8b', '#eceef3'))
        self.connectionBadge.setStyleSheet(
            f'color:{color};background:{background};border-radius:15px;padding:7px 12px;')

    def _emit(self, kind, value):
        # Le thread ne touche jamais aux widgets Qt.
        self.events.put((kind, value))

    def _begin(self, demo=False):
        try:
            self.settings = self.read_settings()
            save_settings(self.settings)
            self.demo_mode = demo
            self.events = Queue()
            self.last_state = {}
            self.cmbSensor.setText(str(self.settings['sensor_id']))
            self.database = ROOT / 'IOT_demo.db' if demo else database_path(self.settings)
            if demo:
                cfg = dict(self.settings)
                cfg['database'] = str(self.database)
                self.thread_mqtt = DemoThread(cfg, self.events)
                self.mqtt = self.thread_mqtt.mqtt
            else:
                cfg = self.settings
                self.mqtt = ClientMQTT(cfg['host'], cfg['port'],
                    f"Client_IHM{cfg['sensor_id']}_{uuid4().hex[:8]}",
                    cfg['username'], cfg['password'], cfg['prefix'], cfg['sensor_id'], self._emit)
                for name in subscriptions(cfg['prefix'], cfg['sensor_id'], cfg['uppercase']):
                    self.mqtt.subscribe_mqtt(name)
                self.mqtt.database_name = self.database
                self.thread_mqtt = ThreadMQTT(self.mqtt)
            self.set_controls(False)
            self.timer.start(1000)
            self.thread_mqtt.start()
        except Exception as error:
            self.timer.stop()
            self.thread_mqtt = None
            self.demo_mode = False
            self.set_controls(False)
            self.log(f'ERREUR : {error}')
            QMessageBox.warning(self, 'Démarrage impossible', str(error))

    def connectMQTT(self):
        # §4.5 : paramètres, ClientMQTT, ThreadMQTT puis timer à 1000 ms.
        if self.thread_mqtt is None:
            self._begin(False)

    def start_demo(self):
        if self.thread_mqtt is None:
            self._begin(True)

    def disconnectMQTT(self):
        # §4.5 : arrêter le timer puis demander l’arrêt du thread de lecture.
        self.timer.stop()
        if self.thread_mqtt is not None:
            self.thread_mqtt.stopthread()
            self.set_controls(False)
            self.btnDisconnect.setEnabled(False)
            self.btnQuickConnect.setEnabled(False)
            self.statusbar.showMessage('Déconnexion en cours…')

    def process_events(self):
        archived = False
        for _ in range(500):
            try:
                kind, value = self.events.get_nowait()
            except Empty:
                break
            if kind == 'sample':
                self.last_state = value
            elif kind == 'archived':
                archived = True
            elif kind == 'connected':
                self.set_controls(bool(value))
            elif kind == 'status':
                self.statusbar.showMessage(value)
            elif kind in ('error', 'fatal'):
                self.log(f'ERREUR : {value}')
                if kind == 'fatal':
                    self.disconnectMQTT()
            elif kind == 'log':
                self.log(value)
            elif kind == 'finished':
                if self.thread_mqtt is not None:
                    self.thread_mqtt.join(timeout=.2)
                self.thread_mqtt = None
                self.demo_mode = False
                self.timer.stop()
                self.set_controls(False)
                self.statusbar.showMessage('Déconnecté')
                self.render_selected()
        if archived:
            self.refresh_database()
            pass

    def display(self):
        # §3.6.2 / §4.5 : lecture des variables de l’instance ClientMQTT.
        self.process_events()
        if self.mqtt is not None:
            self.last_state = self.mqtt.snapshot()
        self.render_selected()

    def render_selected(self):
        sid = self.settings['sensor_id']
        state = self.last_state
        if not state.get('received_at'):
            try:
                db = Database(self.database)
                try:
                    state = db.latest(sid) or state
                finally:
                    db.close()
            except Exception as error:
                self.log(f'ERREUR lecture SQLite : {error}')
        self.tempValue.setText(f'{state["temperature"]:.1f}' if 'temperature' in state else '—')
        self.humidityValue.setText(f'{state["humidity"]:.1f}' if 'humidity' in state else '—')
        self.versionLabel.setText('Version : ' + (state.get('version') or '—'))
        date = state.get('date')
        if date:
            date = datetime.strptime(date, DATE_FORMAT).strftime('%d/%m/%Y %H:%M:%S')
        self.deviceDateLabel.setText('Date du capteur : ' + (date or '—'))
        if state.get('received_at'):
            age = max(0, int(time.time() - state['received_at']))
            label = f'Dernière réception : il y a {age} s'
        elif state:
            label = 'Dernière mesure archivée · pas de réception en direct'
        else:
            label = 'En attente des données du capteur…'
        if self.demo_mode or state.get('version') == 'DÉMO':
            label = 'DÉMONSTRATION · données simulées · ' + label
        self.lastReceivedLabel.setText(label)
        self.commandTargetLabel.setText(f'Destination : capteur {sid}')
        self.refresh_trend(sid)

    def send_action(self, action, value=None):
        try:
            if self.thread_mqtt is None or not self.connected:
                raise ConnectionError('Connecter le broker avant de commander')
            messages = command_messages(self.settings['prefix'], self.settings['sensor_id'],
                                        action, value, self.settings['uppercase'])
            self.thread_mqtt.send(messages)
            self.log(f'Commande demandée : {action}')
        except (ValueError, ConnectionError) as error:
            self.log(f'ERREUR commande : {error}')
            self.statusbar.showMessage(str(error))

    def updateDateTime(self):
        self.send_action('sync')

    def synchroDateTime(self):
        self.updateDateTime()

    def startMeasure(self):
        self.send_action('start')

    def stopMeasure(self):
        self.send_action('stop')

    def slowBlink(self):
        self.send_action('slow')

    def fastBlink(self):
        self.send_action('fast')

    def customBlink(self):
        try:
            self.send_action('blink', int(self.lneBlink.text()))
        except ValueError:
            self.log('ERREUR : saisir une période entière')

    def setBargraph(self):
        try:
            self.send_action('bargraph', int(self.lneBargraph.text()))
        except ValueError:
            self.log('ERREUR : saisir un entier de 0 à 1023')

    def preview_bargraph(self, value):
        try:
            number = int(value)
        except ValueError:
            number = 0
        self.bargraphPreview.setText('  '.join('●' if number & (1 << i) else '○' for i in range(10)))
        self.bargraphPreview.setToolTip('Aperçu de la saisie ; vérifier le montage pour le retour matériel.')

    def log(self, message):
        self.logView.appendPlainText(datetime.now().strftime('%H:%M:%S') + '  ' + str(message))

    def quit(self):
        self.close()

    def closeEvent(self, event):
        self.timer.stop()
        if self.thread_mqtt is not None:
            self.thread_mqtt.stopthread()
            self.thread_mqtt.join(timeout=4)
            if self.thread_mqtt.is_alive():
                self.statusbar.showMessage('Fermeture du réseau en cours…')
                event.ignore()
                return
        event.accept()

    def refresh_database(self):
        try:
            db = Database(self.database)
            try:
                count = db.count(self.settings['sensor_id'])
            finally:
                db.close()
            self.archiveCountLabel.setText(f'{count:,}'.replace(',', ' ') + ' mesures archivées')
            self.databaseLabel.setText(f'Base : {self.database.name}')
            self._trend_key = None
        except Exception as error:
            self.log(f'ERREUR SQLite : {error}')

    def refresh_trend(self, sid):
        key = (str(self.database), sid)
        if self._trend_key == key:
            return
        try:
            db = Database(self.database)
            try:
                self.trend.set_rows(db.recent(sid))
            finally:
                db.close()
            self._trend_key = key
        except Exception as error:
            self.log(f'ERREUR courbe récente : {error}')

    def open_curves(self):
        try:
            dialog = CourbeDialog(self.database, int(self.cmbSensor.text()), self)
            dialog.exec()
        except Exception as error:
            QMessageBox.warning(self, 'Historique', str(error))

def run():
    app = QApplication(sys.argv)
    app.setApplicationName('TempHumiX')
    app.setStyle('Fusion')
    app.setStyleSheet(Path(__file__).with_name('style.qss').read_text(encoding='utf-8'))
    window = MainWindow()
    window.setWindowTitle('TempHumiX — Supervision IoT')
    screen = app.primaryScreen()
    if screen:
        rect = screen.availableGeometry()
        window.resize(min(1180, max(600, rect.width()-50)),
                      min(780, max(500, rect.height()-70)))
    window.show()
    return app.exec()


if __name__ == '__main__':
    sys.exit(run())
