from controller import Robot

from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP

TIME_STEP = 64


class MyScoringRobot(RCJSoccerRobot):
    def run(self):
        while self.robot.step(TIME_STEP) != -1:
            # Get the position of our robot
            robot_pos = self.get_posfrom_devices()
            # Get lidar ranges in an array indexed 0..359, index 0 = front, 90-1 = right, 180-1 = back, 270-1 = left
            lidar_ranges = self.lidar.getRangeImage()
            # just for experiments: print sensor values
            print(robot_pos, 'front range:', lidar_ranges[0])

            if self.is_new_data():
                data = self.get_new_data()

                # Get the position of the ball
                ball_pos = data['ball']

                # YOUR CODE HERE

                # At first you might want to consider some experiments with still robot, then turning faster and faster
                speed = 0.00
                left_speed = 1 * speed
                right_speed = 1 * -speed

                # Set the speed to motors
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)


my_scoring_robot = MyScoringRobot(Robot())
my_scoring_robot.run()
