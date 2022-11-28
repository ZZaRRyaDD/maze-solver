"""Модуль с лабиринтом."""
import os
import random
from typing import Optional

from PIL import Image

from maze_solver.constants import Colors, Objects
from maze_solver.point import Point
from maze_solver.stack import Stack


class Maze:
    """Класс для генерации лабиринта."""

    def __init__(
        self,
        path: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> None:
        self.__list_maze: list[str] = []
        self.__start_point: Optional[Point] = None
        self.__end_point: Optional[Point] = None
        self.__path = ""
        self.__gif: list[Image] = []
        self.__way_points: Stack[Point] = Stack()
        self.__list_way: list[Point] = []
        self.__use_points: Stack[Point] = Stack()
        if width and height:
            self.generate(width, height)
        elif path:
            self.from_other_format(path)
        else:
            raise ValueError("Введите либо размеры, либо путь к файлу")

    @property
    def start_point(self) -> Point:
        """Геттер для пути до изображения."""
        return self.__start_point

    @start_point.setter
    def start_point(self, value: Point) -> None:
        """Сеттер для пути до изображения."""
        self.__start_point = value

    @property
    def end_point(self) -> Point:
        """Геттер для пути до изображения."""
        return self.__end_point

    @end_point.setter
    def end_point(self, value: Point) -> None:
        """Сеттер для пути до изображения."""
        self.__end_point = value

    @property
    def way_points(self) -> Stack:
        """Стек с точками, соответствующие путю."""
        return self.__way_points

    @property
    def list_way(self) -> list[Point]:
        """Список с точками, соответствущие путю."""
        return self.__list_way

    @property
    def gif(self) -> list[Point]:
        """Геттер для гифки."""
        return self.__gif

    @property
    def path(self) -> str:
        """Геттер для пути до изображения."""
        return self.__path

    @path.setter
    def path(self, value: str) -> None:
        """Сеттер для пути до изображения."""
        self.__path = value

    @property
    def list_maze(self) -> list[str]:
        """Возвращает лабиринт."""
        return self.__list_maze

    def from_other_format(self, path: str) -> None:
        """Функция для перевода из другого формата."""
        if path.endswith(".png"):
            with Image.open(path) as image:
                pixels = image.load()
                width, height = image.size
                for index1 in range(width):
                    row = []
                    for index2 in range(height):
                        if pixels[index1, index2] == Colors.WHITE_COLOR:
                            row.append(Objects.WAY)
                        elif pixels[index1, index2] == Colors.BLACK_COLOR:
                            row.append(Objects.WALL)
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
                    if char == Objects.WAY:
                        row.append(char)
                    elif char == Objects.WALL:
                        row.append(char)
                    elif char == "\n":
                        self.__list_maze.append(row)
                        row = []
                self.__list_maze.append(row)
        else:
            raise ValueError("Не верный формат файла")

    def generate_start_point(self) -> None:
        """Генерация начальной точки лабиринта."""
        self.__start_point = Point(1, 1)

    def generate_end_point(self) -> None:
        """Генерация конечной точки лабиринта."""
        height = len(self.__list_maze)
        width = len(self.__list_maze[0])
        point1 = self.__list_maze[height - 2][width - 2]
        point2 = self.__list_maze[height - 3][width - 2]
        if point1 != Objects.WALL:
            self.__end_point = Point(height - 2, width - 2)
        elif point2 != Objects.WALL:
            self.__end_point = Point(height - 3, width - 2)
        else:
            self.__end_point = Point(height - 2, width - 3)

    def init_base_data(
        self,
        output_height: int,
        output_width: int,
        list_maze: list,
    ) -> list:
        """Инициализация лабиринта начальными значениями."""
        for i in range(output_height):
            row = []
            for j in range(output_width):
                if i % 2 == 1 and j % 2 == 1:
                    row.append(Objects.WAY)
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
                        Objects.WAY
                        if any([first_cond, second_cond])
                        else Objects.WALL
                    )
            list_maze.append(row)
        return list_maze

    def assign_set(
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

    def build_right_walls(
        self,
        width: int,
        i: int,
        row_set: list,
        list_maze: list,
    ) -> list:
        """Добавляем стены."""
        for j in range(width - 1):
            if random.randint(0, 1) or row_set[j] == row_set[j + 1]:
                list_maze[i * 2 + 1][j * 2 + 2] = Objects.WALL
            else:
                changing_set = row_set[j + 1]
                for index in range(width):
                    if row_set[index] == changing_set:
                        row_set[index] = row_set[j]
        return list_maze

    def build_bottom_walls(
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
                list_maze[i * 2 + 2][j * 2 + 1] = Objects.WALL
        return list_maze

    def check_walls(
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
                        list_maze[i * 2 + 2][index * 2 + 1] == Objects.WAY
                    ):
                        count_hole += 1
                if not count_hole:
                    list_maze[i * 2 + 2][j * 2 + 1] = Objects.WAY
        if i != height - 1:
            for j in range(width):
                if list_maze[i * 2 + 2][j * 2 + 1] == Objects.WALL:
                    row_set[j] = 0
        return list_maze

    def generate(self, width: int, height: int) -> None:
        """Метод для генерации лабиринта."""
        output_height, output_width = height * 2 + 1, width * 2 + 1
        list_maze = []
        list_maze = self.init_base_data(
            output_height,
            output_width,
            list_maze,
        )
        row_set = [0 for _ in range(width)]
        counter = 1

        for i in range(height):
            counter = self.assign_set(width, counter, row_set)
            list_maze = self.build_right_walls(width, i, row_set, list_maze)
            list_maze = self.build_bottom_walls(width, i, row_set, list_maze)
            list_maze = self.check_walls(height, width, i, row_set, list_maze)

        for j in range(width - 1):
            if row_set[j] != row_set[j + 1]:
                list_maze[output_height - 2][j * 2 + 2] = Objects.WAY

        self.__list_maze = list_maze

    def save(self, name: str, extension: str) -> None:
        """Переводит лабиринт в изображение."""
        name = f"../mazes/{name}.{extension}"
        if extension == "png":
            height, width = len(self.__list_maze), len(self.__list_maze[0])
            with Image.new("RGB", (height, width)) as image:
                pixels = image.load()
                for index1, _ in enumerate(self.__list_maze):
                    for index2, _ in enumerate(self.__list_maze[index1]):
                        if self.__list_maze[index1][index2] == Objects.WAY:
                            pixels[index1, index2] = Colors.WHITE_COLOR
                        else:
                            pixels[index1, index2] = Colors.BLACK_COLOR
                image.save(name)
        elif extension == "txt":
            with open(name, "w", encoding="utf-8") as ptr:
                for index1, _ in enumerate(self.__list_maze):
                    for index2, _ in enumerate(self.__list_maze[index1]):
                        ptr.write(self.__list_maze[index1][index2])

                    if index1 != len(self.__list_maze) - 1:
                        ptr.write("\n")

    def print_maze(self, list_maze) -> None:
        """Печать лабиринта."""
        for row in list_maze:
            print(*row)

    def detour(self, point: Point) -> bool:
        """Метод для обхода лабиринта."""
        if point == self.__end_point and point != self.__start_point:
            self.__way_points.push(point)
            return True

        ways = []
        if point != self.__start_point:
            self.__way_points.push(point)

        future_point = Point(point.x_coordinate + 1, point.y_coordinate)
        if all([
            self.__list_maze[point.x_coordinate + 1][point.y_coordinate] != Objects.WALL,
            future_point not in self.__way_points,
            future_point not in self.__use_points,
        ]):
            ways.append(future_point)

        future_point = Point(point.x_coordinate, point.y_coordinate + 1)
        if all([
            self.__list_maze[point.x_coordinate][point.y_coordinate + 1] != Objects.WALL,
            future_point not in self.__way_points,
            future_point not in self.__use_points,
        ]):
            ways.append(future_point)

        future_point = Point(point.x_coordinate - 1, point.y_coordinate)
        if all([
            self.__list_maze[point.x_coordinate - 1][point.y_coordinate] != Objects.WALL,
            future_point not in self.__way_points,
            future_point not in self.__use_points,
        ]):
            ways.append(future_point)

        future_point = Point(point.x_coordinate, point.y_coordinate - 1)
        if all([
            self.__list_maze[point.x_coordinate][point.y_coordinate - 1] != Objects.WALL,
            future_point not in self.__way_points,
            future_point not in self.__use_points,
        ]):
            ways.append(future_point)

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
        if self.__start_point is None and self.__end_point is None:
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
                    point = Point(index1, index2)
                    if self.__list_maze[index1][index2] == Objects.WAY:
                        if point in self.__use_points:
                            pixels[index1, index2] = Colors.BLUE_COLOR
                        elif point in self.__way_points:
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
                pixels[item.x_coordinate, item.y_coordinate] = Colors.RED_COLOR
            elif item in self.__use_points:
                pixels[item.x_coordinate, item.y_coordinate] = Colors.BLUE_COLOR
            self.__gif.append(image)
            image.save(path)
        os.remove(path)
