import random
from typing import Optional
from referee.consts import (
    TIME_STEP,
    LACK_OF_PROGRESS_NUMBER_OF_NEUTRAL_SPOTS,
    ROBOT_NAMES,
    GameEvents,
    Team,
    NeutralSpotDistanceType,
)
from referee.supervisor import RCJSoccerSupervisor
from referee.utils import (
    is_in_blue_goal,
    is_in_yellow_goal,
    is_outside,
)


class RCJSoccerReferee(RCJSoccerSupervisor):
    def check_robots_in_penalty_area(self):
        """
        Check whether robots are violating rule not to stay in
        penalty area for longer period of time
        """
        for robot in ROBOT_NAMES:
            pos = self.robot_translation[robot]
            self.penalty_area_chck[robot].track(pos, self.time)

            if self.penalty_area_chck[robot].is_violating():
                self.eventer.event(
                    supervisor=self,
                    type=GameEvents.INSIDE_PENALTY_FOR_TOO_LONG.value,
                    payload={
                        "type": "robot",
                        "robot_name": robot,
                    },
                )
                furthest_spots = self.get_unoccupied_neutral_spots_sorted(
                    NeutralSpotDistanceType.FURTHEST.value,
                    robot,
                )
                if furthest_spots:
                    neutral_spot = furthest_spots[0][0]
                    self.move_object_to_neutral_spot(robot, neutral_spot)
                    self.reset_checkers(robot)

    def check_progress(self):
        """
        Check that the robots, as well as the ball, have made enough progress
        in their respective time intervals. If they did not, call "Lack of
        Progress".
        """
        for robot in ROBOT_NAMES:
            pos = self.robot_translation[robot]
            self.progress_chck[robot].track(pos)

            x, z = pos[0], pos[2]
            if is_outside(x, z) or not self.progress_chck[robot].is_progress(robot):
                self.eventer.event(
                    supervisor=self,
                    type=GameEvents.LACK_OF_PROGRESS.value,
                    payload={
                        "type": "robot",
                        "robot_name": robot,
                    }
                )
                nearest_spots = self.get_unoccupied_neutral_spots_sorted(
                    NeutralSpotDistanceType.NEAREST.value,
                    robot,
                )

                if nearest_spots:
                    neutral_spot = random.choice(
                        nearest_spots[:LACK_OF_PROGRESS_NUMBER_OF_NEUTRAL_SPOTS],
                    )
                    self.move_object_to_neutral_spot(robot, neutral_spot[0])
                    self.reset_checkers(robot)

        bpos = self.ball_translation.copy()
        self.progress_chck['ball'].track(bpos)
        bx, bz = bpos[0], bpos[2]
        if is_outside(bx, bz) or not self.progress_chck['ball'].is_progress('ball'):
            self.eventer.event(
                supervisor=self,
                type=GameEvents.LACK_OF_PROGRESS.value,
                payload={
                    "type": "ball"
                },
            )
            nearest_spots = self.get_unoccupied_neutral_spots_sorted(
                NeutralSpotDistanceType.NEAREST.value,
                "ball",
            )

            if nearest_spots:
                neutral_spot = random.choice(
                    nearest_spots[:LACK_OF_PROGRESS_NUMBER_OF_NEUTRAL_SPOTS],
                )

                self.move_object_to_neutral_spot("ball", neutral_spot[0])
                self.reset_checkers("ball")

    def check_goal(self):
        """Check if goal is scored"""

        team_goal = None
        team_kickoff = None

        ball_x, ball_z = self.ball_translation[0], self.ball_translation[2]

        # ball in the blue goal
        if is_in_blue_goal(ball_x, ball_z):
            self.score_yellow += 1

            team_goal = self.team_name_yellow
            team_kickoff = Team.BLUE.value

        # ball in the yellow goal
        elif is_in_yellow_goal(ball_x, ball_z):
            self.score_blue += 1

            team_goal = self.team_name_blue
            team_kickoff = Team.YELLOW.value

        # If a goal was scored, redraw the scores, set the timers, log what
        # happened and set the proper team for kickoff.
        if team_goal and team_kickoff:
            self.draw_scores(self.score_blue, self.score_yellow)
            self.ball_reset_timer = self.post_goal_wait_time

            self.eventer.event(
                supervisor=self,
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
            supervisor=self,
            type=GameEvents.KICKOFF.value,
            payload={
                "robot_name": robot_name,
                "team_name": team,
            },
        )

    def tick(self) -> bool:
        # On the very first tick, note that the match has started
        if self.time == self.match_time:
            self.eventer.event(
                supervisor=self,
                type=GameEvents.MATCH_START.value,
                payload={
                    "score_yellow": self.score_yellow,
                    "score_blue": self.score_blue,
                    "total_match_time": self.match_time,
                },
            )

        self.time -= TIME_STEP / 1000.0

        # On the very last tick, note that the match has finished
        if self.time < 0:
            self.eventer.event(
                supervisor=self,
                type=GameEvents.MATCH_FINISH.value,
                payload={
                    "total_match_time": self.match_time,
                    "score_yellow": self.score_yellow,
                    "score_blue": self.score_blue,
                },
            )

            return False

        self.draw_time(self.time)
        self.draw_event_messages()

        # If we are currently not in the post-goal waiting period,
        # check if a goal took place, setup the waiting period and move the
        # robots to proper positions afterwards.
        if self.ball_reset_timer == 0:
            self.check_goal()
            self.check_progress()
            self.check_robots_in_penalty_area()
        else:
            self.ball_reset_timer -= TIME_STEP / 1000.0
            self.draw_goal_sign()

            # If the post-goal waiting period is over, reset the robots to
            # their starting positions
            if self.ball_reset_timer <= 0:
                self.reset_positions()
                self.ball_reset_timer = 0
                self.hide_goal_sign()
                self.kickoff(self.team_to_kickoff)

        # WORKAROUND: The proper way of moving the ball is to set its position
        # and call resetPhysics on the ball. However, the ball has small velocity
        # and is moving a bit.
        # See https://github.com/cyberbotics/webots/issues/2899
        if self.ball_stop > 0:
            if self.ball_stop == 1:
                self.reset_ball_velocity()
            self.ball_stop -= 1

        return True
