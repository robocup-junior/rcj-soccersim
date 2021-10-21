# rcj_soccer_player controller - ROBOT Y1

# Feel free to import built-in libraries
import math

# You can also import scripts that you put into the folder with controller
from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP
import utils


class MyRobot1(RCJSoccerRobot):
    def run(self):
        while self.robot.step(TIME_STEP) != -1:
            while self.robot.step(TIME_STEP) != -1:
                if self.is_new_data():
                    data = self.get_new_data()

                    while self.is_new_team_data():
                        team_data = self.get_new_team_data()
                        # Do something with team data

                    if self.is_new_ball_data():
                        ball_data = self.get_new_ball_data()
                    else:
                        # If the robot does not see the ball, stop motors
                        self.left_motor.setVelocity(0)
                        self.right_motor.setVelocity(0)
                        continue

                    # Get data from compass
                    heading = self.get_compass_heading()

                    # Get GPS coordinates of the robot
                    robot_pos = self.get_gps_coordinates()

                    # Compute the speed for motors
                    direction = utils.get_direction(ball_data['direction'])

                    # If the robot has the ball right in front of it, go forward,
                    # rotate otherwise
                    if direction == 0:
                        left_speed = -5
                        right_speed = -5
                    else:
                        left_speed = direction * 4
                        right_speed = direction * -4

                    # Set the speed to motors
                    self.left_motor.setVelocity(left_speed)
                    self.right_motor.setVelocity(right_speed)

                    # Send message to team robots
                    self.send_data_to_team(self.player_id)
