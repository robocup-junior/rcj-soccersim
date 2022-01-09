from typing import List

from referee.consts import BLUE_PENALTY_AREA, YELLOW_PENALTY_AREA


class PenaltyAreaChecker:
    def __init__(self, time_allowed: int, reset_after: int):
        self.time_allowed = time_allowed
        self.reset_after = reset_after
        self.time = None

        self.y_vertical, self.y_lower, self.y_upper = YELLOW_PENALTY_AREA
        self.b_vertical, self.b_lower, self.b_upper = BLUE_PENALTY_AREA
        self.reset()

    def reset(self):
        self.time_entered_penalty = None
        self.time_left_penalty = None

    def is_in_yellow_penalty(self, x: float, y: float) -> bool:
        return y < self.y_vertical and self.y_lower < x < self.y_upper

    def is_in_blue_penalty(self, x: float, y: float) -> bool:
        return y > self.b_vertical and self.b_lower < x < self.b_upper

    @property
    def has_been_outside_penalty_for_longer(self) -> bool:
        return self.time < self.time_left_penalty - self.reset_after

    @property
    def is_inside_penalty_over_limit(self) -> bool:
        return self.time < self.time_entered_penalty - self.time_allowed

    @property
    def has_entered(self) -> bool:
        return self.time_entered_penalty is not None

    @property
    def has_left(self) -> bool:
        return self.time_left_penalty is not None

    def track(self, position: List[float], time: int):
        """Make PenaltyAreaChecker react to a new position.

        Args:
            position (list): Current position of the object
            time (int): Current game time
        """
        self.time = time
        x, y = position[0], position[1]

        if self.is_in_blue_penalty(x, y) or self.is_in_yellow_penalty(x, y):
            # the robot enters the penalty area for the first time
            if not self.has_entered:
                self.time_entered_penalty = self.time
            # the robot re-enters the penalty area
            elif self.has_left:
                self.time_left_penalty = None
        else:
            # the robot has left the penalty area
            if self.has_entered and not self.has_left:
                self.time_left_penalty = self.time
            # the robot keeps being outside the penalty area for longer
            elif self.has_left and self.has_been_outside_penalty_for_longer:
                self.reset()

    def is_violating(self) -> bool:
        """Detect whether the robot stays for longer period of time inside
        the penalty area.

        Returns:
            bool: whether the robot is violating this rule
        """
        if self.has_entered and not self.has_left:
            if self.is_inside_penalty_over_limit:
                return True

        return False
