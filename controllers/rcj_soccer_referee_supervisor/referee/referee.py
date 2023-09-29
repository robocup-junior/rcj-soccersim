import json
import random
from typing import List, Optional, Tuple

from controller import Supervisor

from referee.consts import (
    BALL_INITIAL_TRANSLATION,
    KICKOFF_TRANSLATION,
    LACK_OF_PROGRESS_NUMBER_OF_NEUTRAL_SPOTS,
    MAX_EVENT_MESSAGES_IN_QUEUE,
    ROBOT_INITIAL_ROTATION,
    ROBOT_INITIAL_TRANSLATION,
    ROBOT_NAMES,
    TIME_STEP,
)
from referee.enums import GameEvents, NeutralSpotDistanceType, Team
from referee.event_handlers import EventHandler
from referee.eventer import Eventer
from referee.penalty_area_checker import PenaltyAreaChecker
from referee.progress_checker import ProgressChecker
from referee.utils import (
    is_in_blue_goal,
    is_in_yellow_goal,
    is_outside,
    time_to_string,
)


class RCJSoccerReferee:
    def __init__(
        self,
        supervisor: Supervisor,
        match_time: int,
        match_id: int,
        half_id: int,
        progress_check_steps: int,
        progress_check_threshold: int,
        ball_progress_check_steps: int,
        ball_progress_check_threshold: int,
        team_name_blue: str,
        team_name_yellow: str,
        initial_score_blue: int,
        initial_score_yellow: int,
        penalty_area_allowed_time: int,
        penalty_area_reset_after: int,
        post_goal_wait_time: int = 3,
        initial_position_noise: float = 0.15,
    ):
        self.sv = supervisor
        self.match_time = match_time
        self.time = match_time
        self.match_id = match_id
        self.half_id = half_id
        self.team_name_blue = team_name_blue
        self.team_name_yellow = team_name_yellow
        self.score_blue = initial_score_blue
        self.score_yellow = initial_score_yellow
        self.post_goal_wait_time = post_goal_wait_time
        self.initial_position_noise = initial_position_noise

        self.ball_reset_timer = 0
        self.ball_stop = 2

        self.robot_in_penalty_counter = {}
        self.progress_check = {}
        self.penalty_area_check = {}
        for robot in ROBOT_NAMES:
            self.progress_check[robot] = ProgressChecker(
                progress_check_steps, progress_check_threshold
            )

            self.penalty_area_check[robot] = PenaltyAreaChecker(
                penalty_area_allowed_time,
                penalty_area_reset_after,
            )

            self.robot_in_penalty_counter[robot] = 0

        self.progress_check["ball"] = ProgressChecker(
            ball_progress_check_steps, ball_progress_check_threshold
        )

        self.eventer = Eventer()
        # Event message queue to be drawn from
        # List of Tuples of int (time) and string (message)
        self.event_messages_to_draw: List[Tuple[int, str]] = []

        self.reset_positions()
        self.sv.update_positions()
        self.sv.draw_team_names(self.team_name_blue, self.team_name_yellow)
        self.sv.draw_scores(self.score_blue, self.score_yellow)

    def _pack_data(self) -> str:
        """Pack data into json string.

        Returns:
            str: json data encoded into string.
        """
        # Add Notification if the goal is scored and we are
        # waiting for kickoff. The value is True or False
        waiting_for_kickoff = self.ball_reset_timer > 0

        data = {"waiting_for_kickoff": waiting_for_kickoff}
        return json.dumps(data)

    def _add_initial_position_noise(
        self, translation: List[float]
    ) -> List[float]:
        """Return translation with noise added to x and z coordinates.

        Args:
            translation (list): x, y and z coordinates

        Returns:
            list: new x, y, and z coordinates
        """
        level = self.initial_position_noise
        return [
            translation[0] + (random.random() - 0.5) * level,
            translation[1] + (random.random() - 0.5) * level,
            translation[2],
        ]

    def add_event_subscriber(self, subscriber: EventHandler):
        """Add new event subscriber.

        Args:
            subscriber (EventHandler): Instance inheriting EventHandler
        """
        self.eventer.subscribe(subscriber)

    def add_event_message_to_queue(self, message: str):
        """Add new message to the message queue.

        Args:
            message (str): Message to be added to the queue.
        """
        if len(self.event_messages_to_draw) >= MAX_EVENT_MESSAGES_IN_QUEUE:
            self.event_messages_to_draw.pop(0)

        self.event_messages_to_draw.append((self.time, message))

    def process_and_draw_event_messages(self):
        """Process and draw event messages from the queue"""
        messages = []
        for time, msg in self.event_messages_to_draw:
            messages.append(f"{time_to_string(time)} - {msg}")

        self.sv.draw_event_messages(messages)

    def reset_checkers(self, object_name: str):
        """Reset rule checkers for the specified object.

        Args:
            object_name (str): Either "ball" or the robot's name.
        """
        self.progress_check[object_name].reset()
        if object_name != "ball":
            self.penalty_area_check[object_name].reset()

    def reset_ball_position(self):
        """Reset the position of the ball."""
        self.sv.set_ball_position(BALL_INITIAL_TRANSLATION)
        self.ball_stop = 2
        self.reset_checkers("ball")

    def reset_robot_position(self, robot_name: str):
        """Reset robot's position to the initial one.

        Args:
            robot_name (str): The robot to reset the position for
        """
        self.sv.reset_robot_velocity(robot_name)

        translation = ROBOT_INITIAL_TRANSLATION[robot_name].copy()
        translation = self._add_initial_position_noise(translation)

        self.sv.set_robot_position(robot_name, translation)
        self.sv.set_robot_rotation(
            robot_name, ROBOT_INITIAL_ROTATION[robot_name]
        )

        self.reset_checkers(robot_name)

    def reset_positions(self):
        """
        Reset the positions of the ball as well as the robots to the initial
        position.
        """
        self.reset_ball_position()

        # reset the robot positions
        for robot in ROBOT_NAMES:
            self.reset_robot_position(robot)

    def reset_team_for_kickoff(self, team: str) -> str:
        """
        Given a team name ('B' or 'Y'), set the position of the third robot on
        the team to "kick off" (inside the center circle).

        Args:
            team (str): 'B' for blue or 'Y' for yellow team

        Returns:
            str: Name of the robot that is kicking off.
        """
        # Always kickoff with the third robot
        robot = f"{team}3"

        self.sv.set_robot_position(robot, KICKOFF_TRANSLATION[team])
        self.sv.set_robot_rotation(robot, ROBOT_INITIAL_ROTATION[robot])

        return robot

    def check_robots_in_penalty_area(self):
        """
        Check whether robots are violating rule not to stay in
        penalty area for longer period of time
        """
        for robot in ROBOT_NAMES:
            pos = self.sv.get_robot_translation(robot)
            self.penalty_area_check[robot].track(pos, self.time)

            if self.penalty_area_check[robot].is_violating():
                self.eventer.event(
                    referee=self,
                    type=GameEvents.INSIDE_PENALTY_FOR_TOO_LONG.value,
                    payload={
                        "type": "robot",
                        "robot_name": robot,
                    },
                )
                furthest_spots = self.sv.get_unoccupied_neutral_spots_sorted(
                    NeutralSpotDistanceType.FURTHEST.value,
                    robot,
                )
                if furthest_spots:
                    neutral_spot = furthest_spots[0][0]
                    self.sv.move_object_to_neutral_spot(robot, neutral_spot)
                    self.reset_checkers(robot)

    def check_progress(self):
        """
        Check that the robots, as well as the ball, have made enough progress
        in their respective time intervals. If they did not, call "Lack of
        Progress".
        """
        for robot in ROBOT_NAMES:
            pos = self.sv.get_robot_translation(robot)
            self.progress_check[robot].track(pos)

            x, y = pos[0], pos[1]
            if (
                is_outside(x, y)
                or not self.progress_check[robot].is_progress()
            ):
                self.eventer.event(
                    referee=self,
                    type=GameEvents.LACK_OF_PROGRESS.value,
                    payload={
                        "type": "robot",
                        "robot_name": robot,
                    },
                )
                nearest_spots = self.sv.get_unoccupied_neutral_spots_sorted(
                    NeutralSpotDistanceType.NEAREST.value,
                    robot,
                )

                if nearest_spots:
                    neutral_spot = random.choice(
                        nearest_spots[
                            :LACK_OF_PROGRESS_NUMBER_OF_NEUTRAL_SPOTS
                        ],
                    )
                    self.sv.move_object_to_neutral_spot(robot, neutral_spot[0])

                self.reset_checkers(robot)

        bpos = self.sv.get_ball_translation()
        self.progress_check["ball"].track(bpos)
        bx, by = bpos[0], bpos[1]

        if is_outside(bx, by) or not self.progress_check["ball"].is_progress():
            self.eventer.event(
                referee=self,
                type=GameEvents.LACK_OF_PROGRESS.value,
                payload={"type": "ball"},
            )
            nearest_spots = self.sv.get_unoccupied_neutral_spots_sorted(
                NeutralSpotDistanceType.NEAREST.value,
                "ball",
            )

            if nearest_spots:
                neutral_spot = random.choice(
                    nearest_spots[
                        :LACK_OF_PROGRESS_NUMBER_OF_NEUTRAL_SPOTS
                    ],  # noqa
                )

                self.sv.move_object_to_neutral_spot("ball", neutral_spot[0])
                self.ball_stop = 2

            self.reset_checkers("ball")

    def check_goal(self):
        """Check if goal is scored"""

        team_goal = None
        team_kickoff = None

        ball_translation = self.sv.get_ball_translation()
        ball_x, ball_y = ball_translation[0], ball_translation[1]

        # ball in the blue goal
        if is_in_blue_goal(ball_x, ball_y):
            self.score_yellow += 1

            team_goal = self.team_name_yellow
            team_kickoff = Team.BLUE.value

        # ball in the yellow goal
        elif is_in_yellow_goal(ball_x, ball_y):
            self.score_blue += 1

            team_goal = self.team_name_blue
            team_kickoff = Team.YELLOW.value

        # If a goal was scored, redraw the scores, set the timers, log what
        # happened and set the proper team for kickoff.
        if team_goal and team_kickoff:
            self.sv.draw_scores(self.score_blue, self.score_yellow)
            self.ball_reset_timer = self.post_goal_wait_time

            self.eventer.event(
                referee=self,
                type=GameEvents.GOAL.value,
                payload={
                    "team_name": team_goal,
                    "score_yellow": self.score_yellow,
                    "score_blue": self.score_blue,
                },
            )

            # Let the team that did not score the goal have a kickoff.
            self.team_to_kickoff = team_kickoff

    def kickoff(self, team: Optional[str] = None):
        """Set up the kickoff by putting one of the robots of the team that is
        kicking off closer to the center point

        Args:
            team (str): The team that is kicking off. If the team is not
                specified, it will be chosen randomly.
        """
        if team not in (Team.BLUE.value, Team.YELLOW.value, None):
            raise ValueError(f"Unexpected team name {team}")

        seed = random.random()
        if not team:
            team = Team.BLUE.value if seed > 0.5 else Team.YELLOW.value

        robot_name = self.reset_team_for_kickoff(team)

        self.eventer.event(
            referee=self,
            type=GameEvents.KICKOFF.value,
            payload={
                "robot_name": robot_name,
                "team_name": team,
            },
        )

    def tick(self) -> bool:
        self.sv.check_reset_physics_counters()

        # On the very first tick, note that the match has started
        if self.time == self.match_time:
            self.eventer.event(
                referee=self,
                type=GameEvents.MATCH_START.value,
                payload={
                    "score_yellow": self.score_yellow,
                    "score_blue": self.score_blue,
                    "total_match_time": self.match_time,
                    "team_name_yellow": self.team_name_yellow,
                    "team_name_blue": self.team_name_blue,
                    "match_id": self.match_id,
                    "halftime": self.half_id,
                },
            )

        self.sv.update_positions()
        self.sv.emit_data(self._pack_data())
        self.time -= TIME_STEP / 1000.0

        # On the very last tick, note that the match has finished
        if self.time < 0:
            self.eventer.event(
                referee=self,
                type=GameEvents.MATCH_FINISH.value,
                payload={
                    "total_match_time": self.match_time,
                    "score_yellow": self.score_yellow,
                    "score_blue": self.score_blue,
                    "team_name_yellow": self.team_name_yellow,
                    "team_name_blue": self.team_name_blue,
                },
            )

            return False

        self.sv.draw_time(self.time)
        self.process_and_draw_event_messages()

        # If we are currently not in the post-goal waiting period,
        # check if a goal took place, setup the waiting period and move the
        # robots to proper positions afterwards.
        if self.ball_reset_timer == 0:
            self.check_goal()
            self.check_progress()
            self.check_robots_in_penalty_area()
        else:
            self.ball_reset_timer -= TIME_STEP / 1000.0
            self.sv.draw_goal_sign()

            # If the post-goal waiting period is over, reset the robots to
            # their starting positions
            if self.ball_reset_timer <= 0:
                self.reset_positions()
                self.ball_reset_timer = 0
                self.sv.hide_goal_sign()
                self.kickoff(self.team_to_kickoff)

        # WORKAROUND: The proper way of moving the ball is to set its position
        # and call resetPhysics on the ball. However, the ball has small
        # velocity and is moving a bit.
        # See https://github.com/cyberbotics/webots/issues/2899
        if self.ball_stop > 0:
            if self.ball_stop == 1:
                self.sv.reset_ball_velocity()
            self.ball_stop -= 1

        return True
