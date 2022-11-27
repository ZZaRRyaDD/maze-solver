"""Модуль с лабиринтом."""
import os
import random
from typing import Optional

from PIL import Image

from constants import Colors
from stack import Stack

WAY = "1"
WALL = "0"


class Maze:  # pylint: disable=too-many-instance-attributes
    """Класс для генерации лабиринта."""

    def __init__(
        self,
        path: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> None:
        self.__list_maze = []
        self.__start_point = []
        self.__end_point = []
        self.__path = ""
        self.__gif = []
        self.__way_points = Stack()
        self.__list_way = []
        self.__use_points = Stack()
        if width and height:
            self.generate(width, height)
        elif path:
            self.from_other_format(path)
        else:
            raise ValueError("Введите либо размеры, либо путь к файлу")

    @property
    def start_point(self) -> list:
        """Геттер для пути до изображения."""
        return self.__start_point

    @start_point.setter
    def start_point(self, value) -> None:
        """Сеттер для пути до изображения."""
        self.__start_point = value

    @property
    def end_point(self) -> list:
        """Геттер для пути до изображения."""
        return self.__end_point

    @end_point.setter
    def end_point(self, value) -> None:
        """Сеттер для пути до изображения."""
        self.__end_point = value

    @property
    def way_points(self) -> Stack:
        """Стек с точками, соответствующие путю."""
        return self.__way_points

    @property
    def list_way(self) -> str:
        """Список с точками, соответствущие путю."""
        return self.__list_way

    @property
    def gif(self) -> list:
        """Геттер для гифки."""
        return self.__gif

    @property
    def path(self) -> str:
        """Геттер для пути до изображения."""
        return self.__path

    @path.setter
    def path(self, value) -> None:
        """Сеттер для пути до изображения."""
        self.__path = value

    @property
    def list_maze(self) -> list:
        """Возвращает лабиринт."""
        return self.__list_maze

    def from_other_format(self, path: str) -> None:
        """Функция для перевода из другого формата."""
        if path.endswith((".png", ".jpg")):
            with Image.open(path) as image:
                pixels = image.load()
                width, height = image.size
                for index1 in range(width):
                    row = []
                    for index2 in range(height):
                        if pixels[index1, index2] == Colors.WHITE_COLOR:
                            row.append(WAY)
                        elif pixels[index1, index2] == Colors.BLACK_COLOR:
                            row.append(WALL)
                        else:
                            raise ValueError(
                                "Вероятно вы загрузили уже решенный лабиринт",
                            )
                    self.__list_maze.append(row)
            self.__path = path
        elif path.endswith(".txt"):
            with open(path, "r", encoding="utf-8") as ptr:
                string = ptr.read()
                row = []
                for _, char in enumerate(string):
                    if char == WAY:
                        row.append(char)
                    elif char == WALL:
                        row.append(char)
                    elif char == "\n":
                        self.__list_maze.append(row)
                        row = []
                self.__list_maze.append(row)
        else:
            raise ValueError("Не верный формат файла")

    def generate_start_point(self) -> None:
        """Генерация начальной точки лабиринта."""
        point1 = self.__list_maze[1][1]
        point2 = self.__list_maze[1][2]
        if point1 != WALL:
            self.__start_point = [1, 1]
        elif point2 != WALL:
            self.__start_point = [1, 2]
        else:
            self.__start_point = [2, 1]

    def generate_end_point(self) -> None:
        """Генерация конечной точки лабиринта."""
        height = len(self.__list_maze)
        width = len(self.__list_maze[0])
        point1 = self.__list_maze[height - 2][width - 2]
        point2 = self.__list_maze[height - 3][width - 2]
        if point1 != WALL:
            self.__end_point = [height - 2, width - 2]
        elif point2 != WALL:
            self.__end_point = [height - 3, width - 2]
        else:
            self.__end_point = [height - 2, width - 3]

    def init_base_data(  # pylint: disable=no-self-use
        self,
        output_height: int,
        output_width: int,
        list_maze: list,
    ) -> None:
        """Инициализация лабиринта начальными значениями."""
        for i in range(output_height):
            row = []
            for j in range(output_width):
                if i % 2 == 1 and j % 2 == 1:
                    row.append(WAY)
                else:
                    first_cond = all(
                        [
                            i % 2 == 1,
                            j % 2 == 0,
                            j != 0,
                            j != output_width - 1,
                        ],
                    )
                    second_cond = all(
                        [
                            j % 2 == 1,
                            i % 2 == 0,
                            i != 0,
                            i != output_height - 1,
                        ],
                    )
                    row.append(
                        WAY if any([first_cond, second_cond]) else WALL
                    )
            list_maze.append(row)
        return list_maze

    def assign_set(  # pylint: disable=no-self-use
        self,
        width: int,
        counter: int,
        row_set: list,
    ) -> int:
        """Присвоение множества."""
        for j in range(width):
            if not row_set[j]:
                counter += 1
                row_set[j] = counter
        return counter

    def build_right_walls(  # pylint: disable=no-self-use
        self,
        width: int,
        i: int,
        row_set: list,
        list_maze: list,
    ) -> list:
        """Добавляем стены."""
        for j in range(width - 1):
            if random.randint(0, 1) or row_set[j] == row_set[j + 1]:
                list_maze[i * 2 + 1][j * 2 + 2] = WALL
            else:
                changing_set = row_set[j + 1]
                for index in range(width):
                    if row_set[index] == changing_set:
                        row_set[index] = row_set[j]
        return list_maze

    def build_bottom_walls(  # pylint: disable=no-self-use
        self,
        width: int,
        i: int,
        row_set: list,
        list_maze: list,
    ) -> list:
        """Построние стен снизу."""
        for j in range(width):
            count_current_set = 0
            for index in range(width):
                if row_set[j] == row_set[index]:
                    count_current_set += 1
            if random.randint(0, 1) and count_current_set != 1:
                list_maze[i * 2 + 2][j * 2 + 1] = WALL
        return list_maze

    def check_walls(  # pylint: disable=no-self-use
        self,
        height: int,
        width: int,
        i: int,
        row_set: list,
        list_maze: list,
    ) -> list:
        """Проверка расположения стен."""
        if i != height - 1:
            for j in range(width):
                count_hole = 0
                for index in range(width):
                    if (
                        row_set[index] == row_set[j] and
                        list_maze[i * 2 + 2][index * 2 + 1] == WAY
                    ):
                        count_hole += 1
                if not count_hole:
                    list_maze[i * 2 + 2][j * 2 + 1] = WAY
        if i != height - 1:
            for j in range(width):
                if list_maze[i * 2 + 2][j * 2 + 1] == WALL:
                    row_set[j] = 0
        return list_maze

    def generate(self, width: int, height: int) -> None:
        """Метод для генерации лабиринта."""
        output_height, output_width = height * 2 + 1, width * 2 + 1
        list_maze = []
        list_maze = self.init_base_data(output_height, output_width, list_maze)
        row_set = [0 for _ in range(width)]
        counter = 1

        for i in range(height):
            counter = self.assign_set(width, counter, row_set)
            list_maze = self.build_right_walls(width, i, row_set, list_maze)
            list_maze = self.build_bottom_walls(width, i, row_set, list_maze)
            list_maze = self.check_walls(height, width, i, row_set, list_maze)

        for j in range(width - 1):
            if row_set[j] != row_set[j + 1]:
                list_maze[output_height - 2][j * 2 + 2] = WAY

        self.__list_maze = list_maze

    def save(self, name: str, extension: str) -> None:
        """Переводит лабиринт в изображение."""
        name += f".{extension.lower()}"
        if extension in ("PNG", "JPG"):
            height, width = len(self.__list_maze), len(self.__list_maze[0])
            with Image.new("RGB", (height, width)) as image:
                pixels = image.load()
                for index1, _ in enumerate(self.__list_maze):
                    for index2, _ in enumerate(self.__list_maze[index1]):
                        if self.__list_maze[index1][index2] == WAY:
                            pixels[index1, index2] = Colors.WHITE_COLOR
                        else:
                            pixels[index1, index2] = Colors.BLACK_COLOR
                image.save(name)
        elif extension == "TXT":
            with open(name, "w", encoding="utf-8") as ptr:
                for index1, _ in enumerate(self.__list_maze):
                    for index2, _ in enumerate(self.__list_maze[index1]):
                        ptr.write(self.__list_maze[index1][index2])

                    if index1 != len(self.__list_maze) - 1:
                        ptr.write("\n")

    def print_maze(self, list_maze) -> None:  # pylint: disable=no-self-use
        """Печать лабиринта."""
        for row in list_maze:
            print(*row)

    def detour(self, point: list) -> bool:
        """Метод для обхода лабиринта."""
        if point == self.__end_point and point != self.__start_point:
            self.__way_points.push(point)
            return True

        ways = []
        if point != self.__start_point:
            self.__way_points.push(point)
        if (
            self.__list_maze[point[0] + 1][point[1]] != WALL
            and [point[0] + 1, point[1]] not in self.__way_points
            and [point[0] + 1, point[1]] not in self.__use_points
        ):
            ways.append([point[0] + 1, point[1]])

        if (
            self.__list_maze[point[0]][point[1] + 1] != WALL
            and [point[0], point[1] + 1] not in self.__way_points
            and [point[0], point[1] + 1] not in self.__use_points
        ):
            ways.append([point[0], point[1] + 1])

        if (
            self.__list_maze[point[0] - 1][point[1]] != WALL
            and [point[0] - 1, point[1]] not in self.__way_points
            and [point[0] - 1, point[1]] not in self.__use_points
        ):
            ways.append([point[0] - 1, point[1]])

        if (
            self.__list_maze[point[0]][point[1] - 1] != WALL
            and [point[0], point[1] - 1] not in self.__way_points
            and [point[0], point[1] - 1] not in self.__use_points
        ):
            ways.append([point[0], point[1] - 1])

        if ways:
            for pnt in ways:
                self.__list_way.append(pnt)
                result = self.detour(pnt)
                if result:
                    break
                if not result and pnt == ways[-1]:
                    self.__use_points.push(self.__way_points.pop())
            return result
        self.__use_points.push(self.__way_points.pop())
        return False

    def solve_maze(self) -> None:
        """Метод для решения лабиринта."""
        if not self.__start_point and not self.__end_point:
            self.generate_start_point()
            self.generate_end_point()
        self.__way_points.push(self.__start_point)
        self.__list_way.append(self.__start_point)
        self.detour(self.__start_point)

    def create_image(self, path: str) -> None:
        """Метод для сохранения решенного лабиринта."""
        height, width = len(self.__list_maze), len(self.__list_maze[0])
        with Image.new("RGB", (height, width)) as image:
            pixels = image.load()
            for index1, _ in enumerate(self.__list_maze):
                for index2, _ in enumerate(self.__list_maze[index1]):
                    if self.__list_maze[index1][index2] == WAY:
                        if [index1, index2] in self.__use_points:
                            pixels[index1, index2] = Colors.BLUE_COLOR
                        elif [index1, index2] in self.__way_points:
                            pixels[index1, index2] = Colors.RED_COLOR
                        else:
                            pixels[index1, index2] = Colors.WHITE_COLOR
                    else:
                        pixels[index1, index2] = Colors.BLACK_COLOR
            image.save(path)

    def create_gif(self, path: str) -> None:
        """Создание гифки."""
        for item in self.__list_way:
            image = Image.open(path)
            pixels = image.load()
            if item in self.__way_points:
                pixels[item[0], item[1]] = Colors.RED_COLOR
            elif item in self.__use_points:
                pixels[item[0], item[1]] = Colors.BLUE_COLOR
            self.__gif.append(image)
            image.save(path)
        os.remove(path)
