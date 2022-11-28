"""Модуль с диалоговым окном для сохранения лабиринта."""
from forms import Ui_DialogSave
from PyQt5 import QtCore, QtWidgets


class SaveWindow(QtWidgets.QDialog):
    """Класс окна ввода настроек лабиринта."""

    saveClicked = QtCore.pyqtSignal(str, str)

    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_DialogSave()
        self.ui.setupUi(self)
        self.setFixedSize(195, 120)

    @QtCore.pyqtSlot()
    def on_ok_btn_clicked(self) -> None:
        """Слот при нажатии ОК."""
        extension = ""
        if self.ui.txt.isChecked():
            extension = "txt"
        elif self.ui.png.isChecked():
            extension = "png"
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
