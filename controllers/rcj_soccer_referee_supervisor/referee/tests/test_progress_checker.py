import pytest

from referee.progress_checker import ProgressChecker


@pytest.fixture
def checker() -> ProgressChecker:
    return ProgressChecker(steps=235, threshold=0.5)


def test_initialize(checker: ProgressChecker):
    assert len(checker.samples) == 235
    assert checker.iterator == 0
    assert checker.prev_position is None


def test_first_track(checker: ProgressChecker):
    position = [0.0, 0.0, 0.0]
    checker.track(position)

    assert checker.prev_position == position
    assert checker.samples[0] == 0


def test_track_multiple_times(checker: ProgressChecker):
    checker.track([0.0, 0.0, 0.0])
    checker.track([0.01, 0.0, 0.0])
    checker.track([0.02, 0.0, 0.0])

    assert checker.iterator == 2
    assert checker.samples[0] == 0.01
    assert checker.samples[1] == 0.01
    assert checker.samples[2] == 0
    assert checker.prev_position == [0.02, 0.0, 0.0]


def test_progress_after_initialize(checker: ProgressChecker):
    assert checker.is_progress()


def test_progress_not_enough_steps(checker: ProgressChecker):
    checker.iterator = 234

    assert checker.is_progress()


def test_progress_enough_steps(checker: ProgressChecker):
    checker.iterator = 235

    assert not checker.is_progress()


def test_no_progress(checker: ProgressChecker):
    x = 0.0
    checker.track([x, 0.0, 0.0])
    for _ in range(234):
        x += 0.002
        checker.track([x, 0.0, 0.0])
        assert checker.is_progress()

    checker.track([x + 0.002, 0.0, 0.0])
    assert not checker.is_progress()


def test_progress_ok(checker: ProgressChecker):
    for _ in range(235):
        checker.track([0.0, 0.0, 0.0])
        assert checker.is_progress()

    checker.track([0.5, 0.0, 0.0])
    assert checker.is_progress()
