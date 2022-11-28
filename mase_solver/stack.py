"""Модуль со стеком."""
from typing import Any, Optional, Union


class Stack:
    """Класс стека."""

    def __init__(self, items: Optional[list] = None) -> None:
        self.__items = []
        if items:
            for item in items:
                self.__items.append(item)

    def __getitem__(self, key: int) -> list:
        """Возвращает элемент по ключу."""
        return self.__items[key]

    def __setitem__(self, key: int, value: list) -> None:
        """Задает элемент по ключу."""
        self.__items[key] = value

    def push(self, item: list) -> None:
        """Вставляет элемент."""
        self.__items.append(item)

    def pop(self) -> list:
        """Удаляет элемент и возвращает его."""
        return self.__items.pop()

    def size(self) -> int:
        """Возвращает размер стека."""
        return len(self.__items)

    def __eq__(self, other: Union["Stack", Any]) -> bool:
        if not isinstance(other, Stack):
            return False

        if self.size() != other.size():
            return False

        inspect = True
        for index, _ in enumerate(self.__items):
            if self.__items[index] != other[index]:
                inspect = False
                break
        return inspect
