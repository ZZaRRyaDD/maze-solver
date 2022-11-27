"""Модуль с диалоговым окном для сохранения лабиринта."""
from PyQt5 import QtCore, QtWidgets

from forms.maze_save_window import Ui_Dialog  # pylint: disable=import-error


class SaveWindow(QtWidgets.QDialog):
    """Класс окна ввода настроек лабиринта."""

    saveClicked = QtCore.pyqtSignal(str, str)

    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setFixedSize(195, 120)

    @QtCore.pyqtSlot()
    def on_ok_btn_clicked(self) -> None:
        """Слот при нажатии ОК."""
        extension = ""
        if self.ui.txt.isChecked():
            extension = "TXT"
        elif self.ui.png.isChecked():
            extension = "PNG"
        elif self.ui.jpg.isChecked():
            extension = "JPG"
        name_file = self.ui.name_file.text()
        if extension and name_file:
            self.saveClicked.emit(
                extension,
                name_file,
            )
            self.close()
        else:
            QtWidgets.QMessageBox.warning(
                self,
                "Внимание!",
                "Введены не все данные!",
            )
