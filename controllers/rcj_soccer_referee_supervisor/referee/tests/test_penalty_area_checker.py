from typing import List

import pytest

from referee.consts import BLUE_PENALTY_AREA, YELLOW_PENALTY_AREA
from referee.penalty_area_checker import PenaltyAreaChecker


@pytest.fixture
def checker() -> PenaltyAreaChecker:
    return PenaltyAreaChecker(time_allowed=15, reset_after=2)


@pytest.fixture
def outside_penalty_pos() -> List[float]:
    return [0.0, 0.0, 0.0]


@pytest.fixture
def in_yellow_penalty_pos() -> List[float]:
    return [
        YELLOW_PENALTY_AREA[2] - 0.001,
        YELLOW_PENALTY_AREA[0] - 0.001,
        0.0,
    ]


@pytest.fixture
def in_blue_penalty_pos() -> List[float]:
    return [
        BLUE_PENALTY_AREA[2] - 0.001,
        BLUE_PENALTY_AREA[0] + 0.001,
        0.0,
    ]


@pytest.mark.parametrize(
    "x,y,expected",
    [
        (0.0, 0.0, False),
        (YELLOW_PENALTY_AREA[2], YELLOW_PENALTY_AREA[0], False),
        (YELLOW_PENALTY_AREA[2] - 0.001, YELLOW_PENALTY_AREA[0] - 0.001, True),
    ],
)
def test_is_in_yellow_penalty(
    x: float, y: float, expected: bool, checker: PenaltyAreaChecker
):
    assert checker.is_in_yellow_penalty(x, y) == expected


@pytest.mark.parametrize(
    "x,y,expected",
    [
        (0.0, 0.0, False),
        (BLUE_PENALTY_AREA[2], BLUE_PENALTY_AREA[0], False),
        (BLUE_PENALTY_AREA[2] - 0.001, BLUE_PENALTY_AREA[0] + 0.001, True),
    ],
)
def test_is_in_blue_penalty(
    x: float, y: float, expected: bool, checker: PenaltyAreaChecker
):
    assert checker.is_in_blue_penalty(x, y) == expected


def test_outside_penalty_area(checker: PenaltyAreaChecker):
    checker.track([0.0, 0.0, 0.0], 60)

    assert not checker.has_entered
    assert not checker.has_left
    assert checker.time_entered_penalty is None
    assert checker.time_left_penalty is None
    assert not checker.is_violating()


def test_enter_yellow_penalty_area(
    checker: PenaltyAreaChecker, in_yellow_penalty_pos: List[float]
):
    checker.track(in_yellow_penalty_pos, 60)

    assert checker.has_entered
    assert not checker.has_left
    assert checker.time_entered_penalty == 60


def test_enter_blue_penalty_area(
    checker: PenaltyAreaChecker, in_blue_penalty_pos: List[float]
):
    checker.track(in_blue_penalty_pos, 60)

    assert checker.has_entered
    assert not checker.has_left
    assert checker.time_entered_penalty == 60


def test_left_penalty_area(
    checker: PenaltyAreaChecker,
    in_yellow_penalty_pos: List[float],
    outside_penalty_pos: List[float],
):
    checker.track(in_yellow_penalty_pos, 60)
    checker.track(outside_penalty_pos, 59)

    assert checker.has_entered
    assert checker.has_left
    assert checker.time_left_penalty == 59
    assert not checker.has_been_outside_penalty_for_longer


def test_left_penalty_area_for_longer(
    checker: PenaltyAreaChecker,
    in_yellow_penalty_pos: List[float],
    outside_penalty_pos: List[float],
):
    checker.track(in_yellow_penalty_pos, 60)
    checker.track(outside_penalty_pos, 59)
    checker.track(outside_penalty_pos, 56)

    assert not checker.has_entered
    assert not checker.has_left


def test_reenter_penalty_area(
    checker: PenaltyAreaChecker,
    in_yellow_penalty_pos: List[float],
    outside_penalty_pos: List[float],
):
    checker.track(in_yellow_penalty_pos, 60)
    checker.track(outside_penalty_pos, 59)
    checker.track(in_yellow_penalty_pos, 58)

    assert checker.time_entered_penalty == 60
    assert not checker.has_left
    assert not checker.is_violating()


def test_violating(
    checker: PenaltyAreaChecker,
    in_yellow_penalty_pos: List[float],
    outside_penalty_pos: List[float],
):
    checker.track(in_yellow_penalty_pos, 60)
    checker.track(outside_penalty_pos, 59)
    checker.track(in_yellow_penalty_pos, 57)
    checker.track(in_yellow_penalty_pos, 40)

    assert checker.is_violating()
