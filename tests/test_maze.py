"""Тесты для модуля maze"""
import pytest
from pytest_mock import MockerFixture

from maze_solver.maze import Maze
from maze_solver.point import Point


@pytest.mark.parametrize(["height", "width", "initial", "right_bottom", "way"], [
    [
        3,
        3,
        [
            ["0", "0", "0", "0", "0", "0", "0"],
            ["0", "1", "1", "1", "1", "1", "0"],
            ["0", "1", "0", "1", "0", "1", "0"],
            ["0", "1", "1", "1", "1", "1", "0"],
            ["0", "1", "0", "1", "0", "1", "0"],
            ["0", "1", "1", "1", "1", "1", "0"],
            ["0", "0", "0", "0", "0", "0", "0"],
        ],
        [
            [
                ["0", "0", "0", "0", "0", "0", "0"],
                ["0", "1", "0", "1", "0", "1", "0"],
                ["0", "1", "0", "1", "0", "1", "0"],
                ["0", "1", "1", "1", "1", "1", "0"],
                ["0", "1", "0", "1", "0", "1", "0"],
                ["0", "1", "1", "1", "1", "1", "0"],
                ["0", "0", "0", "0", "0", "0", "0"],
            ],
            [
                ["0", "0", "0", "0", "0", "0", "0"],
                ["0", "1", "0", "1", "0", "1", "0"],
                ["0", "1", "0", "1", "0", "1", "0"],
                ["0", "1", "0", "1", "0", "1", "0"],
                ["0", "1", "0", "1", "0", "1", "0"],
                ["0", "1", "1", "1", "1", "1", "0"],
                ["0", "0", "0", "0", "0", "0", "0"],
            ],
            [
                ["0", "0", "0", "0", "0", "0", "0"],
                ["0", "1", "0", "1", "0", "1", "0"],
                ["0", "1", "0", "1", "0", "1", "0"],
                ["0", "1", "0", "1", "0", "1", "0"],
                ["0", "1", "0", "1", "0", "1", "0"],
                ["0", "1", "1", "1", "1", "1", "0"],
                ["0", "0", "0", "0", "0", "0", "0"],
            ],
        ],
        [
            Point(1, 1),
            Point(2, 1),
            Point(3, 1),
            Point(4, 1),
            Point(5, 1),
            Point(5, 2),
            Point(5, 3),
            Point(5, 4),
            Point(5, 5),
        ],
    ],
    [
        1,
        1,
        [
            ["0", "0", "0"],
            ["0", "1", "0"],
            ["0", "0", "0"],
        ],
        [
            [
                ["0", "0", "0"],
                ["0", "1", "0"],
                ["0", "0", "0"],
            ],
        ],
        [
            Point(1, 1),
        ],
    ],
])
def test_maze(
    mocker: MockerFixture,
    height: int,
    width: int,
    initial: list,
    right_bottom: list,
    way: list,
) -> None:
    """Тест генерации и решения лабиринта."""
    mocker.patch("maze_solver.maze.Maze.init_base_data", side_effect=initial)
    mocker.patch("maze_solver.maze.Maze.build_right_walls", side_effect=right_bottom)
    mocker.patch("maze_solver.maze.Maze.build_bottom_walls", side_effect=right_bottom)
    mocker.patch("maze_solver.maze.Maze.check_walls", side_effect=right_bottom)
    maze = Maze(height=height, width=width)
    maze.solve_maze()

    assert all([right_bottom[-1] == maze.list_maze, way == maze.list_way])
