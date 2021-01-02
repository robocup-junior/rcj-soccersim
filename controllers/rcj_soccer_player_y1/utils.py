from typing import Tuple


def compute_motor_speeds(ball_angle: float) -> Tuple[int, int]:
    # If the robot has the ball right in front of it, go forward,
    # rotate otherwise
    if ball_angle >= 345 or ball_angle <= 15:
        left_speed = -5
        right_speed = -5
    else:
        multiplier = -1 if ball_angle < 180 else 1
        left_speed = multiplier * 4
        right_speed = multiplier * -4

    return left_speed, right_speed
