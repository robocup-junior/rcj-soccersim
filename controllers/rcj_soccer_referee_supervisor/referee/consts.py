from enum import Enum


class Team(Enum):
    BLUE = "B"
    YELLOW = "Y"


DEFAULT_MATCH_TIME = 10 * 60  # 10 minutes

GOAL_YELLOW_X_LIMIT = -0.745
GOAL_BLUE_X_LIMIT = 0.745
GOAL_Z_UPPER_LIMIT = 0.2
GOAL_Z_LOWER_LIMIT = -0.209
GOAL_YELLOW_BACK_WALL_X_LIMIT = -0.849
GOAL_BLUE_BACK_WALL_X_LIMIT = 0.849

FIELD_X_UPPER_LIMIT = 0.755
FIELD_X_LOWER_LIMIT = -0.755
FIELD_Z_UPPER_LIMIT = 0.655
FIELD_Z_LOWER_LIMIT = -0.655

TIME_STEP = 64
ROBOT_NAMES = ["B1", "B2", "B3", "Y1", "Y2", "Y3"]
N_ROBOTS = len(ROBOT_NAMES)

BALL_DEPTH = 0
BALL_INITIAL_TRANSLATION = [0, BALL_DEPTH, 0]

CENTER_NS = "center_ns"
YELLOW_LEFT_NS = "yellow_left_ns"
YELLOW_MIDDLE_NS = "yellow_middle_ns"
YELLOW_RIGHT_NS = "yellow_right_ns"
BLUE_LEFT_NS = "blue_left_ns"
BLUE_MIDDLE_NS = "blue_middle_ns"
BLUE_RIGHT_NS = "blue_right_ns"
NEUTRAL_SPOTS = {
   CENTER_NS:        (0,    0),
   YELLOW_LEFT_NS:   (-0.3, -0.3),
   YELLOW_MIDDLE_NS: (-0.2, 0),
   YELLOW_RIGHT_NS:  (-0.3, 0.3),
   BLUE_LEFT_NS:     (0.3,  0.3),
   BLUE_MIDDLE_NS:   (0.2,  0),
   BLUE_RIGHT_NS:    (0.3,  -0.3),
}

OBJECT_DEPTH = 0.03817

ROBOT_INITIAL_TRANSLATION = {
    "B1": [0.3,  OBJECT_DEPTH, 0.3],
    "B2": [0.3,  OBJECT_DEPTH, -0.3],
    "B3": [0.3,  OBJECT_DEPTH, 0],
    "Y1": [-0.3, OBJECT_DEPTH, -0.3],
    "Y2": [-0.3, OBJECT_DEPTH, 0.3],
    "Y3": [-0.3, OBJECT_DEPTH, 0],
}

ROBOT_INITIAL_ROTATION = {
    "B1": [0, 1, 0, -1.57],
    "B2": [0, 1, 0, -1.57],
    "B3": [0, 1, 0, -1.57],
    "Y1": [0, 1, 0, 1.57],
    "Y2": [0, 1, 0, 1.57],
    "Y3": [0, 1, 0, 1.57],
}

BLUE_KICKOFF_TRANSLATION = [0.1, OBJECT_DEPTH, 0]
YELLOW_KICKOFF_TRANSLATION = [-0.1, OBJECT_DEPTH, 0]

KICKOFF_TRANSLATION = {
    Team.BLUE.value: BLUE_KICKOFF_TRANSLATION,
    Team.YELLOW.value: YELLOW_KICKOFF_TRANSLATION
}

# (vertical boundary x, lower boundary z, upper boundary z)
YELLOW_PENALTY_AREA = (-0.59, -0.35, 0.35)
BLUE_PENALTY_AREA = (0.59, -0.35, 0.35)

MAX_EVENT_MESSAGES_IN_QUEUE = 10

DISTANCE_AROUND_UNOCCUPIED_NEUTRAL_SPOT = 0.08

LACK_OF_PROGRESS_NUMBER_OF_NEUTRAL_SPOTS = 3


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
