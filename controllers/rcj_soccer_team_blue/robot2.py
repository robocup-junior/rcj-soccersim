# rcj_soccer_player controller - ROBOT B2

# Feel free to import built-in libraries
import math  # noqa: F401

# You can also import scripts that you put into the folder with controller
import utils
from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP

class MyRobot2(RCJSoccerRobot):
    def run(self):
        kick_time = 0
        while self.robot.step(TIME_STEP) != -1:
            kick_time += TIME_STEP  # Time in milliseconds
            if self.is_new_data():
                data = self.get_new_data()  # noqa: F841

                while self.is_new_team_data():
                    team_data = self.get_new_team_data()  # noqa: F841
                    # Do something with team data

                if self.is_new_ball_data():
                    ball_data = self.get_new_ball_data()
                else:
                    # If the robot does not see the ball, stop motors
                    self.front_left_motor.setVelocity(0.0)
                    self.front_right_motor.setVelocity(0.0)
                    self.rear_left_motor.setVelocity(0.0)
                    self.rear_right_motor.setVelocity(0.0)
                    continue

                # Get data from compass
                heading = self.get_compass_heading()  # noqa: F841

                # Get GPS coordinates of the robot
                robot_pos = self.get_gps_coordinates()  # noqa: F841

                # Get data from sonars
                sonar_values = self.get_sonar_values()  # noqa: F841

                # Compute the speed for motors
                direction = utils.get_direction(ball_data["direction"])

                """
                Wheel motors (max velocity: 40, +: counterclockwise, -: clockwise)
                Dribbler motor (max velocity: 50, +: hold, -: release)
                Kicker motor (max velocity: 20, state 1: out, state 0: in, call kickBall function)
                """

                # If the robot has the ball right in front of it, go forward, rotate otherwise
                # Set the speed to motors
                if direction == 0:
                    move_speed = 40
                    self.front_left_motor.setVelocity(move_speed)
                    self.rear_left_motor.setVelocity(move_speed)
                    self.front_right_motor.setVelocity(-move_speed)
                    self.rear_right_motor.setVelocity(-move_speed)
                else:
                    turn_speed = -direction * 20
                    self.front_left_motor.setVelocity(turn_speed)
                    self.rear_left_motor.setVelocity(turn_speed)
                    self.front_right_motor.setVelocity(turn_speed)
                    self.rear_right_motor.setVelocity(turn_speed)

                # Dribble the ball at a velocity of 50
                self.dribbler_motor.setVelocity(50)

                # Kick the ball for 0.5 seconds every 5 seconds
                if 5000 < kick_time < 5500:
                    self.kick_ball(1, 20)
                elif kick_time > 5500:
                    kick_time = 0
                else:
                    self.kick_ball(0, 20)

                # Send message to team robots
                self.send_data_to_team(self.player_id)
