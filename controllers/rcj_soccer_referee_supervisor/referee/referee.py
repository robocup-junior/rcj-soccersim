from referee.consts import (
    GOAL_X_LIMIT,
    TIME_STEP,
    ROBOT_NAMES
)
from referee.supervisor import RCJSoccerSupervisor


class RCJSoccerReferee(RCJSoccerSupervisor):
    def check_robots_in_penalty_area(self):
        """Check whether robots are violating rule not to stay in
        penalty area for longer period of time"""
        # TODO: decide if this rule will be applied and then implement it
        pass

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
                print(f'Robot {robot}: Lack of progress')
                self.reset_robot_position(robot)

        bpos = self.ball_translation.copy()
        self.progress_chck['ball'].track(bpos)
        if not self.progress_chck['ball'].is_progress('ball'):
            print('Ball: Lack of progress')
            self.reset_ball_position()

    def check_goal(self):
        """Check if goal is scored"""
        # ball in the blue goal
        if self.ball_translation[0] > GOAL_X_LIMIT:
            self.score_yellow += 1
            self.draw_scores(self.score_blue, self.score_yellow)
            self.ball_reset_timer = self.post_goal_wait_time

        # ball in the yellow goal
        elif self.ball_translation[0] < -GOAL_X_LIMIT:
            self.score_blue += 1
            self.draw_scores(self.score_blue, self.score_yellow)
            self.ball_reset_timer = self.post_goal_wait_time

    def tick(self) -> bool:
        self.time -= TIME_STEP / 1000.0
        if self.time < 0:
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

        return True
