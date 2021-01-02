import random
from typing import Optional
from referee.consts import (
    GOAL_X_LIMIT,
    TIME_STEP,
    ROBOT_NAMES,
    GameEvents,
    Team
)
from referee.supervisor import RCJSoccerSupervisor


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
                self.log.event(
                    supervisor=self,
                    type=GameEvents.INSIDE_PENALTY_FOR_TOO_LONG.value,
                    msg=f"Robot {robot}: Inside penalty for too long",
                    payload={
                        "type": "robot",
                        "robot": robot,
                    }
                )
                # TODO: move the robot to the FURTHEST unoccupied neutral spot
                self.reset_robot_position(robot)

    def check_progress(self):
        """
        Check that the robots, as well as the ball, have made enough progress
        in their respective time intervals. If they did not, call "Lack of
        Progress".
        """
        for robot in ROBOT_NAMES:
            pos = self.robot_translation[robot]
            self.progress_chck[robot].track(pos)

            if not self.progress_chck[robot].is_progress(robot):
                self.log.event(
                    supervisor=self,
                    type=GameEvents.LACK_OF_PROGRESS.value,
                    msg=f"Robot {robot}: Lack of progress",
                    payload={
                        "type": "robot",
                        "robot": robot,
                    }
                )
                self.reset_robot_position(robot)

        bpos = self.ball_translation.copy()
        self.progress_chck['ball'].track(bpos)
        if not self.progress_chck['ball'].is_progress('ball'):
            self.log.event(
                supervisor=self,
                type=GameEvents.LACK_OF_PROGRESS.value,
                msg="Ball: Lack of progress",
                payload={
                    "type": "ball"
                }
            )
            self.reset_ball_position()

    def check_goal(self):
        """Check if goal is scored"""

        team_goal = None
        team_kickoff = None

        # ball in the blue goal
        if self.ball_translation[0] > GOAL_X_LIMIT:
            self.score_yellow += 1

            team_goal = self.team_name_yellow
            team_kickoff = Team.BLUE

        # ball in the yellow goal
        elif self.ball_translation[0] < -GOAL_X_LIMIT:
            self.score_blue += 1

            team_goal = self.team_name_blue
            team_kickoff = Team.YELLOW

        # If a goal was scored, redraw the scores, set the timers, log what
        # happened and set the proper team for kickoff.
        if team_goal and team_kickoff:
            self.draw_scores(self.score_blue, self.score_yellow)
            self.ball_reset_timer = self.post_goal_wait_time

            self.log.event(
                supervisor=self,
                type=GameEvents.GOAL.value,
                team=team_goal,
                msg=f"A goal was scored by {team_goal}",
                payload={
                    "score_yellow": self.score_yellow,
                    "score_blue": self.score_blue,
                }
            )

            # Let the team that did not score the goal have a kickoff.
            self.kickoff(team_kickoff)

    def kickoff(self, team: Optional[Team] = None):
        """Set up the kickoff by putting one of the robots of the team that is
        kicking off closer to the center point

        Args:
            team (Team): The team that is kicking off. If the team is not
                specified, it will be chosen randomly.
        """
        if team not in (Team.BLUE, Team.YELLOW, None):
            raise ValueError(f"Unexpected team name {team}")

        if not team:
            team = Team.BLUE if random.random() > 0.5 else Team.YELLOW

        robot_name = self.reset_team_for_kickoff(team)

        self.log.event(
            supervisor=self,
            type=GameEvents.KICKOFF.value,
            robot_name=robot_name,
            msg=f"Robot {robot_name} is kicking off."
        )

    def tick(self) -> bool:
        # On the very first tick, note that the match has started
        if self.time == self.match_time:
            self.log.event(
                supervisor=self,
                type=GameEvents.MATCH_START.value,
                msg=f"The match ({self.match_time}s) has started",
                payload={
                    "score_yellow": self.score_yellow,
                    "score_blue": self.score_blue,
                    "total_match_time": self.match_time
                }
            )

        self.time -= TIME_STEP / 1000.0

        # On the very last tick, note that the match has finished
        if self.time < 0:
            self.log.event(
                supervisor=self,
                type=GameEvents.MATCH_FINISH.value,
                msg=f"The match time {self.match_time}s is over",
                payload={
                    "score_yellow": self.score_yellow,
                    "score_blue": self.score_blue
                }
            )

            return False

        self.draw_time(self.time)

        # If we are currently not in the post-goal waiting period,
        # check if a goal took place, setup the waiting period and move the
        # robots to proper positions afterwards.
        if self.ball_reset_timer == 0:
            self.check_goal()
            self.check_progress()
            self.check_robots_in_penalty_area()
        else:
            self.ball_reset_timer -= TIME_STEP / 1000.0
            # If the post-goal waiting period is over, reset the robots to
            # their starting positions
            if self.ball_reset_timer <= 0:
                self.reset_positions()
                self.ball_reset_timer = 0
                self.kickoff()

        return True
