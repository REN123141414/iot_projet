# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'graphe.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDateTimeEdit, QDialog, QGraphicsView,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_GraphWindow(object):
    def setupUi(self, GraphWindow):
        if not GraphWindow.objectName():
            GraphWindow.setObjectName(u"GraphWindow")
        GraphWindow.resize(1240, 880)
        self.graphRoot = QVBoxLayout(GraphWindow)
        self.graphRoot.setObjectName(u"graphRoot")
        self.graphTitle = QLabel(GraphWindow)
        self.graphTitle.setObjectName(u"graphTitle")

        self.graphRoot.addWidget(self.graphTitle)

        self.graphFilters = QHBoxLayout()
        self.graphFilters.setObjectName(u"graphFilters")
        self.graphSensorCaption = QLabel(GraphWindow)
        self.graphSensorCaption.setObjectName(u"graphSensorCaption")

        self.graphFilters.addWidget(self.graphSensorCaption)

        self.cmbSensor = QLabel(GraphWindow)
        self.cmbSensor.setObjectName(u"cmbSensor")

        self.graphFilters.addWidget(self.cmbSensor)

        self.dteStartTimeCaption = QLabel(GraphWindow)
        self.dteStartTimeCaption.setObjectName(u"dteStartTimeCaption")

        self.graphFilters.addWidget(self.dteStartTimeCaption)

        self.dteStartTime = QDateTimeEdit(GraphWindow)
        self.dteStartTime.setObjectName(u"dteStartTime")
        self.dteStartTime.setCalendarPopup(True)

        self.graphFilters.addWidget(self.dteStartTime)

        self.dteEndTimeCaption = QLabel(GraphWindow)
        self.dteEndTimeCaption.setObjectName(u"dteEndTimeCaption")

        self.graphFilters.addWidget(self.dteEndTimeCaption)

        self.dteEndTime = QDateTimeEdit(GraphWindow)
        self.dteEndTime.setObjectName(u"dteEndTime")
        self.dteEndTime.setCalendarPopup(True)

        self.graphFilters.addWidget(self.dteEndTime)


        self.graphRoot.addLayout(self.graphFilters)

        self.graphicsView = QGraphicsView(GraphWindow)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setMinimumHeight(420)

        self.graphRoot.addWidget(self.graphicsView)

        self.lblResult = QLabel(GraphWindow)
        self.lblResult.setObjectName(u"lblResult")

        self.graphRoot.addWidget(self.lblResult)

        self.graphButtons = QHBoxLayout()
        self.graphButtons.setObjectName(u"graphButtons")
        self.btnLoadData = QPushButton(GraphWindow)
        self.btnLoadData.setObjectName(u"btnLoadData")

        self.graphButtons.addWidget(self.btnLoadData)

        self.btnClearData = QPushButton(GraphWindow)
        self.btnClearData.setObjectName(u"btnClearData")

        self.graphButtons.addWidget(self.btnClearData)

        self.btnClose = QPushButton(GraphWindow)
        self.btnClose.setObjectName(u"btnClose")

        self.graphButtons.addWidget(self.btnClose)


        self.graphRoot.addLayout(self.graphButtons)


        self.retranslateUi(GraphWindow)

        QMetaObject.connectSlotsByName(GraphWindow)
    # setupUi

    def retranslateUi(self, GraphWindow):
        GraphWindow.setWindowTitle(QCoreApplication.translate("GraphWindow", u"TempHumiX \u2014 Historique des mesures", None))
        self.graphTitle.setText(QCoreApplication.translate("GraphWindow", u"Historique des mesures", None))
        self.graphSensorCaption.setText(QCoreApplication.translate("GraphWindow", u"Capteur", None))
        self.dteStartTimeCaption.setText(QCoreApplication.translate("GraphWindow", u"D\u00e9but", None))
        self.dteStartTime.setDisplayFormat(QCoreApplication.translate("GraphWindow", u"dd/MM/yyyy HH:mm:ss", None))
        self.dteEndTimeCaption.setText(QCoreApplication.translate("GraphWindow", u"Fin", None))
        self.dteEndTime.setDisplayFormat(QCoreApplication.translate("GraphWindow", u"dd/MM/yyyy HH:mm:ss", None))
        self.lblResult.setText(QCoreApplication.translate("GraphWindow", u"Choisir un intervalle puis charger les donn\u00e9es.", None))
        self.btnLoadData.setText(QCoreApplication.translate("GraphWindow", u"Charger les donn\u00e9es", None))
        self.btnClearData.setText(QCoreApplication.translate("GraphWindow", u"Effacer les courbes", None))
        self.btnClose.setText(QCoreApplication.translate("GraphWindow", u"Fermer", None))
    # retranslateUi

