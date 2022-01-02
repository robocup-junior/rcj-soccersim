from typing import Any

import pytest

from referee.consts import (
    FIELD_X_LOWER_LIMIT,
    FIELD_X_UPPER_LIMIT,
    FIELD_Y_LOWER_LIMIT,
    FIELD_Y_UPPER_LIMIT,
    GOAL_BLUE_BACK_WALL_Y_LIMIT,
    GOAL_BLUE_Y_LIMIT,
    GOAL_X_LOWER_LIMIT,
    GOAL_X_UPPER_LIMIT,
    GOAL_YELLOW_BACK_WALL_Y_LIMIT,
    GOAL_YELLOW_Y_LIMIT,
)
from referee.utils import (
    is_in_blue_goal,
    is_in_yellow_goal,
    is_outside,
    time_to_string,
)


@pytest.mark.parametrize(
    "time,expected",
    [
        (10, "00:10"),
        (1234, "20:34"),
        (0, "00:00"),
    ],
)
def test_time_to_string_ok(time: int, expected: str):
    assert time_to_string(time) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (-1, ValueError),
        (None, TypeError),
        ("1", TypeError),
    ],
)
def test_time_to_string_wrong_value(value: Any, expected: Exception):
    with pytest.raises(expected):
        time_to_string(value)


@pytest.mark.parametrize(
    "x,y,expected",
    [
        (0.0, -0.8, True),
        (0.0, 0.0, False),
        (0.0, GOAL_YELLOW_Y_LIMIT, False),
        (GOAL_X_UPPER_LIMIT, -0.8, False),
        (GOAL_X_LOWER_LIMIT, -0.8, False),
        (0.0, GOAL_YELLOW_BACK_WALL_Y_LIMIT, False),
    ],
)
def test_is_in_yellow_goal(x: float, y: float, expected: bool):
    assert is_in_yellow_goal(x, y) == expected


@pytest.mark.parametrize(
    "x,y,expected",
    [
        (0.0, 0.8, True),
        (0.0, 0.0, False),
        (0.0, GOAL_BLUE_Y_LIMIT, False),
        (GOAL_X_UPPER_LIMIT, 0.8, False),
        (GOAL_X_LOWER_LIMIT, 0.8, False),
        (0.0, GOAL_BLUE_BACK_WALL_Y_LIMIT, False),
    ],
)
def test_is_in_blue_goal(x: float, y: float, expected: bool):
    assert is_in_blue_goal(x, y) == expected


@pytest.mark.parametrize(
    "x,y,expected",
    [
        (0.0, 0.0, False),
        (0.0, FIELD_Y_UPPER_LIMIT, False),  # In blue goal
        (0.0, FIELD_Y_LOWER_LIMIT, False),  # In yellow goal
        (FIELD_X_UPPER_LIMIT + 0.0001, 0.0, True),
        (FIELD_X_LOWER_LIMIT - 0.0001, 0.0, True),
        (0.0, GOAL_YELLOW_BACK_WALL_Y_LIMIT, True),
        (0.0, GOAL_BLUE_BACK_WALL_Y_LIMIT, True),
        (GOAL_X_UPPER_LIMIT, FIELD_Y_UPPER_LIMIT + 0.0001, True),
        (GOAL_X_UPPER_LIMIT, FIELD_Y_LOWER_LIMIT - 0.0001, True),
        (GOAL_X_LOWER_LIMIT, FIELD_Y_UPPER_LIMIT + 0.0001, True),
        (GOAL_X_LOWER_LIMIT, FIELD_Y_LOWER_LIMIT - 0.0001, True),
    ],
)
def test_is_outside(x: float, y: float, expected: bool):
    assert is_outside(x, y) == expected
