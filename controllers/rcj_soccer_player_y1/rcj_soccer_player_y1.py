# rcj_soccer_player controller - ROBOT Y1

###### REQUIRED in order to import abstract robot class
import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP
######

# Feel free to import built-in libraries here
import math


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

                # If the robot has the ball right in front of it, go forward,
                # rotate otherwise
                if ball_angle >= 345 or ball_angle <= 15:
                    left_speed = -5
                    right_speed = -5
                else:
                    multiplier = -1 if ball_angle < 180 else 1
                    left_speed = multiplier * 4
                    right_speed = multiplier * -4

                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)


my_robot = MyRobot()
my_robot.run()
