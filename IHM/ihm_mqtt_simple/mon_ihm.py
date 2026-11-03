# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mon_ihm.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QPlainTextEdit,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QStackedWidget, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1180, 780)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.shellLayout = QHBoxLayout(self.centralwidget)
        self.shellLayout.setSpacing(0)
        self.shellLayout.setObjectName(u"shellLayout")
        self.shellLayout.setContentsMargins(0, 0, 0, 0)
        self.sidebar = QFrame(self.centralwidget)
        self.sidebar.setObjectName(u"sidebar")
        self.sidebar.setMinimumWidth(196)
        self.sidebar.setMaximumWidth(196)
        self.sidebarLayout = QVBoxLayout(self.sidebar)
        self.sidebarLayout.setSpacing(8)
        self.sidebarLayout.setObjectName(u"sidebarLayout")
        self.sidebarLayout.setContentsMargins(18, 18, 18, 18)
        self.brandLayout = QHBoxLayout()
        self.brandLayout.setSpacing(8)
        self.brandLayout.setObjectName(u"brandLayout")
        self.brandMark = QLabel(self.sidebar)
        self.brandMark.setObjectName(u"brandMark")
        self.brandMark.setMinimumWidth(30)
        self.brandMark.setMaximumWidth(30)
        self.brandMark.setMinimumHeight(32)
        self.brandMark.setMaximumHeight(32)

        self.brandLayout.addWidget(self.brandMark)

        self.brandName = QLabel(self.sidebar)
        self.brandName.setObjectName(u"brandName")

        self.brandLayout.addWidget(self.brandName)


        self.sidebarLayout.addLayout(self.brandLayout)

        self.brandSub = QLabel(self.sidebar)
        self.brandSub.setObjectName(u"brandSub")

        self.sidebarLayout.addWidget(self.brandSub)

        self.navCaption = QLabel(self.sidebar)
        self.navCaption.setObjectName(u"navCaption")

        self.sidebarLayout.addWidget(self.navCaption)

        self.btnOverview = QPushButton(self.sidebar)
        self.btnOverview.setObjectName(u"btnOverview")

        self.sidebarLayout.addWidget(self.btnOverview)

        self.btnCurves = QPushButton(self.sidebar)
        self.btnCurves.setObjectName(u"btnCurves")

        self.sidebarLayout.addWidget(self.btnCurves)

        self.btnHardware = QPushButton(self.sidebar)
        self.btnHardware.setObjectName(u"btnHardware")

        self.sidebarLayout.addWidget(self.btnHardware)

        self.btnSettings = QPushButton(self.sidebar)
        self.btnSettings.setObjectName(u"btnSettings")

        self.sidebarLayout.addWidget(self.btnSettings)

        self.btnLogs = QPushButton(self.sidebar)
        self.btnLogs.setObjectName(u"btnLogs")

        self.sidebarLayout.addWidget(self.btnLogs)

        self.sidebarStretch = QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.sidebarLayout.addItem(self.sidebarStretch)

        self.sidebarFooter = QLabel(self.sidebar)
        self.sidebarFooter.setObjectName(u"sidebarFooter")

        self.sidebarLayout.addWidget(self.sidebarFooter)


        self.shellLayout.addWidget(self.sidebar)

        self.mainContent = QWidget(self.centralwidget)
        self.mainContent.setObjectName(u"mainContent")
        self.rootLayout = QVBoxLayout(self.mainContent)
        self.rootLayout.setSpacing(24)
        self.rootLayout.setObjectName(u"rootLayout")
        self.rootLayout.setContentsMargins(30, 30, 30, 30)
        self.headerLayout = QHBoxLayout()
        self.headerLayout.setSpacing(14)
        self.headerLayout.setObjectName(u"headerLayout")
        self.titles = QVBoxLayout()
        self.titles.setSpacing(5)
        self.titles.setObjectName(u"titles")
        self.eyebrow = QLabel(self.mainContent)
        self.eyebrow.setObjectName(u"eyebrow")

        self.titles.addWidget(self.eyebrow)

        self.titleLabel = QLabel(self.mainContent)
        self.titleLabel.setObjectName(u"titleLabel")

        self.titles.addWidget(self.titleLabel)

        self.subtitleLabel = QLabel(self.mainContent)
        self.subtitleLabel.setObjectName(u"subtitleLabel")

        self.titles.addWidget(self.subtitleLabel)


        self.headerLayout.addLayout(self.titles)

        self.headerStretch = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.headerLayout.addItem(self.headerStretch)

        self.connectionBadge = QLabel(self.mainContent)
        self.connectionBadge.setObjectName(u"connectionBadge")

        self.headerLayout.addWidget(self.connectionBadge)

        self.btnQuickConnect = QPushButton(self.mainContent)
        self.btnQuickConnect.setObjectName(u"btnQuickConnect")

        self.headerLayout.addWidget(self.btnQuickConnect)


        self.rootLayout.addLayout(self.headerLayout)

        self.pages = QStackedWidget(self.mainContent)
        self.pages.setObjectName(u"pages")
        self.dashboardPage = QWidget()
        self.dashboardPage.setObjectName(u"dashboardPage")
        self.dataLayout = QVBoxLayout(self.dashboardPage)
        self.dataLayout.setSpacing(18)
        self.dataLayout.setObjectName(u"dataLayout")
        self.dataLayout.setContentsMargins(0, 0, 0, 0)
        self.selectRow = QHBoxLayout()
        self.selectRow.setSpacing(10)
        self.selectRow.setObjectName(u"selectRow")
        self.selectedCaption = QLabel(self.dashboardPage)
        self.selectedCaption.setObjectName(u"selectedCaption")

        self.selectRow.addWidget(self.selectedCaption)

        self.cmbSensor = QLabel(self.dashboardPage)
        self.cmbSensor.setObjectName(u"cmbSensor")

        self.selectRow.addWidget(self.cmbSensor)

        self.selectStretch = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.selectRow.addItem(self.selectStretch)

        self.lastReceivedLabel = QLabel(self.dashboardPage)
        self.lastReceivedLabel.setObjectName(u"lastReceivedLabel")

        self.selectRow.addWidget(self.lastReceivedLabel)


        self.dataLayout.addLayout(self.selectRow)

        self.cardsLayout = QHBoxLayout()
        self.cardsLayout.setSpacing(18)
        self.cardsLayout.setObjectName(u"cardsLayout")
        self.tempCard = QFrame(self.dashboardPage)
        self.tempCard.setObjectName(u"tempCard")
        self.tempCard.setMinimumHeight(180)
        self.tempCardLayout = QVBoxLayout(self.tempCard)
        self.tempCardLayout.setSpacing(12)
        self.tempCardLayout.setObjectName(u"tempCardLayout")
        self.tempCardLayout.setContentsMargins(24, 24, 24, 24)
        self.tempCaption = QLabel(self.tempCard)
        self.tempCaption.setObjectName(u"tempCaption")

        self.tempCardLayout.addWidget(self.tempCaption)

        self.tempValueRow = QHBoxLayout()
        self.tempValueRow.setSpacing(8)
        self.tempValueRow.setObjectName(u"tempValueRow")
        self.tempValue = QLabel(self.tempCard)
        self.tempValue.setObjectName(u"tempValue")

        self.tempValueRow.addWidget(self.tempValue)

        self.tempUnit = QLabel(self.tempCard)
        self.tempUnit.setObjectName(u"tempUnit")

        self.tempValueRow.addWidget(self.tempUnit)

        self.tempValueStretch = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.tempValueRow.addItem(self.tempValueStretch)


        self.tempCardLayout.addLayout(self.tempValueRow)

        self.tempFootnote = QLabel(self.tempCard)
        self.tempFootnote.setObjectName(u"tempFootnote")

        self.tempCardLayout.addWidget(self.tempFootnote)


        self.cardsLayout.addWidget(self.tempCard)

        self.humidityCard = QFrame(self.dashboardPage)
        self.humidityCard.setObjectName(u"humidityCard")
        self.humidityCard.setMinimumHeight(180)
        self.humidityCardLayout = QVBoxLayout(self.humidityCard)
        self.humidityCardLayout.setSpacing(12)
        self.humidityCardLayout.setObjectName(u"humidityCardLayout")
        self.humidityCardLayout.setContentsMargins(24, 24, 24, 24)
        self.humidityCaption = QLabel(self.humidityCard)
        self.humidityCaption.setObjectName(u"humidityCaption")

        self.humidityCardLayout.addWidget(self.humidityCaption)

        self.humidityValueRow = QHBoxLayout()
        self.humidityValueRow.setSpacing(8)
        self.humidityValueRow.setObjectName(u"humidityValueRow")
        self.humidityValue = QLabel(self.humidityCard)
        self.humidityValue.setObjectName(u"humidityValue")

        self.humidityValueRow.addWidget(self.humidityValue)

        self.humidityUnit = QLabel(self.humidityCard)
        self.humidityUnit.setObjectName(u"humidityUnit")

        self.humidityValueRow.addWidget(self.humidityUnit)

        self.humidityValueStretch = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.humidityValueRow.addItem(self.humidityValueStretch)


        self.humidityCardLayout.addLayout(self.humidityValueRow)

        self.humidityFootnote = QLabel(self.humidityCard)
        self.humidityFootnote.setObjectName(u"humidityFootnote")

        self.humidityCardLayout.addWidget(self.humidityFootnote)


        self.cardsLayout.addWidget(self.humidityCard)


        self.dataLayout.addLayout(self.cardsLayout)

        self.trendPanel = QFrame(self.dashboardPage)
        self.trendPanel.setObjectName(u"trendPanel")
        self.trendPanelLayout = QVBoxLayout(self.trendPanel)
        self.trendPanelLayout.setSpacing(12)
        self.trendPanelLayout.setObjectName(u"trendPanelLayout")
        self.trendPanelLayout.setContentsMargins(22, 22, 22, 22)
        self.trendHeader = QHBoxLayout()
        self.trendHeader.setSpacing(12)
        self.trendHeader.setObjectName(u"trendHeader")
        self.trendTitle = QLabel(self.trendPanel)
        self.trendTitle.setObjectName(u"trendTitle")

        self.trendHeader.addWidget(self.trendTitle)

        self.trendHeaderStretch = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.trendHeader.addItem(self.trendHeaderStretch)

        self.archiveCountLabel = QLabel(self.trendPanel)
        self.archiveCountLabel.setObjectName(u"archiveCountLabel")

        self.trendHeader.addWidget(self.archiveCountLabel)


        self.trendPanelLayout.addLayout(self.trendHeader)

        self.chartContainer = QWidget(self.trendPanel)
        self.chartContainer.setObjectName(u"chartContainer")
        self.chartContainer.setMinimumHeight(146)
        self.chartLayout = QVBoxLayout(self.chartContainer)
        self.chartLayout.setSpacing(0)
        self.chartLayout.setObjectName(u"chartLayout")
        self.chartLayout.setContentsMargins(0, 0, 0, 0)

        self.trendPanelLayout.addWidget(self.chartContainer)

        self.trendHint = QLabel(self.trendPanel)
        self.trendHint.setObjectName(u"trendHint")

        self.trendPanelLayout.addWidget(self.trendHint)


        self.dataLayout.addWidget(self.trendPanel)

        self.acquisitionPanel = QFrame(self.dashboardPage)
        self.acquisitionPanel.setObjectName(u"acquisitionPanel")
        self.acquisitionLayout = QHBoxLayout(self.acquisitionPanel)
        self.acquisitionLayout.setSpacing(10)
        self.acquisitionLayout.setObjectName(u"acquisitionLayout")
        self.acquisitionLayout.setContentsMargins(16, 16, 16, 16)
        self.acquisitionTitles = QVBoxLayout()
        self.acquisitionTitles.setSpacing(4)
        self.acquisitionTitles.setObjectName(u"acquisitionTitles")
        self.acquisitionTitle = QLabel(self.acquisitionPanel)
        self.acquisitionTitle.setObjectName(u"acquisitionTitle")

        self.acquisitionTitles.addWidget(self.acquisitionTitle)

        self.acquisitionHint = QLabel(self.acquisitionPanel)
        self.acquisitionHint.setObjectName(u"acquisitionHint")

        self.acquisitionTitles.addWidget(self.acquisitionHint)


        self.acquisitionLayout.addLayout(self.acquisitionTitles)

        self.acquisitionStretch = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.acquisitionLayout.addItem(self.acquisitionStretch)

        self.btnStopMeasure = QPushButton(self.acquisitionPanel)
        self.btnStopMeasure.setObjectName(u"btnStopMeasure")

        self.acquisitionLayout.addWidget(self.btnStopMeasure)

        self.btnStartMeasure = QPushButton(self.acquisitionPanel)
        self.btnStartMeasure.setObjectName(u"btnStartMeasure")

        self.acquisitionLayout.addWidget(self.btnStartMeasure)


        self.dataLayout.addWidget(self.acquisitionPanel)

        self.metaLayout = QHBoxLayout()
        self.metaLayout.setSpacing(12)
        self.metaLayout.setObjectName(u"metaLayout")
        self.deviceDateLabel = QLabel(self.dashboardPage)
        self.deviceDateLabel.setObjectName(u"deviceDateLabel")

        self.metaLayout.addWidget(self.deviceDateLabel)

        self.metaStretch = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.metaLayout.addItem(self.metaStretch)

        self.versionLabel = QLabel(self.dashboardPage)
        self.versionLabel.setObjectName(u"versionLabel")

        self.metaLayout.addWidget(self.versionLabel)

        self.databaseLabel = QLabel(self.dashboardPage)
        self.databaseLabel.setObjectName(u"databaseLabel")

        self.metaLayout.addWidget(self.databaseLabel)


        self.dataLayout.addLayout(self.metaLayout)

        self.pages.addWidget(self.dashboardPage)
        self.hardwarePage = QWidget()
        self.hardwarePage.setObjectName(u"hardwarePage")
        self.hardwareLayout = QVBoxLayout(self.hardwarePage)
        self.hardwareLayout.setSpacing(18)
        self.hardwareLayout.setObjectName(u"hardwareLayout")
        self.hardwareLayout.setContentsMargins(0, 0, 0, 0)
        self.commandsGroup = QFrame(self.hardwarePage)
        self.commandsGroup.setObjectName(u"commandsGroup")
        self.commandsLayout = QVBoxLayout(self.commandsGroup)
        self.commandsLayout.setSpacing(18)
        self.commandsLayout.setObjectName(u"commandsLayout")
        self.commandsLayout.setContentsMargins(22, 22, 22, 22)
        self.commandTargetLabel = QLabel(self.commandsGroup)
        self.commandTargetLabel.setObjectName(u"commandTargetLabel")

        self.commandsLayout.addWidget(self.commandTargetLabel)

        self.syncRow = QHBoxLayout()
        self.syncRow.setSpacing(18)
        self.syncRow.setObjectName(u"syncRow")
        self.syncTitles = QVBoxLayout()
        self.syncTitles.setSpacing(5)
        self.syncTitles.setObjectName(u"syncTitles")
        self.syncTitle = QLabel(self.commandsGroup)
        self.syncTitle.setObjectName(u"syncTitle")

        self.syncTitles.addWidget(self.syncTitle)

        self.syncHint = QLabel(self.commandsGroup)
        self.syncHint.setObjectName(u"syncHint")

        self.syncTitles.addWidget(self.syncHint)


        self.syncRow.addLayout(self.syncTitles)

        self.syncStretch = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.syncRow.addItem(self.syncStretch)

        self.btnSynchroDateTime = QPushButton(self.commandsGroup)
        self.btnSynchroDateTime.setObjectName(u"btnSynchroDateTime")

        self.syncRow.addWidget(self.btnSynchroDateTime)


        self.commandsLayout.addLayout(self.syncRow)

        self.ledPanel = QFrame(self.commandsGroup)
        self.ledPanel.setObjectName(u"ledPanel")
        self.ledLayout = QVBoxLayout(self.ledPanel)
        self.ledLayout.setSpacing(14)
        self.ledLayout.setObjectName(u"ledLayout")
        self.ledLayout.setContentsMargins(18, 18, 18, 18)
        self.ledTitle = QLabel(self.ledPanel)
        self.ledTitle.setObjectName(u"ledTitle")

        self.ledLayout.addWidget(self.ledTitle)

        self.ledPresets = QHBoxLayout()
        self.ledPresets.setSpacing(12)
        self.ledPresets.setObjectName(u"ledPresets")
        self.btnSlowBlink = QPushButton(self.ledPanel)
        self.btnSlowBlink.setObjectName(u"btnSlowBlink")

        self.ledPresets.addWidget(self.btnSlowBlink)

        self.btnFastBlink = QPushButton(self.ledPanel)
        self.btnFastBlink.setObjectName(u"btnFastBlink")

        self.ledPresets.addWidget(self.btnFastBlink)

        self.ledStretch = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.ledPresets.addItem(self.ledStretch)


        self.ledLayout.addLayout(self.ledPresets)

        self.customBlinkRow = QHBoxLayout()
        self.customBlinkRow.setSpacing(12)
        self.customBlinkRow.setObjectName(u"customBlinkRow")
        self.blinkCaption = QLabel(self.ledPanel)
        self.blinkCaption.setObjectName(u"blinkCaption")

        self.customBlinkRow.addWidget(self.blinkCaption)

        self.lneBlink = QLineEdit(self.ledPanel)
        self.lneBlink.setObjectName(u"lneBlink")

        self.customBlinkRow.addWidget(self.lneBlink)

        self.btnBlink = QPushButton(self.ledPanel)
        self.btnBlink.setObjectName(u"btnBlink")

        self.customBlinkRow.addWidget(self.btnBlink)


        self.ledLayout.addLayout(self.customBlinkRow)


        self.commandsLayout.addWidget(self.ledPanel)

        self.barPanel = QFrame(self.commandsGroup)
        self.barPanel.setObjectName(u"barPanel")
        self.barLayout = QVBoxLayout(self.barPanel)
        self.barLayout.setSpacing(14)
        self.barLayout.setObjectName(u"barLayout")
        self.barLayout.setContentsMargins(18, 18, 18, 18)
        self.barTitle = QLabel(self.barPanel)
        self.barTitle.setObjectName(u"barTitle")

        self.barLayout.addWidget(self.barTitle)

        self.bargraphRow = QHBoxLayout()
        self.bargraphRow.setSpacing(12)
        self.bargraphRow.setObjectName(u"bargraphRow")
        self.bargraphCaption = QLabel(self.barPanel)
        self.bargraphCaption.setObjectName(u"bargraphCaption")

        self.bargraphRow.addWidget(self.bargraphCaption)

        self.lneBargraph = QLineEdit(self.barPanel)
        self.lneBargraph.setObjectName(u"lneBargraph")

        self.bargraphRow.addWidget(self.lneBargraph)

        self.btnBargraph = QPushButton(self.barPanel)
        self.btnBargraph.setObjectName(u"btnBargraph")

        self.bargraphRow.addWidget(self.btnBargraph)


        self.barLayout.addLayout(self.bargraphRow)

        self.bargraphPreview = QLabel(self.barPanel)
        self.bargraphPreview.setObjectName(u"bargraphPreview")

        self.barLayout.addWidget(self.bargraphPreview)


        self.commandsLayout.addWidget(self.barPanel)

        self.commandHint = QLabel(self.commandsGroup)
        self.commandHint.setObjectName(u"commandHint")
        self.commandHint.setWordWrap(True)

        self.commandsLayout.addWidget(self.commandHint)


        self.hardwareLayout.addWidget(self.commandsGroup)

        self.hardwareStretch = QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.hardwareLayout.addItem(self.hardwareStretch)

        self.pages.addWidget(self.hardwarePage)
        self.settingsPage = QWidget()
        self.settingsPage.setObjectName(u"settingsPage")
        self.settingsLayout = QVBoxLayout(self.settingsPage)
        self.settingsLayout.setSpacing(18)
        self.settingsLayout.setObjectName(u"settingsLayout")
        self.settingsLayout.setContentsMargins(0, 0, 0, 0)
        self.connectionGroup = QFrame(self.settingsPage)
        self.connectionGroup.setObjectName(u"connectionGroup")
        self.connectionLayout = QVBoxLayout(self.connectionGroup)
        self.connectionLayout.setSpacing(14)
        self.connectionLayout.setObjectName(u"connectionLayout")
        self.connectionLayout.setContentsMargins(22, 22, 22, 22)
        self.connectionTitle = QLabel(self.connectionGroup)
        self.connectionTitle.setObjectName(u"connectionTitle")

        self.connectionLayout.addWidget(self.connectionTitle)

        self.profileCombo = QComboBox(self.connectionGroup)
        self.profileCombo.addItem("")
        self.profileCombo.addItem("")
        self.profileCombo.addItem("")
        self.profileCombo.setObjectName(u"profileCombo")

        self.connectionLayout.addWidget(self.profileCombo)

        self.addressFields = QHBoxLayout()
        self.addressFields.setSpacing(18)
        self.addressFields.setObjectName(u"addressFields")
        self.lneHostField = QVBoxLayout()
        self.lneHostField.setSpacing(7)
        self.lneHostField.setObjectName(u"lneHostField")
        self.lneHostCaption = QLabel(self.connectionGroup)
        self.lneHostCaption.setObjectName(u"lneHostCaption")

        self.lneHostField.addWidget(self.lneHostCaption)

        self.lneHost = QLineEdit(self.connectionGroup)
        self.lneHost.setObjectName(u"lneHost")

        self.lneHostField.addWidget(self.lneHost)


        self.addressFields.addLayout(self.lneHostField)

        self.spnPortField = QVBoxLayout()
        self.spnPortField.setSpacing(7)
        self.spnPortField.setObjectName(u"spnPortField")
        self.spnPortCaption = QLabel(self.connectionGroup)
        self.spnPortCaption.setObjectName(u"spnPortCaption")

        self.spnPortField.addWidget(self.spnPortCaption)

        self.spnPort = QSpinBox(self.connectionGroup)
        self.spnPort.setObjectName(u"spnPort")
        self.spnPort.setMinimum(1)
        self.spnPort.setMaximum(65535)
        self.spnPort.setValue(1883)

        self.spnPortField.addWidget(self.spnPort)


        self.addressFields.addLayout(self.spnPortField)


        self.connectionLayout.addLayout(self.addressFields)

        self.credentialsFields = QHBoxLayout()
        self.credentialsFields.setSpacing(18)
        self.credentialsFields.setObjectName(u"credentialsFields")
        self.lneUsernameField = QVBoxLayout()
        self.lneUsernameField.setSpacing(7)
        self.lneUsernameField.setObjectName(u"lneUsernameField")
        self.lneUsernameCaption = QLabel(self.connectionGroup)
        self.lneUsernameCaption.setObjectName(u"lneUsernameCaption")

        self.lneUsernameField.addWidget(self.lneUsernameCaption)

        self.lneUsername = QLineEdit(self.connectionGroup)
        self.lneUsername.setObjectName(u"lneUsername")

        self.lneUsernameField.addWidget(self.lneUsername)


        self.credentialsFields.addLayout(self.lneUsernameField)

        self.lnePasswordField = QVBoxLayout()
        self.lnePasswordField.setSpacing(7)
        self.lnePasswordField.setObjectName(u"lnePasswordField")
        self.lnePasswordCaption = QLabel(self.connectionGroup)
        self.lnePasswordCaption.setObjectName(u"lnePasswordCaption")

        self.lnePasswordField.addWidget(self.lnePasswordCaption)

        self.lnePassword = QLineEdit(self.connectionGroup)
        self.lnePassword.setObjectName(u"lnePassword")
        self.lnePassword.setEchoMode(QLineEdit.Password)

        self.lnePasswordField.addWidget(self.lnePassword)


        self.credentialsFields.addLayout(self.lnePasswordField)


        self.connectionLayout.addLayout(self.credentialsFields)

        self.topicFields = QHBoxLayout()
        self.topicFields.setSpacing(18)
        self.topicFields.setObjectName(u"topicFields")
        self.spnSensorField = QVBoxLayout()
        self.spnSensorField.setSpacing(7)
        self.spnSensorField.setObjectName(u"spnSensorField")
        self.spnSensorCaption = QLabel(self.connectionGroup)
        self.spnSensorCaption.setObjectName(u"spnSensorCaption")

        self.spnSensorField.addWidget(self.spnSensorCaption)

        self.spnSensor = QSpinBox(self.connectionGroup)
        self.spnSensor.setObjectName(u"spnSensor")
        self.spnSensor.setMinimum(1)
        self.spnSensor.setMaximum(999999999)
        self.spnSensor.setValue(44666)

        self.spnSensorField.addWidget(self.spnSensor)


        self.topicFields.addLayout(self.spnSensorField)

        self.lnePrefixField = QVBoxLayout()
        self.lnePrefixField.setSpacing(7)
        self.lnePrefixField.setObjectName(u"lnePrefixField")
        self.lnePrefixCaption = QLabel(self.connectionGroup)
        self.lnePrefixCaption.setObjectName(u"lnePrefixCaption")

        self.lnePrefixField.addWidget(self.lnePrefixCaption)

        self.lnePrefix = QLineEdit(self.connectionGroup)
        self.lnePrefix.setObjectName(u"lnePrefix")

        self.lnePrefixField.addWidget(self.lnePrefix)


        self.topicFields.addLayout(self.lnePrefixField)


        self.connectionLayout.addLayout(self.topicFields)

        self.caseCombo = QComboBox(self.connectionGroup)
        self.caseCombo.addItem("")
        self.caseCombo.addItem("")
        self.caseCombo.setObjectName(u"caseCombo")

        self.connectionLayout.addWidget(self.caseCombo)

        self.topicHint = QLabel(self.connectionGroup)
        self.topicHint.setObjectName(u"topicHint")
        self.topicHint.setWordWrap(True)

        self.connectionLayout.addWidget(self.topicHint)

        self.connectionButtons = QHBoxLayout()
        self.connectionButtons.setSpacing(10)
        self.connectionButtons.setObjectName(u"connectionButtons")
        self.btnConnect = QPushButton(self.connectionGroup)
        self.btnConnect.setObjectName(u"btnConnect")

        self.connectionButtons.addWidget(self.btnConnect)

        self.btnDisconnect = QPushButton(self.connectionGroup)
        self.btnDisconnect.setObjectName(u"btnDisconnect")

        self.connectionButtons.addWidget(self.btnDisconnect)

        self.connectionStretch = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.connectionButtons.addItem(self.connectionStretch)


        self.connectionLayout.addLayout(self.connectionButtons)


        self.settingsLayout.addWidget(self.connectionGroup)

        self.demoLayout = QHBoxLayout()
        self.demoLayout.setSpacing(14)
        self.demoLayout.setObjectName(u"demoLayout")
        self.demoHint = QLabel(self.settingsPage)
        self.demoHint.setObjectName(u"demoHint")

        self.demoLayout.addWidget(self.demoHint)

        self.demoStretch = QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.demoLayout.addItem(self.demoStretch)

        self.btnDemo = QPushButton(self.settingsPage)
        self.btnDemo.setObjectName(u"btnDemo")

        self.demoLayout.addWidget(self.btnDemo)


        self.settingsLayout.addLayout(self.demoLayout)

        self.settingsStretch = QSpacerItem(10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.settingsLayout.addItem(self.settingsStretch)

        self.pages.addWidget(self.settingsPage)
        self.logsPage = QWidget()
        self.logsPage.setObjectName(u"logsPage")
        self.logsLayout = QVBoxLayout(self.logsPage)
        self.logsLayout.setSpacing(12)
        self.logsLayout.setObjectName(u"logsLayout")
        self.logsLayout.setContentsMargins(0, 0, 0, 0)
        self.logCaption = QLabel(self.logsPage)
        self.logCaption.setObjectName(u"logCaption")

        self.logsLayout.addWidget(self.logCaption)

        self.logView = QPlainTextEdit(self.logsPage)
        self.logView.setObjectName(u"logView")
        self.logView.setReadOnly(True)

        self.logsLayout.addWidget(self.logView)

        self.pages.addWidget(self.logsPage)

        self.rootLayout.addWidget(self.pages)


        self.shellLayout.addWidget(self.mainContent)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"TempHumiX \u2014 Supervision IoT", None))
        self.brandMark.setText(QCoreApplication.translate("MainWindow", u"T", None))
        self.brandName.setText(QCoreApplication.translate("MainWindow", u"TempHumiX", None))
        self.brandSub.setText(QCoreApplication.translate("MainWindow", u"SENSOR WORKSPACE", None))
        self.navCaption.setText(QCoreApplication.translate("MainWindow", u"ESPACE DE TRAVAIL", None))
        self.btnOverview.setText(QCoreApplication.translate("MainWindow", u"Vue d\u2019ensemble", None))
        self.btnCurves.setText(QCoreApplication.translate("MainWindow", u"Historique", None))
        self.btnHardware.setText(QCoreApplication.translate("MainWindow", u"\u00c9quipement", None))
        self.btnSettings.setText(QCoreApplication.translate("MainWindow", u"Connexion", None))
        self.btnLogs.setText(QCoreApplication.translate("MainWindow", u"Journal", None))
        self.sidebarFooter.setText(QCoreApplication.translate("MainWindow", u"IMT NORD EUROPE\n"
"Projet Internet des objets", None))
        self.eyebrow.setText(QCoreApplication.translate("MainWindow", u"TEMP / HUMIDIT\u00c9", None))
        self.titleLabel.setText(QCoreApplication.translate("MainWindow", u"Vue d\u2019ensemble", None))
        self.subtitleLabel.setText(QCoreApplication.translate("MainWindow", u"Votre environnement, en un regard.", None))
        self.connectionBadge.setText(QCoreApplication.translate("MainWindow", u"HORS LIGNE", None))
        self.btnQuickConnect.setText(QCoreApplication.translate("MainWindow", u"Connecter", None))
        self.selectedCaption.setText(QCoreApplication.translate("MainWindow", u"CAPTEUR", None))
        self.cmbSensor.setText(QCoreApplication.translate("MainWindow", u"44666", None))
        self.lastReceivedLabel.setText(QCoreApplication.translate("MainWindow", u"En attente de la premi\u00e8re mesure", None))
        self.tempCaption.setText(QCoreApplication.translate("MainWindow", u"Temp\u00e9rature", None))
        self.tempValue.setText(QCoreApplication.translate("MainWindow", u"\u2014", None))
        self.tempUnit.setText(QCoreApplication.translate("MainWindow", u"\u00b0C", None))
        self.tempFootnote.setText(QCoreApplication.translate("MainWindow", u"MESURE DU CAPTEUR", None))
        self.humidityCaption.setText(QCoreApplication.translate("MainWindow", u"Humidit\u00e9 relative", None))
        self.humidityValue.setText(QCoreApplication.translate("MainWindow", u"\u2014", None))
        self.humidityUnit.setText(QCoreApplication.translate("MainWindow", u"%", None))
        self.humidityFootnote.setText(QCoreApplication.translate("MainWindow", u"MESURE DU CAPTEUR", None))
        self.trendTitle.setText(QCoreApplication.translate("MainWindow", u"\u00c9volution r\u00e9cente", None))
        self.archiveCountLabel.setText(QCoreApplication.translate("MainWindow", u"0 mesure archiv\u00e9e", None))
        self.trendHint.setText(QCoreApplication.translate("MainWindow", u"30 derni\u00e8res mesures \u00b7 temps du capteur", None))
        self.acquisitionTitle.setText(QCoreApplication.translate("MainWindow", u"Acquisition des mesures", None))
        self.acquisitionHint.setText(QCoreApplication.translate("MainWindow", u"Les nouvelles valeurs sont archiv\u00e9es automatiquement.", None))
        self.btnStopMeasure.setText(QCoreApplication.translate("MainWindow", u"Pause", None))
        self.btnStartMeasure.setText(QCoreApplication.translate("MainWindow", u"D\u00e9marrer", None))
        self.deviceDateLabel.setText(QCoreApplication.translate("MainWindow", u"Date du capteur : \u2014", None))
        self.versionLabel.setText(QCoreApplication.translate("MainWindow", u"Version : \u2014", None))
        self.databaseLabel.setText(QCoreApplication.translate("MainWindow", u"Base : IOT.db", None))
        self.commandTargetLabel.setText(QCoreApplication.translate("MainWindow", u"Capteur 44666", None))
        self.syncTitle.setText(QCoreApplication.translate("MainWindow", u"Date et version", None))
        self.syncHint.setText(QCoreApplication.translate("MainWindow", u"Synchroniser l\u2019horloge et demander la version du firmware.", None))
        self.btnSynchroDateTime.setText(QCoreApplication.translate("MainWindow", u"Synchroniser", None))
        self.ledTitle.setText(QCoreApplication.translate("MainWindow", u"T\u00e9moin lumineux", None))
        self.btnSlowBlink.setText(QCoreApplication.translate("MainWindow", u"Lent", None))
        self.btnFastBlink.setText(QCoreApplication.translate("MainWindow", u"Rapide", None))
        self.blinkCaption.setText(QCoreApplication.translate("MainWindow", u"P\u00e9riode personnalis\u00e9e (ms)", None))
        self.lneBlink.setText(QCoreApplication.translate("MainWindow", u"500", None))
        self.btnBlink.setText(QCoreApplication.translate("MainWindow", u"Appliquer", None))
        self.barTitle.setText(QCoreApplication.translate("MainWindow", u"Bargraphe \u00e0 10 LEDs", None))
        self.bargraphCaption.setText(QCoreApplication.translate("MainWindow", u"Valeur binaire \u00b7 0 \u00e0 1023", None))
        self.lneBargraph.setText(QCoreApplication.translate("MainWindow", u"10", None))
        self.btnBargraph.setText(QCoreApplication.translate("MainWindow", u"Envoyer", None))
        self.bargraphPreview.setText(QCoreApplication.translate("MainWindow", u"\u25cb  \u25cf  \u25cb  \u25cf  \u25cb  \u25cb  \u25cb  \u25cb  \u25cb  \u25cb", None))
        self.commandHint.setText(QCoreApplication.translate("MainWindow", u"Confirmer l\u2019ex\u00e9cution sur le montage. L\u2019aper\u00e7u repr\u00e9sente la valeur saisie.", None))
        self.connectionTitle.setText(QCoreApplication.translate("MainWindow", u"Param\u00e8tres du broker", None))
        self.profileCombo.setItemText(0, QCoreApplication.translate("MainWindow", u"Param\u00e8tres du cours", None))
        self.profileCombo.setItemText(1, QCoreApplication.translate("MainWindow", u"Arduino REN \u00b7 192.168.1.1", None))
        self.profileCombo.setItemText(2, QCoreApplication.translate("MainWindow", u"Personnalis\u00e9", None))

        self.lneHostCaption.setText(QCoreApplication.translate("MainWindow", u"Adresse IP / h\u00f4te", None))
        self.lneHost.setText(QCoreApplication.translate("MainWindow", u"10.120.2.3", None))
        self.spnPortCaption.setText(QCoreApplication.translate("MainWindow", u"Port", None))
        self.lneUsernameCaption.setText(QCoreApplication.translate("MainWindow", u"Utilisateur", None))
        self.lneUsername.setText(QCoreApplication.translate("MainWindow", u"mos_user", None))
        self.lnePasswordCaption.setText(QCoreApplication.translate("MainWindow", u"Mot de passe", None))
        self.lnePassword.setText(QCoreApplication.translate("MainWindow", u"mos_user", None))
        self.spnSensorCaption.setText(QCoreApplication.translate("MainWindow", u"Mon identifiant", None))
        self.lnePrefixCaption.setText(QCoreApplication.translate("MainWindow", u"Pr\u00e9fixe des topics", None))
        self.lnePrefix.setText(QCoreApplication.translate("MainWindow", u"/iot", None))
        self.caseCombo.setItemText(0, QCoreApplication.translate("MainWindow", u"Commandes : MAJUSCULES", None))
        self.caseCombo.setItemText(1, QCoreApplication.translate("MainWindow", u"Commandes : minuscules", None))

        self.topicHint.setText(QCoreApplication.translate("MainWindow", u"M\u00eame broker que l\u2019Arduino. La casse des topics de commande doit correspondre au firmware.", None))
        self.btnConnect.setText(QCoreApplication.translate("MainWindow", u"Connecter", None))
        self.btnDisconnect.setText(QCoreApplication.translate("MainWindow", u"D\u00e9connecter", None))
        self.demoHint.setText(QCoreApplication.translate("MainWindow", u"Sans mat\u00e9riel ? Utilisez la d\u00e9monstration locale.", None))
        self.btnDemo.setText(QCoreApplication.translate("MainWindow", u"Lancer la d\u00e9mo", None))
        self.logCaption.setText(QCoreApplication.translate("MainWindow", u"\u00c9V\u00c9NEMENTS MQTT ET APPLICATION", None))
    # retranslateUi

