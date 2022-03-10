"""Модуль с некоторыми переопределенными методами QLabel."""
from PyQt5 import QtWidgets, QtCore


class MyQLabel(QtWidgets.QLabel):
    """Кастомный qlabel для ослеживания координат."""

    getClicked = QtCore.pyqtSignal(tuple)

    def __init__(self, main_widget, *args):
        super(MyQLabel, self).__init__(*args)
        self.main = main_widget

    def mousePressEvent(self, event):
        """Обработка клика по картинке."""
        if self.pixmap():
            self.main.get_points(
                (
                    [
                        event.pos().x(),
                        event.pos().y(),
                    ],
                    [
                        self.size().width(),
                        self.size().height(),
                    ],
                )
            )
            