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


def time_to_string(time: int) -> str:
    """Convert time to string representation

    Args:
        time (int): Time in seconds

    Returns:
        str: Time in MM:SS format
    """
    if time < 0:
        raise ValueError("Negative integer not supported")
    return "%02d:%02d" % (time // 60, time % 60)


def is_in_yellow_goal(x: float, y: float) -> bool:
    """Return whether object is located in the yellow goal.

    Args:
        x (float): X position
        y (float): Y position

    Returns:
        bool: True if the object is located in the yellow goal
    """
    if GOAL_X_LOWER_LIMIT < x < GOAL_X_UPPER_LIMIT:
        if GOAL_YELLOW_BACK_WALL_Y_LIMIT < y < GOAL_YELLOW_Y_LIMIT:
            return True
    return False


def is_in_blue_goal(x: float, y: float) -> bool:
    """Return whether object is located in the blue goal.

    Args:
        x (float): X position
        y (float): Y position

    Returns:
        bool: True if the object is located in the blue goal
    """
    if GOAL_X_LOWER_LIMIT < x < GOAL_X_UPPER_LIMIT:
        if GOAL_BLUE_Y_LIMIT < y < GOAL_BLUE_BACK_WALL_Y_LIMIT:
            return True
    return False


def is_outside(x: float, y: float) -> bool:
    """Return whether object is located outside the field.

    Args:
        x (float): X position
        y (float): Y position

    Returns:
        bool: True if the object is located outside
    """
    if x > FIELD_X_UPPER_LIMIT or x < FIELD_X_LOWER_LIMIT:
        return True

    if y < FIELD_Y_LOWER_LIMIT or y > FIELD_Y_UPPER_LIMIT:
        return not (is_in_blue_goal(x, y) or is_in_yellow_goal(x, y))

    return False
