from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtProperty, QPointF


class SolarObjectButton(QtWidgets.QPushButton):
    def __init__(self, parent):
        super().__init__(parent)

    # метод _set_pos немного смещает планету во время анимации
    def _set_pos(self, pos):
        self.move(pos.x() - self.width() / 2, pos.y() - self.height() / 2)

    pos = pyqtProperty(QPointF, fset=_set_pos)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1103, 895)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(-10, 780, 1121, 81))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(16, 0, 16, 0)
        self.horizontalLayout.setSpacing(28)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.reset_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.reset_button.setObjectName("reset_button")
        self.horizontalLayout.addWidget(self.reset_button)
        self.stop_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.stop_button.setObjectName("stop_button")
        self.horizontalLayout.addWidget(self.stop_button)
        self.down_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.down_button.setObjectName("down_button")
        self.horizontalLayout.addWidget(self.down_button)
        self.up_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.up_button.setObjectName("up_button")
        self.horizontalLayout.addWidget(self.up_button)
        self.earth = SolarObjectButton(self.centralwidget)
        self.earth.setGeometry(QtCore.QRect(677, 387, 26, 26))
        self.earth.setStyleSheet("border-radius: 13px; \n"
"background-color: qlineargradient(spread:reflect, x1:0.454, y1:0.512, x2:1, y2:1, stop:0.198864 rgba(0, 0, 206, 255), stop:0.670455 rgba(70, 140, 99, 255), stop:0.8125 rgba(255, 255, 255, 255));")
        self.earth.setText("")
        self.earth.setIconSize(QtCore.QSize(16, 16))
        self.earth.setObjectName("earth")
        self.mercury = SolarObjectButton(self.centralwidget)
        self.mercury.setGeometry(QtCore.QRect(612, 392, 16, 16))
        self.mercury.setStyleSheet("border-radius: 8px; \n"
"background-color: qlineargradient(spread:pad, x1:0.534091, y1:0.523, x2:1, y2:1, stop:0 rgba(187, 57, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
"")
        self.mercury.setText("")
        self.mercury.setObjectName("mercury")
        self.venerus = SolarObjectButton(self.centralwidget)
        self.venerus.setGeometry(QtCore.QRect(645, 390, 20, 20))
        self.venerus.setStyleSheet("border-radius: 10px; \n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 178, 102, 255), stop:0.55 rgba(235, 148, 61, 255), stop:0.98 rgba(0, 0, 0, 255), stop:1 rgba(0, 0, 0, 0));")
        self.venerus.setText("")
        self.venerus.setObjectName("venerus")
        self.mars = SolarObjectButton(self.centralwidget)
        self.mars.setGeometry(QtCore.QRect(715, 390, 20, 20))
        self.mars.setStyleSheet("border-radius: 10px; \n"
"background-color: qlineargradient(spread:pad, x1:0.699, y1:0.545455, x2:1, y2:0.642682, stop:0 rgba(255, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));")
        self.mars.setText("")
        self.mars.setIconSize(QtCore.QSize(16, 16))
        self.mars.setObjectName("mars")
        self.jupiter = SolarObjectButton(self.centralwidget)
        self.jupiter.setGeometry(QtCore.QRect(743, 383, 34, 34))
        self.jupiter.setStyleSheet("border-radius: 17px; \n"
"background-color: qlineargradient(spread:reflect, x1:0.972, y1:0.926, x2:1, y2:1, stop:0.295455 rgba(101, 83, 0, 255), stop:0.664773 rgba(157, 152, 140, 255), stop:0.886364 rgba(221, 167, 63, 255));")
        self.jupiter.setText("")
        self.jupiter.setIconSize(QtCore.QSize(16, 16))
        self.jupiter.setObjectName("jupiter")
        self.saturn = SolarObjectButton(self.centralwidget)
        self.saturn.setGeometry(QtCore.QRect(779, 384, 32, 32))
        self.saturn.setStyleSheet("border-radius: 16px; \n"
"background-color: qlineargradient(spread:pad, x1:0.284, y1:0.351955, x2:0.63, y2:0.9375, stop:0.232955 rgba(235, 142, 0, 255), stop:0.488636 rgba(138, 75, 2, 255), stop:0.664773 rgba(246, 102, 2, 255));")
        self.saturn.setText("")
        self.saturn.setIconSize(QtCore.QSize(16, 16))
        self.saturn.setObjectName("saturn")
        self.uran = SolarObjectButton(self.centralwidget)
        self.uran.setGeometry(QtCore.QRect(815, 385, 30, 30))
        self.uran.setStyleSheet("border-radius: 15px; \n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 174, 255, 255), stop:0.5625 rgba(0, 56, 205, 255), stop:1 rgba(0, 255, 255, 255));")
        self.uran.setText("")
        self.uran.setIconSize(QtCore.QSize(16, 16))
        self.uran.setObjectName("uran")
        self.neptun = SolarObjectButton(self.centralwidget)
        self.neptun.setGeometry(QtCore.QRect(851, 386, 28, 28))
        self.neptun.setStyleSheet("border-radius: 14px; \n"
"background-color: qlineargradient(spread:pad, x1:0.824, y1:0.449045, x2:1, y2:1, stop:0.159091 rgba(0, 32, 255, 255), stop:0.409091 rgba(0, 0, 255, 255), stop:0.863636 rgba(22, 92, 255, 255));")
        self.neptun.setText("")
        self.neptun.setIconSize(QtCore.QSize(16, 16))
        self.neptun.setObjectName("neptun")
        self.pluton = SolarObjectButton(self.centralwidget)
        self.pluton.setGeometry(QtCore.QRect(894, 394, 12, 12))
        self.pluton.setStyleSheet("border-radius: 6px; \n"
"background-color: qlineargradient(spread:pad, x1:0.864, y1:0.210727, x2:1, y2:1, stop:0 rgba(65, 65, 65, 255), stop:0.4375 rgba(117, 13, 13, 255), stop:1 rgba(126, 144, 126, 255));")
        self.pluton.setText("")
        self.pluton.setObjectName("pluton")
        self.sun = QtWidgets.QPushButton(self.centralwidget)
        self.sun.setGeometry(QtCore.QRect(511, 360, 80, 80))
        self.sun.setStyleSheet("border-radius: 40px; \n"
"background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 68, 0, 255), stop:1 rgba(255, 255, 0, 255));")
        self.sun.setText("")
        self.sun.setIconSize(QtCore.QSize(16, 16))
        self.sun.setObjectName("sun")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Модель Солнечной Системы"))
        self.reset_button.setText(_translate("MainWindow", "СБРОС"))
        self.stop_button.setText(_translate("MainWindow", "СТОП"))
        self.down_button.setText(_translate("MainWindow", "НАЗАД"))
        self.up_button.setText(_translate("MainWindow", "ВПЕРЁД"))
