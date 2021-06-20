import time

from controller import Robot

from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP

TIME_STEP = 64


class MyScoringRobot(RCJSoccerRobot):
    def run(self):
        self.msg_counter = 1
        while self.robot.step(TIME_STEP) != -1:
            self.send_msg(f"MY TEST MESSAGE {self.msg_counter}")
            self.msg_counter += 1
            self.receive_msg()
            #time.sleep(1)

            if self.is_new_data():
                data = self.get_new_data()

                #Get the position of our robot
                robot_pos = data[self.name]
                # Get the position of the ball
                ball_pos = data['ball']

                # YOUR CODE HERE

                left_speed = 1 * 4
                right_speed = 1 * -4

                # Set the speed to motors
                self.left_motor.setVelocity(left_speed)
                self.right_motor.setVelocity(right_speed)

ip = "78.47.128.91"
port = 10002
my_scoring_robot = MyScoringRobot(Robot())
my_scoring_robot.setup_tcp_connection(ip, port)
my_scoring_robot.run()
my_scoring_robot.close_connection()
