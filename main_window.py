"""Модуль главного окна."""
from math import floor

from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets

from constants import Colors, Modes
from forms import Ui_MazeGenerator
from maze import Maze
from save_window import SaveWindow
from settings_window import SettingWindow


class MainWindow(QtWidgets.QMainWindow):
    """Класс главного окна."""

    def __init__(self):
        super().__init__()
        self.ui = Ui_MazeGenerator()
        self.ui.setupUi(self)
        self.ui.getPointsClicked.connect(self.get_points)
        self.__maze = None
        self.__clicked_x, self.__clicked_y = 0, 0
        self.__mode = Modes.MODE_NO_CHOICE
        self.ui.generate_maze.setToolTip("Генерация лабиринта")
        self.ui.save_maze.setToolTip("Сохранение лабиринта")
        self.ui.load_maze.setToolTip("Загрузка лабиринта")
        self.ui.set_coordinate.setToolTip("Выбор координат")
        self.ui.solve_maze.setToolTip("Решение лабиринта")
        self.ui.generate_gif.setToolTip("Генерация гифки")

    @QtCore.pyqtSlot()
    def on_generate_maze_clicked(self) -> None:
        """Слот при нажатии на кнопку генерации."""
        settings = SettingWindow()
        settings.saveClicked.connect(self.generate_maze)
        settings.show()
        settings.exec_()

    def generate_maze(
        self,
        width: int,
        height: int,
        img_name: str,
        extension: str,
    ) -> None:
        """Получение параметров и рисование."""
        try:
            self.ui.img.clear()
            self.__maze = Maze(width=width, height=height)
            self.__maze.save(img_name, extension)
            path = f"{img_name}.{extension}"
            self.__maze.path = path
            image = QtGui.QImage(path)
            pixmap = QtGui.QPixmap.fromImage(image)
            self.ui.img.setPixmap(
                pixmap.scaled(
                    self.ui.img.size().width(),
                    self.ui.img.size().height(),
                    QtCore.Qt.KeepAspectRatio,
                ),
            )
            self.ui.img.setScaledContents(True)
        except ValueError:
            QtWidgets.QMessageBox.warning(
                self,
                "Внимание!",
                "Введены не верные значения!",
            )

    @QtCore.pyqtSlot()
    def on_save_maze_clicked(self) -> None:
        """Слот при нажатии на кнопку сохранения."""
        save = SaveWindow()
        save.saveClicked.connect(self.save_maze)
        save.show()
        save.exec_()

    def save_maze(self, extenstion: str, name_file: str) -> None:
        """Сохранение файла."""
        if self.__maze:
            self.__maze.save(name_file, extenstion)
        else:
            QtWidgets.QMessageBox.warning(
                self,
                "Внимание!",
                "Лабиринт не сгенерирован!",
            )

    @QtCore.pyqtSlot()
    def on_load_maze_clicked(self) -> None:
        """Метод загрузки лабиринта."""
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Выберите файл с лабиринтом",
            "./",
            "Maze (*.png *.jpg, *.txt)",
        )
        try:
            self.__maze = Maze(path=file_path)
            name = file_path[file_path.rindex("/") + 1:file_path.index(".")]
            extension = "png" if file_path.endswith(".txt") else "txt"
            self.__maze.save(name, extension.upper())
            self.ui.img.clear()
            img = file_path if extension == "txt" else f"{name}.{extension}"
            self.__maze.path = img
            image_load = QtGui.QImage(img)
            pixmap_load = QtGui.QPixmap.fromImage(image_load)
            self.ui.img.setPixmap(
                pixmap_load.scaled(
                    self.ui.img.size().width(),
                    self.ui.img.size().height(),
                    QtCore.Qt.KeepAspectRatio,
                )
            )
            self.ui.img.setScaledContents(True)
        except ValueError:
            QtWidgets.QMessageBox.warning(
                self,
                "Внимание!",
                "Введены не верные значения!",
            )

    def get_points(self, position: list, size: list) -> None:
        """Слот для получения точек с label."""
        with Image.open(self.__maze.path) as image:
            width, height = image.size
            self.__clicked_x = floor(position[0]/(size[0]/width))
            self.__clicked_y = floor(position[1]/(size[1]/height))
            print(
                f"Отслеженная x: {self.__clicked_x}, "
                f"отслеженная y {self.__clicked_y}"
            )
            if self.__mode == Modes.MODE_CHOICE:
                pixels = image.load()
                if self.__clicked_x <= width and self.__clicked_y <= height:
                    point = pixels[self.__clicked_x, self.__clicked_y]
                    if point == Colors.BLACK_COLOR:
                        QtWidgets.QMessageBox.warning(
                            self,
                            "Внимание!",
                            "Выбранная точка является стеной.",
                        )
                    elif point == Colors.WHITE_COLOR:
                        if not self.__maze.start_point:
                            self.__maze.start_point = [
                                self.__clicked_x,
                                self.__clicked_y,
                            ]
                        elif not self.__maze.end_point:
                            self.__maze.end_point = [
                                self.__clicked_x,
                                self.__clicked_y,
                            ]
                            self.__mode = Modes.MODE_NO_CHOICE
                            QtWidgets.QMessageBox.information(
                                self,
                                "Выбранные точки!",
                                (
                                    f"Выбраны точки: {self.__maze.start_point}"
                                    f" и {self.__maze.end_point}. "
                                    "Для начала решения лабиринта "
                                    "нажмите сооветствующую кнопку."
                                ),
                            )
                else:
                    QtWidgets.QMessageBox.warning(
                        self,
                        "Внимание!",
                        "Точка по координате y не верна.",
                    )

    @QtCore.pyqtSlot()
    def on_set_coordinate_clicked(self) -> None:
        """Метод запуска выбора координат."""
        if self.__maze:
            if not self.__maze.list_way:
                if self.__mode == Modes.MODE_NO_CHOICE:
                    self.__clicked_x, self.__clicked_y = 0, 0
                    self.__maze.start_point = []
                    self.__maze.end_point = []
                    QtWidgets.QMessageBox.information(
                        self,
                        "Выбор точки",
                        (
                            "Сейчас включается режим выбора точки. "
                            "Кликните по двум точкам, "
                            "чтобы задать старт и конец "
                            "лабаринта соответственно"
                        ),
                    )
                    self.__mode = Modes.MODE_CHOICE
            else:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Внимание!",
                    "Загрузите нерешенный лабиринт или сгенерируйте новый.",
                )
        else:
            QtWidgets.QMessageBox.warning(
                self,
                "Внимание!",
                "Для выбора точек введите/загрузите лабиринт.",
            )

    @QtCore.pyqtSlot()
    def on_solve_maze_clicked(self) -> None:
        """Метод запуска решения лабиринта."""
        if self.__maze:
            self.__maze.solve_maze()
            new_path = (
                self.__maze.path[:self.__maze.path.index(".")] +
                "_solve" +
                self.__maze.path[self.__maze.path.index("."):]
            )
            self.ui.img.clear()
            self.__maze.create_image(new_path)
            image_load = QtGui.QImage(new_path)
            pixmap_load = QtGui.QPixmap.fromImage(image_load)
            self.ui.img.setPixmap(
                pixmap_load.scaled(
                    self.ui.img.size().width(),
                    self.ui.img.size().height(),
                    QtCore.Qt.KeepAspectRatio,
                ),
            )
            self.ui.img.setScaledContents(True)
        else:
            QtWidgets.QMessageBox.warning(
                self,
                "Внимание!",
                "Лабиринт не сгенерирован!",
            )

    @QtCore.pyqtSlot()
    def on_generate_gif_clicked(self) -> None:
        """Метож запуска генерации гифки."""
        if self.__maze:
            if not self.__maze.list_way:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Внимание!",
                    "Сначала решите лабиринт!",
                )
            else:
                gif_name = (
                    self.__maze.path[:self.__maze.path.index(".")] +
                    "_solve.gif"
                )
                gif_name_before = (
                    self.__maze.path[:self.__maze.path.index(".")] +
                    "_solve_for_gif.png"
                )
                self.__maze.save(
                    gif_name_before[:gif_name_before.index(".")],
                    "PNG",
                )
                self.__maze.create_gif(gif_name_before)
                self.__maze.gif[0].save(
                    gif_name,
                    save_all=True,
                    append_images=self.__maze.gif[:],
                    duration=100,
                    loop=0,
                )
                self.ui.img.clear()
                movie = QtGui.QMovie(gif_name)
                self.ui.img.setMovie(movie)
                movie.start()
        else:
            QtWidgets.QMessageBox.warning(
                self,
                "Внимание!",
                "Лабиринт не сгенерирован!",
            )
