"""Модуль с диалоговым окном для ввода данных лабиринта."""
from forms import Ui_DialogSetting
from PyQt5 import QtCore, QtWidgets


class SettingWindow(QtWidgets.QDialog):
    """Класс окна ввода настроек лабиринта."""

    saveClicked = QtCore.pyqtSignal(int, int, str)

    def __init__(self):
        super().__init__()
        self.ui = Ui_DialogSetting()
        self.ui.setupUi(self)
        self.setFixedSize(210, 200)

    @QtCore.pyqtSlot()
    def on_ok_btn_clicked(self) -> None:
        """Слот при нажатии ОК."""
        width = self.ui.width_maze.value()
        height = self.ui.height_maze.value()
        img_name = self.ui.image_name.text()
        if all([width, height, img_name]):
            self.saveClicked.emit(
                width,
                height,
                img_name,
            )
            self.close()
        else:
            QtWidgets.QMessageBox.warning(
                self,
                "Внимание!",
                "Введены не все данные!",
            )
