from enum import Enum


class Team(Enum):
    BLUE = "B"
    YELLOW = "Y"


class LabelIDs(Enum):
    """Each label ought to have specific ID when calling setLabel function."""

    BLUE_SCORE = 0
    YELLOW_SCORE = 1
    TIME = 2
    EVENT_MESSAGES = 3
    GOAL = 4
    BLUE_TEAM = 5
    YELLOW_TEAM = 6


class GameEvents(Enum):
    MATCH_START = "MATCH_START"
    MATCH_FINISH = "MATCH_FINISH"
    LACK_OF_PROGRESS = "LACK_OF_PROGRESS"
    INSIDE_PENALTY_FOR_TOO_LONG = "INSIDE_PENALTY_FOR_TOO_LONG"
    KICKOFF = "KICKOFF"
    GOAL = "GOAL"


class NeutralSpotDistanceType(Enum):
    FURTHEST = "FURTHEST"
    NEAREST = "NEAREST"
