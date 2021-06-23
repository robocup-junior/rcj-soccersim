from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP

TIME_STEP = 64


class MyBallPassingRobot2(RCJSoccerRobot):
    def run(self):
        while self.robot.step(TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()

                # Get the position of our robot
                robot_pos = data[self.name]
                # Get the position of the ball
                ball_pos = data['ball']

                # YOUR CODE HERE

                left_speed = 1 * 4
                right_speed = 1 * -4

                # Set the speed to motors
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)
