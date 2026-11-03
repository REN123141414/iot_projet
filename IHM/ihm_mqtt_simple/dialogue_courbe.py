"""§6 : boîte de dialogue Qt, requête SQLite et graphique Matplotlib."""
from datetime import datetime, timedelta
from PySide6.QtCore import QDateTime, Qt
from PySide6.QtGui import QImage, QPixmap, QPainter
from PySide6.QtWidgets import QDialog, QGraphicsScene
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib import dates as mdates
from .database import Database
from commandes import DATE_FORMAT
from .graphe import Ui_GraphWindow


class CourbeDialog(QDialog, Ui_GraphWindow):
    def __init__(self, database, selected_sensor, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.database = database
        self.resize(1120, 700)
        self.graphTitle.setObjectName('titleLabel')
        if database.name == 'IOT_demo.db':
            self.graphTitle.setText('Historique des mesures · DÉMONSTRATION')
        self.scene = QGraphicsScene(self)
        self.graphicsView.setScene(self.scene)
        self.graphicsView.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.item = None
        self.cmbSensor.setText(str(selected_sensor))
        end = QDateTime.currentDateTime()
        self.dteStartTime.setDateTime(end.addSecs(-3600))
        self.dteEndTime.setDateTime(end)
        self.btnLoadData.clicked.connect(self.afficher_courbe)
        self.btnClearData.clicked.connect(self.effacer_courbe)
        self.btnClose.clicked.connect(self.close)

    def figure_to_pixmap(self, fig):
        canvas = FigureCanvasAgg(fig)
        canvas.draw()
        width, height = canvas.get_width_height()
        # La copie conserve les pixels après destruction du canvas local.
        image = QImage(canvas.buffer_rgba(), width, height,
                       QImage.Format.Format_RGBA8888).copy()
        return QPixmap.fromImage(image)

    def afficher_courbe(self):
        start = self.dteStartTime.dateTime().toString('yyyy-MM-dd HH:mm:ss')
        end = self.dteEndTime.dateTime().toString('yyyy-MM-dd HH:mm:ss')
        if start > end:
            self.lblResult.setText('La date de début doit précéder la date de fin.')
            return
        try:
            db = Database(self.database)
            try:
                rows = db.query(int(self.cmbSensor.text()), start, end)
            finally:
                db.close()
        except Exception as error:
            self.lblResult.setText(f'Lecture impossible : {error}')
            return
        self.scene.clear()
        self.item = None
        if not rows:
            self.lblResult.setText('Aucune mesure pour ce capteur dans cet intervalle.')
            return
        fig = Figure(figsize=(10, 4.8), dpi=120, layout='constrained', facecolor='#ffffff')
        ax = fig.add_subplot(111)
        right = ax.twinx()
        dates = [datetime.strptime(row[0], DATE_FORMAT) for row in rows]
        line_t, = ax.plot(dates, [r[1] for r in rows], color='#7061cf',
                          marker='o', markersize=3, label='Température (°C)')
        line_h, = right.plot(dates, [r[2] for r in rows], color='#31998c',
                             marker='+', markersize=4, label='Humidité (%)')
        ax.set_title(f'Capteur {self.cmbSensor.text()} · température et humidité', pad=15)
        ax.set_xlabel('Date et heure du capteur')
        ax.set_ylabel('Température (°C)', color='#7061cf')
        right.set_ylabel('Humidité (%)', color='#31998c')
        locator = mdates.AutoDateLocator(minticks=3, maxticks=7)
        lo, hi = datetime.strptime(start, DATE_FORMAT), datetime.strptime(end, DATE_FORMAT)
        ax.set_xlim(lo, hi if hi > lo else lo + timedelta(seconds=1))
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))
        ax.grid(alpha=.12)
        for axes in (ax, right):
            axes.spines['top'].set_visible(False)
            for edge in ('left', 'right', 'bottom'):
                axes.spines[edge].set_color('#e3e5ee')
            axes.tick_params(colors='#858b9b', labelsize=9)
        ax.legend(handles=[line_t, line_h], loc='upper left', frameon=False)
        self.item = self.scene.addPixmap(self.figure_to_pixmap(fig))
        self.scene.setSceneRect(self.item.boundingRect())
        self.graphicsView.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        self.lblResult.setText(f'{len(rows)} mesure(s) · {self.database.name}')

    def effacer_courbe(self):
        self.scene.clear()
        self.item = None
        self.lblResult.setText('Courbes effacées. Les données SQLite sont conservées.')

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if getattr(self, 'item', None) is not None:
            self.graphicsView.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
