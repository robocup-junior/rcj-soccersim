import math
from typing import List, Tuple

from controller import Supervisor

from referee.consts import (
    BALL_DEPTH,
    DISTANCE_AROUND_UNOCCUPIED_NEUTRAL_SPOT,
    NEUTRAL_SPOTS,
    OBJECT_DEPTH,
    ROBOT_INITIAL_ROTATION,
    ROBOT_NAMES,
)
from referee.enums import LabelIDs, NeutralSpotDistanceType
from referee.utils import time_to_string


class RCJSoccerSupervisor(Supervisor):
    def __init__(self):
        super().__init__()

        self.emitter = self.getDevice("emitter")

        self.ball = self.getFromDef("BALL")
        self.ball_translation_field = self.ball.getField("translation")
        self.ball_translation = self.ball_translation_field.getSFVec3f()

        self.robot_nodes = {}
        self.robot_translation_fields = {}
        self.robot_rotation_fields = {}
        self.robot_translation = {}
        self.robot_rotation = {}
        self.robot_reset_physics = {}
        for robot in ROBOT_NAMES:
            robot_node = self.getFromDef(robot)
            self.robot_nodes[robot] = robot_node

            field = robot_node.getField("translation")
            self.robot_translation_fields[robot] = field
            self.robot_translation[robot] = field.getSFVec3f()

            field = robot_node.getField("rotation")
            self.robot_rotation_fields[robot] = field
            self.robot_rotation[robot] = field.getSFRotation()

            self.robot_reset_physics[robot] = 0

    def check_reset_physics_counters(self):
        # HACK(Richo): Workaround for the following issue
        # https://github.com/RoboCupJuniorTC/rcj-soccersim/issues/130
        for robot in ROBOT_NAMES:
            reset_physics_counter = self.robot_reset_physics[robot]
            if reset_physics_counter > 0:
                self.robot_nodes[robot].resetPhysics()
                self.robot_reset_physics[robot] = reset_physics_counter - 1

    def update_positions(self):
        """Update the positions of robots and the ball"""
        self.ball_translation = self.ball_translation_field.getSFVec3f()

        for robot in ROBOT_NAMES:
            t = self.robot_translation_fields[robot].getSFVec3f()
            self.robot_translation[robot] = t

            r = self.robot_rotation_fields[robot].getSFRotation()
            self.robot_rotation[robot] = r

        assert len(self.robot_translation) == len(self.robot_rotation)

    def get_robot_translation(self, robot: str) -> list:
        """Return the position of the robot.

        Args:
            robot (str): The robot whose position is returned

        Returns:
            list: x, y and z coordinates
        """
        return self.robot_translation[robot]

    def get_ball_translation(self) -> list:
        """Return the position of the ball.

        Returns:
            list: x, y and z coordinates
        """
        return self.ball_translation

    def set_robot_position(self, robot_name: str, position: List[float]):
        """Set the position of a robot.

        Args:
            robot_name (str): The robot we are moving
            position (list of floats): The actual position
        """
        tr_field = self.robot_translation_fields[robot_name]
        tr_field.setSFVec3f(position)
        self.robot_reset_physics[robot_name] = 1
        self.robot_nodes[robot_name].resetPhysics()
        self.robot_translation[robot_name] = position

    def set_robot_rotation(self, robot_name: str, rotation: List[float]):
        """Set the rotation of a robot.

        Args:
            robot_name (str): The robot we are rotating
            rotation (list of floats): The actual rotation
        """
        rot_field = self.robot_rotation_fields[robot_name]
        rot_field.setSFRotation(rotation)
        self.robot_rotation[robot_name] = rotation

    def set_ball_position(self, position: List[float]):
        """Set the position of the ball.

        Args:
            position (list of floats): The actual position
        """
        self.ball_translation_field.setSFVec3f(position)
        self.reset_ball_velocity()
        self.ball.resetPhysics()
        self.ball_translation = position

    def reset_robot_velocity(self, robot_name: str):
        """Reset the robot's velocity.

        Args:
            robot_name (str): The robot we set the velocity for
        """
        self.robot_nodes[robot_name].setVelocity([0, 0, 0, 0, 0, 0])

    def reset_ball_velocity(self):
        """Reset the ball's velocity."""
        self.ball.setVelocity([0, 0, 0, 0, 0, 0])

    def is_neutral_spot_occupied(self, ns_x: float, ns_y: float) -> bool:
        """Check whether the specific neutral spot is occupied

        Args:
            ns_x (float): x position of the neutral spot
            ns_y (float): y position of the neutral spot

        Returns:
            bool: Whether the neutral spot is unoccupied
        """
        # Check whether any of the robots is blocking the neutral spot
        for _, pos in self.robot_translation.items():
            rx, ry = pos[0], pos[1]
            distance = math.sqrt((rx - ns_x) ** 2 + (ry - ns_y) ** 2)
            if distance < DISTANCE_AROUND_UNOCCUPIED_NEUTRAL_SPOT:
                return True

        # Check whether the ball is blocking the neutral spot
        bx, by = self.ball_translation[0], self.ball_translation[1]
        distance = math.sqrt((bx - ns_x) ** 2 + (by - ns_y) ** 2)
        if distance < DISTANCE_AROUND_UNOCCUPIED_NEUTRAL_SPOT:
            return True

        return False

    def get_unoccupied_neutral_spots_sorted(
        self,
        distance_type: NeutralSpotDistanceType,
        object_name: str,
    ) -> List[Tuple[str, float]]:
        """Get sorted pairs of (neutral_spot, distance)
        sorted according to distance_type.
        Furthest distance type -> descending order
        Nearest distance type -> ascending order

        Args:
            distance_type (NeutralSpotDistanceType): Either nearest or furthest
            object_name (str): Get the spot for this object

        Returns:
            list: sorted pairs of neutral spots and their distances
        """
        if object_name == "ball":
            x = self.ball_translation[0]
            y = self.ball_translation[1]
        else:
            x = self.robot_translation[object_name][0]
            y = self.robot_translation[object_name][1]

        spot_distance_pairs = []
        for ns, ns_pos in NEUTRAL_SPOTS.items():
            ns_x, ns_y = ns_pos
            spot_distance = math.sqrt((x - ns_x) ** 2 + (y - ns_y) ** 2)

            if not self.is_neutral_spot_occupied(ns_x, ns_y):
                spot_distance_pairs.append((ns, spot_distance))

        do_reverse = distance_type == NeutralSpotDistanceType.FURTHEST.value
        sorted_pairs = list(
            sorted(
                spot_distance_pairs,
                key=lambda pair: pair[1],
                reverse=do_reverse,
            ),
        )

        return sorted_pairs

    def move_object_to_neutral_spot(self, object_name: str, neutral_spot: str):
        """Move the robot to the specified neutral spot.

        Args:
            object_name (str): Name of the object (Ball or robot's name)
            neutral_spot (str): The spot the robot will be moved to
        """
        x, y = NEUTRAL_SPOTS[neutral_spot]
        if object_name == "ball":
            self.set_ball_position([x, y, BALL_DEPTH])
        else:
            self.set_robot_position(object_name, [x, y, OBJECT_DEPTH])
            self.set_robot_rotation(
                object_name, ROBOT_INITIAL_ROTATION[object_name]
            )

    def emit_data(self, data: str):
        """Send packet via emitter

        Args:
            data (str): the data to be sent
        """
        self.emitter.send(data)

    def draw_team_names(self, team_name_blue: str, team_name_yellow: str):
        """Visualize (draw) the names of the teams.

        Args:
            team_name_blue (str): name of the blue team
            team_name_yellow (str): name of the yellow team
        """
        self.setLabel(
            LabelIDs.BLUE_TEAM.value,
            team_name_blue,
            0.92 - (len(team_name_blue) * 0.01),  # X position
            0.05,  # Y position
            0.1,  # Size
            0x0000FF,  # Color
            0.0,  # Transparency
            "Tahoma",  # Font
        )

        self.setLabel(
            LabelIDs.YELLOW_TEAM.value,
            team_name_yellow,
            0.05,  # X position
            0.05,  # Y position
            0.1,  # Size
            0xFFFF00,  # Color
            0.0,  # Transparency
            "Tahoma",  # Font
        )

    def draw_scores(self, blue: int, yellow: int):
        """Visualize (draw) the provide scores for both the blue and
        the yellow teams.

        Args:
            blue (int): score of the blue team
            yellow (int): score of the yellow team
        """
        self.setLabel(
            LabelIDs.BLUE_SCORE.value,
            str(blue),
            0.92,  # X position
            0.01,  # Y position
            0.1,  # Size
            0x0000FF,  # Color
            0.0,  # Transparency
            "Tahoma",  # Font
        )

        self.setLabel(
            LabelIDs.YELLOW_SCORE.value,
            str(yellow),
            0.05,  # X position
            0.01,  # Y position
            0.1,  # Size
            0xFFFF00,  # Color
            0.0,  # Transparency
            "Tahoma",  # Font
        )

    def draw_time(self, time: int):
        """Visualize (draw) the current match time

        Args:
            time (int): the current match time
        """
        self.setLabel(
            LabelIDs.TIME.value,
            time_to_string(time),
            0.45,
            0.01,
            0.1,
            0x000000,
            0.0,
            "Arial",
        )

    def draw_event_messages(self, messages: List[str]):
        """Visualize (draw) the event messages from queue

        Args:
            messages: List of string messages to be drawn
        """
        if messages:
            self.setLabel(
                LabelIDs.EVENT_MESSAGES.value,
                "\n".join(messages),
                0.01,
                0.95 - ((len(messages) - 1) * 0.025),
                0.05,
                0xFFFFFF,
                0.0,
                "Tahoma",
            )

    def draw_goal_sign(self, transparency: float = 0.0):
        """Visualize (draw) a GOAL! sign after goal gets scored.

        Args:
            transparency (float): the transparecny of the text, with 0 meaning
                no transparency and 1 meaning total transparency (the text will
                not be visible).
        """
        self.setLabel(
            LabelIDs.GOAL.value,
            "GOAL!",
            0.30,
            0.40,
            0.4,
            0xFF0000,
            transparency,
            "Verdana",
        )

    def hide_goal_sign(self):
        """Hide the GOAL! once the game is again in progress."""
        self.setLabel(
            LabelIDs.GOAL.value,
            "",
            0.30,
            0.40,
            0.4,
            0xFF0000,
            1.0,
            "Verdana",
        )
