from controller import Supervisor
import struct

MATCH_TIME = 10 * 60  # 10 minutes
GOAL_X_LIMIT = 0.745
TIME_STEP = 64
ROBOT_NAMES = ["B1", "B2", "B3", "Y1", "Y2", "Y3"]
N_ROBOTS = len(ROBOT_NAMES)
ROBOT_INITIAL_TRANSLATION = {"B1": [0.3, 0.03817, 0.2],
                             "B2": [0.3, 0.03817, -0.2],
                             "B3": [0.75, 0.03817, 0],
                             "Y1": [-0.3, 0.03817, 0.2],
                             "Y2": [-0.3, 0.03817, -0.2],
                             "Y3": [-0.75, 0.03817, 0]}

ROBOT_INITIAL_ROTATION = {"B1": [0, 1, 0, 1.57],
                          "B2": [0, 1, 0, 1.57],
                          "B3": [0, 1, 0, 3.14],
                          "Y1": [0, 1, 0, 1.57],
                          "Y2": [0, 1, 0, 1.57],
                          "Y3": [0, 1, 0, 3.14]}

BALL_INITIAL_TRANSLATION = [0, 0, 0]


class RCJSoccerReferee(Supervisor):

    def __init__(self, match_time: int,
                 post_goal_wait_time: int = 3):

        super().__init__()

        self.match_time = match_time
        self.post_goal_wait_time = post_goal_wait_time

        self.time = match_time

        self.emitter = self.getEmitter("emitter")

        self.robot_translation = ROBOT_INITIAL_TRANSLATION.copy()
        self.robot_rotation = ROBOT_INITIAL_ROTATION.copy()

        self.robot_translation_fields = {}
        self.robot_rotation_fields = {}

        for robot in ROBOT_NAMES:
            robot_node = self.getFromDef(robot)
            field = robot_node.getField('translation')

            self.robot_translation_fields[robot] = field

            field = robot_node.getField('rotation')
            self.robot_rotation_fields[robot] = field

        self.ball = self.getFromDef("BALL")
        self.ball_translation_field = self.ball.getField("translation")

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

    def draw_scores(self, blue: int, yellow: int):
        """
        Visualize (draw) the provide scores for both the blue and the yellow
        teams.

        Args:
            blue (int): score of the blue team
            yello (int): score of the yellow team

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

    def _pack_packet(self,
                     robot_rotation: dict,
                     robot_translation: dict,
                     ball_translation: list):
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

        ball_translation_field = self.ball.getField("translation")
        ball_translation_field.setSFVec3f(BALL_INITIAL_TRANSLATION)

        self.ball.setVelocity([0, 0, 0, 0, 0, 0])

        # reset the robot positions
        for robot in ROBOT_NAMES:
            self.getFromDef(robot).setVelocity([0, 0, 0, 0, 0, 0])

            tr_field = self.getFromDef(robot).getField('translation')
            tr_field.setSFVec3f(ROBOT_INITIAL_TRANSLATION[robot])

            rot_field = self.getFromDef(robot).getField('rotation')
            rot_field.setSFRotation(ROBOT_INITIAL_ROTATION[robot])

    def tick(self):
        self.time -= TIME_STEP / 1000.0
        if self.time < 0:
            self.time = self.match_time

        self.draw_time(self.time)

        # If we are currently not currently in the post-goal waiting period,
        # check if a goal took place, setup the waiting period and move the
        # robots to proper positions afterwards.
        if self.ball_reset_timer == 0:

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

        else:
            self.ball_reset_timer -= TIME_STEP / 1000.0
            # If the post-goal waiting period is over, reset the robots to
            # their starting positions
            if self.ball_reset_timer <= 0:
                self.reset_positions()
                self.ball_reset_timer = 0


referee = RCJSoccerReferee(match_time=MATCH_TIME)

while referee.step(TIME_STEP) != -1:
    referee.emit_positions()

    referee.tick()
