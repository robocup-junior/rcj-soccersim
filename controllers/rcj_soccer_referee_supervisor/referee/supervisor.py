import struct
import random
from pathlib import Path

from controller import Supervisor
from referee.progress_checker import ProgressChecker
from referee.penalty_area_checker import PenaltyAreaChecker
from referee.consts import (
    ROBOT_NAMES,
    ROBOT_INITIAL_TRANSLATION,
    ROBOT_INITIAL_ROTATION,
    BALL_INITIAL_TRANSLATION,
)
from referee.json_logger import JSONLogger


class RCJSoccerSupervisor(Supervisor):
    def __init__(
        self,
        match_time: int,
        progress_check_steps: int,
        progress_check_threshold: int,
        ball_progress_check_steps: int,
        ball_progress_check_threshold: int,
        reflog_path: Path,
        team_name_blue: str,
        team_name_yellow: str,
        penalty_area_allowed_time: int,
        penalty_area_reset_after: int,
        post_goal_wait_time: int = 3,
        add_noise_to_initial_position: bool = True
    ):

        super().__init__()

        self.match_time = match_time
        self.post_goal_wait_time = post_goal_wait_time
        self.add_noise_to_initial_position = add_noise_to_initial_position

        self.time = match_time

        self.log = JSONLogger(reflog_path)
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

    def draw_scores(self, blue: int, yellow: int):
        """
        Visualize (draw) the provide scores for both the blue and the yellow
        teams.

        Args:
            blue (int): score of the blue team
            yellow (int): score of the yellow team
        """

        self.setLabel(0, str(blue),
                      # X and Y positions
                      0.92, 0.01,
                      # Size and color
                      0.1, 0x0000ff,
                      # Transparency and Font
                      0.0, "Tahoma")

        self.setLabel(1, str(yellow),
                      # X and Y positions
                      0.05, 0.01,
                      # Size and color
                      0.1, 0xffff00,
                      # Transparency and Font
                      0.0, "Tahoma")

    def draw_time(self, time):
        """
        Visualize (draw) the current match time

        Args:
            time (int): the current match time
        """

        time_str = "%02d:%02d" % (time // 60, time % 60)
        self.setLabel(2, time_str, 0.45, 0.01, 0.1, 0x000000, 0.0, "Arial")

    def _pack_packet(
        self,
        robot_rotation: dict,
        robot_translation: dict,
        ball_translation: list,
    ):
        """
        Take the positions and rotations of the robots and the ball and pack
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

    def reset_robot_position(self, robot):
        self.getFromDef(robot).setVelocity([0, 0, 0, 0, 0, 0])

        translation = ROBOT_INITIAL_TRANSLATION[robot].copy()
        if self.add_noise_to_initial_position:
            translation[0] += (random.random() - 0.5) / 5
            translation[2] += (random.random() - 0.5) / 5

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
