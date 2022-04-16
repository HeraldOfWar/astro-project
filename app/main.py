import sys
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtGui import QPainterPath, QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow
from main_window import Ui_MainWindow


class ModelSolarSystem(QMainWindow, Ui_MainWindow):

    # загружаем все объекты в окне
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.solar_views = [self.sun, self.mercury, self.venerus, self.earth, self.mars,
                            self.jupiter, self.saturn, self.uran, self.neptun, self.pluton]
        self.start_positions = []
        for i in self.solar_views:
            self.start_positions.append((i.x(), i.y()))
        self.initButtons()
        self.initOrbits()
        self.initAnimations()
        self.repaint()

    # привязываем все кнопки к методам, элементам класса SolarObject, сохраняем начальные позиции
    # всех объектов Солнечной системы
    def initButtons(self):
        for view in self.solar_views:
            view.clicked.connect(self.show_info)
        self.up_button.clicked.connect(self.start)
        self.down_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)
        self.reset_button.clicked.connect(self.reset)

    # создаём орбиты для планет
    def initOrbits(self):
        self.orbits = []
        k, r = 0, 1
        for i in range(1, 10):
            orbit = QPainterPath()
            orbit.addEllipse(480 - k, 330 - k, int(r * 140), int(r * 140))
            k += 35
            r += 0.5
            self.orbits.append(orbit)

    # создаём анимации движения для каждой планеты
    def initAnimations(self):
        self.animations = []
        for i in range(9):
            anim = QPropertyAnimation(self.solar_views[i + 1], b'pos')
            anim.setDuration(10000 * (i + 1))
            values = [p / 100 for p in range(0, 101)]
            # устанавливаем в процентном соотношении точки, которые нужно пройти во время анимации
            for j in values:
                anim.setKeyValueAt(j, self.orbits[i].pointAtPercent(j))
            anim.setLoopCount(10000)
            self.animations.append(anim)

    # рисуем орбиты для планет
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        for p in self.orbits:
            qp.drawPath(p)
        qp.end()

    # начинаем анимацию
    def start(self):
        for a in self.animations:
            if self.sender().objectName() == 'down_button':
                a.setDirection(0)
            else:
                a.setDirection(1)
            a.start()

    # ставим анимацию на паузу
    def stop(self):
        for a in self.animations:
            a.pause()

    # останавливаем анимацию и возвращаем планеты на изначальные позиции
    def reset(self):
        for a in self.animations:
             a.stop()
        for i in range(1, len(self.solar_views)):
            self.solar_views[i].move(self.start_positions[i][0], self.start_positions[i][1])

    # открываем страницу в браузере с информацией об объекте Солнечной системы
    def show_info(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ModelSolarSystem()
    ex.show()
    sys.exit(app.exec())
