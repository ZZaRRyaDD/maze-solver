"""Тесты для модуля maze"""
import pytest
from pytest_mock import MockerFixture

from maze_solver.maze import Maze


@pytest.mark.parametrize(
    ["height", "width", "initial", "right_bottom", "way"],
    [[
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
            [1, 1],
            [2, 1],
            [3, 1],
            [4, 1],
            [5, 1],
            [5, 2],
            [5, 3],
            [5, 4],
            [5, 5],
        ],
    ], [
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
            [1, 1],
        ],
    ]],
)
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
    assert all(
        [
            right_bottom[-1] == maze.list_maze,
            way ==
            [
                [point.x_coordinate, point.y_coordinate]
                for point in maze.list_way
            ],
        ]
    )
