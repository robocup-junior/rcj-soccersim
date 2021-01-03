import struct
import random

from typing import List, Tuple

from controller import Supervisor
from referee.progress_checker import ProgressChecker
from referee.penalty_area_checker import PenaltyAreaChecker
from referee.consts import (
    ROBOT_NAMES,
    ROBOT_INITIAL_TRANSLATION,
    ROBOT_INITIAL_ROTATION,
    BALL_INITIAL_TRANSLATION,
    KICKOFF_TRANSLATION,
    LabelIDs,
    MAX_EVENT_MESSAGES_IN_QUEUE,
)
from referee.eventer import Eventer
from referee.event_handlers import EventHandler
from referee.utils import time_to_string


class RCJSoccerSupervisor(Supervisor):
    def __init__(
        self,
        match_time: int,
        progress_check_steps: int,
        progress_check_threshold: int,
        ball_progress_check_steps: int,
        ball_progress_check_threshold: int,
        team_name_blue: str,
        team_name_yellow: str,
        penalty_area_allowed_time: int,
        penalty_area_reset_after: int,
        post_goal_wait_time: int = 3,
        initial_position_noise: float = 0.15
    ):

        super().__init__()

        self.match_time = match_time
        self.post_goal_wait_time = post_goal_wait_time
        self.initial_position_noise = initial_position_noise

        self.time = match_time

        # Event message queue to be drawn
        # List of Tuples of int (time) and string (message)
        self.event_messages_to_draw: List[Tuple[int, str]] = []

        self.eventer = Eventer()

        self.team_name_blue = team_name_blue
        self.team_name_yellow = team_name_yellow

        self.emitter = self.getEmitter("emitter")

        self.robot_translation = ROBOT_INITIAL_TRANSLATION.copy()
        self.robot_rotation = ROBOT_INITIAL_ROTATION.copy()

        self.robot_translation_fields = {}
        self.robot_rotation_fields = {}

        self.robot_in_penalty_counter = {}

        self.progress_chck = {}
        self.penalty_area_chck = {}

        for robot in ROBOT_NAMES:
            robot_node = self.getFromDef(robot)
            field = robot_node.getField('translation')

            self.robot_translation_fields[robot] = field

            field = robot_node.getField('rotation')
            self.robot_rotation_fields[robot] = field

            self.robot_in_penalty_counter[robot] = 0

            self.progress_chck[robot] = ProgressChecker(
                progress_check_steps,
                progress_check_threshold
            )

            self.penalty_area_chck[robot] = PenaltyAreaChecker(
                penalty_area_allowed_time,
                penalty_area_reset_after,
            )

        self.ball = self.getFromDef("BALL")
        self.ball_translation_field = self.ball.getField("translation")

        bpc = ProgressChecker(ball_progress_check_steps,
                              ball_progress_check_threshold)
        self.progress_chck['ball'] = bpc

        self.reset_positions()

        self._update_positions()

        self.ball_reset_timer = 0
        self.score_blue = self.score_yellow = 0
        # The team that ought to have the kickoff at the next restart
        self.team_to_kickoff = None

        self.draw_scores(self.score_blue, self.score_yellow)

    def _update_positions(self):
        self.ball_translation = self.ball_translation_field.getSFVec3f()

        for robot in ROBOT_NAMES:
            t = self.robot_translation_fields[robot].getSFVec3f()
            self.robot_translation[robot] = t

            r = self.robot_rotation_fields[robot].getSFRotation()
            self.robot_rotation[robot] = r

            # TODO: update self.robot_in_penalty_counter if the robot
            #       is located in penalty area

    def add_event_subscriber(self, subscriber: EventHandler):
        """Add new event subscriber.

        Args:
            subscriber (EventHandler): Instance inheriting EventHandler
        """
        self.eventer.subscribe(subscriber)

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
            0x0000ff,  # Color
            0.0,  # Transparency
            "Tahoma",  # Font
        )

        self.setLabel(
            LabelIDs.YELLOW_SCORE.value,
            str(yellow),
            0.05,  # X position
            0.01,  # Y position
            0.1,  # Size
            0xffff00,  # Color
            0.0,  # Transparency
            "Tahoma"  # Font
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

    def draw_event_messages(self):
        """Visualize (draw) the event messages from queue"""
        messages = []
        for time, msg in self.event_messages_to_draw:
            messages.append("{} - {}".format(time_to_string(time), msg))

        if messages:
            self.setLabel(
                LabelIDs.EVENT_MESSAGES.value,
                "\n".join(messages),
                0.01,
                0.95 - ((len(messages)-1) * 0.025),
                0.05,
                0xffffff,
                0.0,
                "Tahoma",
            )

    def add_event_message_to_queue(self, message: str):
        if len(self.event_messages_to_draw) >= MAX_EVENT_MESSAGES_IN_QUEUE:
            self.event_messages_to_draw.pop(0)

        self.event_messages_to_draw.append((self.time, message))

    def _pack_packet(
        self,
        robot_rotation: dict,
        robot_translation: dict,
        ball_translation: list,
    ):
        """ Take the positions and rotations of the robots and the ball and pack
        them into a single packet that can be send to all robots in the game.

        Args:
            robot_rotation (dict): a mapping between the robot name and its
                                   rotation
            robot_translation (dict): a mapping between the robot name and its
                                      position on the field
            ball_translation (list): the position of the ball on the field

        Returns:
            str: the packed packet.

        """

        assert len(robot_translation) == len(robot_rotation)

        # X, Z and rotation for each robot
        # plus X and Z for ball
        struct_fmt = 'ddd' * len(robot_translation) + 'dd'

        data = []
        for robot in ROBOT_NAMES:
            data.append(robot_translation[robot][0])  # X
            data.append(robot_translation[robot][2])  # Z

            if robot_rotation[robot][1] > 0:
                data.append(robot_rotation[robot][3])
            else:
                data.append(-robot_rotation[robot][3])

        data.append(ball_translation[0])
        data.append(ball_translation[2])

        return struct.pack(struct_fmt, *data)

    def emit_positions(self):
        self._update_positions()

        packet = self._pack_packet(self.robot_rotation,
                                   self.robot_translation,
                                   self.ball_translation)

        self.emitter.send(packet)

    def reset_positions(self):
        """
        Reset the positions of the ball as well as the robots to the initial
        position.
        """

        self.reset_ball_position()

        # reset the robot positions
        for robot in ROBOT_NAMES:
            self.reset_robot_position(robot)

    def reset_ball_position(self):
        ball_translation_field = self.ball.getField("translation")
        ball_translation_field.setSFVec3f(BALL_INITIAL_TRANSLATION)

        self.ball.setVelocity([0, 0, 0, 0, 0, 0])
        self.progress_chck['ball'].reset()

    def _add_initial_position_noise(
        self,
        translation: List[float]
    ) -> List[float]:

        level = self.initial_position_noise
        translation[0] += (random.random() - 0.5) * level
        translation[2] += (random.random() - 0.5) * level
        return translation

    def reset_robot_position(self, robot):
        self.getFromDef(robot).setVelocity([0, 0, 0, 0, 0, 0])

        translation = ROBOT_INITIAL_TRANSLATION[robot].copy()
        translation = self._add_initial_position_noise(translation)

        tr_field = self.getFromDef(robot).getField('translation')
        tr_field.setSFVec3f(translation)

        rot_field = self.getFromDef(robot).getField('rotation')
        rot_field.setSFRotation(ROBOT_INITIAL_ROTATION[robot])

        # Ensure the progress checker does not count this "jump"
        self.progress_chck[robot].reset()

        self.penalty_area_chck[robot].reset()

    def robot_name_to_team_name(self, robot_name: str) -> str:
        if robot_name.startswith('Y'):
            return self.team_name_yellow
        elif robot_name.startswith('B'):
            return self.team_name_blue
        else:
            raise ValueError(f"Unrecognized robot's name {robot_name}")

    def reset_team_for_kickoff(self, team: str):
        """
        Given a team name ('B' or 'Y'), set the position of the third robot on
        the team to "kick off" (inside the center circle).

        Returns:
            str: Name of the robot that is kicking off.
        """
        # Always kickoff with the third robot
        robot = f'{team}3'

        tr_field = self.getFromDef(robot).getField('translation')
        tr_field.setSFVec3f(KICKOFF_TRANSLATION[team])

        rot_field = self.getFromDef(robot).getField('rotation')
        rot_field.setSFRotation(ROBOT_INITIAL_ROTATION[robot])

        return robot
