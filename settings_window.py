"""Модуль с диалоговым окном для ввода данных лабиринта."""
from PyQt5 import QtCore, QtWidgets

from forms.maze_settings_window import Ui_Dialog  # pylint: disable=import-error


class SettingWindow(QtWidgets.QDialog):
    """Класс окна ввода настроек лабиринта."""

    saveClicked = QtCore.pyqtSignal(int, int, str, str)

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setFixedSize(240, 225)

    @QtCore.pyqtSlot()
    def on_ok_btn_clicked(self) -> None:
        """Слот при нажатии ОК."""
        width = self.ui.width_maze.value()
        height = self.ui.height_maze.value()
        img_name = self.ui.image_name.text()
        extension = self.ui.select_extension.currentText()
        if all([width, height, img_name, extension]):
            self.saveClicked.emit(
                width,
                height,
                img_name,
                extension,
            )
            self.close()
        else:
            QtWidgets.QMessageBox.warning(
                self,
                "Внимание!",
                "Введены не все данные!",
            )
