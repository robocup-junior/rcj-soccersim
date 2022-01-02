from unittest.mock import MagicMock

import pytest

from referee.event_handlers import EventHandler
from referee.eventer import Eventer


@pytest.fixture
def eventer() -> Eventer:
    return Eventer()


def test_no_subscribers(eventer: Eventer):
    assert eventer.subscribers == []


def test_subscribers_exist(eventer: Eventer):
    subscriber1 = EventHandler()
    subscriber2 = EventHandler()
    eventer.subscribe(subscriber1)
    eventer.subscribe(subscriber2)

    assert eventer.subscribers == [subscriber1, subscriber2]


def test_event(eventer: Eventer):
    subscriber1 = EventHandler()
    subscriber2 = EventHandler()
    subscriber1.handle = MagicMock()
    subscriber2.handle = MagicMock()
    eventer.subscribe(subscriber1)
    eventer.subscribe(subscriber2)

    eventer.event("arg", kwarg="test")

    subscriber1.handle.assert_called_with("arg", kwarg="test")
    subscriber2.handle.assert_called_with("arg", kwarg="test")
