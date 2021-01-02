# rcj_soccer_player controller - ROBOT Y2

###### REQUIRED in order to import abstract robot class
import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP
######

# Feel free to import built-in libraries
import math

# You can also import scripts that you put into the folder with controller
import utils


class MyRobot(RCJSoccerRobot):
    def run(self):
        while self.robot.step(TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()

                # Get the position of our robot
                robot_pos = data[self.name]
                # Get the position of the ball
                ball_pos = data['ball']

                # Get angle between the robot and the ball
                # and between the robot and the north
                ball_angle, robot_angle = self.get_angles(ball_pos, robot_pos)

                # Compute the speed for motors
                left_speed, right_speed = utils.compute_motor_speeds(ball_angle)

                # Set the speed to motors
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)


my_robot = MyRobot()
my_robot.run()
