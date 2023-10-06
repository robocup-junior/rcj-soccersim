import sys
from unittest.mock import MagicMock

sys.modules["controller"] = MagicMock()

import pytest

from referee.consts import MAX_EVENT_MESSAGES_IN_QUEUE
from referee.referee import RCJSoccerReferee


@pytest.fixture
def referee() -> RCJSoccerReferee:
    supervisor = MagicMock()
    return RCJSoccerReferee(
        supervisor=supervisor,
        match_time=600,
        progress_check_steps=235,
        progress_check_threshold=0.5,
        ball_progress_check_steps=235,
        ball_progress_check_threshold=0.5,
        team_name_blue="Blues",
        team_name_yellow="Yellows",
        initial_score_blue=0,
        initial_score_yellow=0,
        penalty_area_allowed_time=15,
        penalty_area_reset_after=2,
        match_id=1,
        half_id=1,
        initial_position_noise=0.15,
    )


def test_pack_packet(referee: RCJSoccerReferee):
    assert referee._pack_data() == '{"waiting_for_kickoff": false}'


def test_add_initial_position_noise(referee: RCJSoccerReferee):
    position = [0.0, 0.0, 0.0]
    new_position = referee._add_initial_position_noise(position)

    assert -0.075 <= new_position[0] < 0.075
    assert -0.075 <= new_position[1] < 0.075
    assert new_position[2] == 0.0


def test_add_event_message_to_queue(referee: RCJSoccerReferee):
    assert referee.event_messages_to_draw == []

    for i in range(1, MAX_EVENT_MESSAGES_IN_QUEUE + 1):
        referee.add_event_message_to_queue(str(i))
        assert len(referee.event_messages_to_draw) == i
        assert referee.event_messages_to_draw[-1] == (referee.time, str(i))

    referee.add_event_message_to_queue(str(MAX_EVENT_MESSAGES_IN_QUEUE + 1))
    assert len(referee.event_messages_to_draw) == MAX_EVENT_MESSAGES_IN_QUEUE
    assert referee.event_messages_to_draw[-1] == (
        referee.time,
        str(MAX_EVENT_MESSAGES_IN_QUEUE + 1),
    )
    assert referee.event_messages_to_draw[0] == (referee.time, "2")
