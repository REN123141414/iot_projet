"""Deux mini-courbes exactes, issues des 30 dernières lignes SQLite du capteur."""
from datetime import datetime
from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtGui import QColor, QFont, QPainter, QPainterPath, QPen, QLinearGradient
from PySide6.QtWidgets import QWidget, QSizePolicy
from commandes import DATE_FORMAT


class RecentTrend(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.rows = []
        self.setMinimumHeight(100)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setToolTip('Valeurs archivées du capteur sélectionné. Chaque courbe possède sa propre échelle.')

    def set_rows(self, rows):
        self.rows = rows
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        font = QFont(self.font())
        font.setPointSize(9)
        painter.setFont(font)
        if not self.rows:
            painter.setPen(QColor('#9499a7'))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter,
                             'Les tendances apparaîtront avec les premières mesures.')
            return
        dates = [datetime.strptime(row[0], DATE_FORMAT) for row in self.rows]
        xs = [(date - dates[0]).total_seconds() for date in dates]
        duration = max(xs[-1], 1)
        width, height = self.width(), self.height()
        plot_width = max(1, width - 12)
        row_height = (height - 20) / 2
        for index, column, color, label, unit in ((0, 1, '#7061cf', 'Température', '°C'),
                                                  (1, 2, '#31998c', 'Humidité', '%')):
            top = index * row_height
            values = [float(row[column]) for row in self.rows]
            vmin, vmax = min(values), max(values)
            pad = max((vmax-vmin) * .2, .2)
            lo, hi = vmin-pad, vmax+pad
            graph_top, graph_height = top+23, max(8, row_height-31)
            painter.setPen(QColor(color))
            painter.drawText(QPointF(0, top+12), label)
            painter.setPen(QColor('#8d93a2'))
            painter.drawText(QRectF(0, top, width, 18), Qt.AlignmentFlag.AlignRight,
                             f'{vmin:.1f} – {vmax:.1f} {unit}')
            painter.setPen(QPen(QColor('#eceef3'), 1))
            painter.drawLine(QPointF(0, graph_top+graph_height), QPointF(width, graph_top+graph_height))
            points = [QPointF(6 + x/duration*plot_width,
                               graph_top+(hi-value)/(hi-lo)*graph_height)
                      for x, value in zip(xs, values)]
            path = QPainterPath(points[0])
            for point in points[1:]:
                path.lineTo(point)
            area = QPainterPath(path)
            area.lineTo(points[-1].x(), graph_top+graph_height)
            area.lineTo(points[0].x(), graph_top+graph_height)
            area.closeSubpath()
            gradient = QLinearGradient(0, graph_top, 0, graph_top+graph_height)
            tint = QColor(color); tint.setAlpha(40)
            gradient.setColorAt(0, tint); tint.setAlpha(0); gradient.setColorAt(1, tint)
            painter.fillPath(area, gradient)
            painter.setPen(QPen(QColor(color), 2, Qt.PenStyle.SolidLine,
                                Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawPath(path)
            painter.setBrush(QColor(color))
            painter.drawEllipse(points[-1], 3, 3)
        painter.setPen(QColor('#9499a7'))
        fmt = '%d/%m %H:%M:%S' if dates[-1].date() != dates[0].date() else '%H:%M:%S'
        painter.drawText(QRectF(0, height-16, width/2, 16), Qt.AlignmentFlag.AlignLeft, dates[0].strftime(fmt))
        painter.drawText(QRectF(width/2, height-16, width/2, 16), Qt.AlignmentFlag.AlignRight, dates[-1].strftime(fmt))
