from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Point:
    """Класс с информацией о точке."""

    x_coordinate: int
    y_coordinate: int

    def __eq__(self, __o: object) -> bool:
        """Метод для сравнения двух объектов одного класса."""
        if not isinstance(__o, Point):
            return False
        if any([
            self.x_coordinate != __o.x_coordinate,
            self.y_coordinate != __o.y_coordinate,
        ]):
            return False
        return True
