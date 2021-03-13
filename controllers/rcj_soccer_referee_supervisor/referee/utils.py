from referee.consts import (
    GOAL_BLUE_X_LIMIT,
    GOAL_BLUE_BACK_WALL_X_LIMIT,
    GOAL_YELLOW_BACK_WALL_X_LIMIT,
    GOAL_YELLOW_X_LIMIT,
    GOAL_Z_UPPER_LIMIT,
    GOAL_Z_LOWER_LIMIT,
    FIELD_X_LOWER_LIMIT,
    FIELD_X_UPPER_LIMIT,
    FIELD_Z_UPPER_LIMIT,
    FIELD_Z_LOWER_LIMIT,
)


def time_to_string(time: int) -> str:
    """Convert time to string representation

    Args:
        time (int): Time in seconds

    Returns:
        str: Time in MM:SS format
    """
    return "%02d:%02d" % (time // 60, time % 60)


def is_in_yellow_goal(x: int, z: int) -> bool:
    """Return whether object is located in the yellow goal.

    Args:
        x (int): X position
        z (int): Z position

    Returns:
        bool: True if the object is located in the yellow goal
    """
    if GOAL_Z_LOWER_LIMIT < z < GOAL_Z_UPPER_LIMIT:
        if GOAL_YELLOW_BACK_WALL_X_LIMIT < x < GOAL_YELLOW_X_LIMIT:
            return True
    return False


def is_in_blue_goal(x: int, z: int) -> bool:
    """Return whether object is located in the blue goal.

    Args:
        x (int): X position
        z (int): Z position

    Returns:
        bool: True if the object is located in the blue goal
    """
    if GOAL_Z_LOWER_LIMIT < z < GOAL_Z_UPPER_LIMIT:
        if GOAL_BLUE_X_LIMIT < x < GOAL_BLUE_BACK_WALL_X_LIMIT:
            return True
    return False


def is_outside(x: int, z: int) -> bool:
    """Return whether object is located outside the field.

    Args:
        x (int): X position
        z (int): Z position

    Returns:
        bool: True if the object is located outside
    """
    if z > FIELD_Z_UPPER_LIMIT or z < FIELD_Z_LOWER_LIMIT:
        return True

    if x < FIELD_X_LOWER_LIMIT or x > FIELD_X_UPPER_LIMIT:
        return not (is_in_blue_goal(x, z) or is_in_yellow_goal(x, z))

    return False
