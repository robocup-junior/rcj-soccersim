import math
import struct
import os

from rcj_soccer_sim.msg import bot_command, bot_measurements

from typing import Tuple
from controller import Robot

ROBOT_NAMES = ["B1", "B2", "B3", "Y1", "Y2", "Y3"]
N_ROBOTS = len(ROBOT_NAMES)


class RCJSoccerRobot:
    def __init__(self):
        # create the Robot instance.
        self.robot = Robot()
        self.name = self.robot.getName()
        self.team = self.name[0]
        self.player_id = int(self.name[1])
        os.environ["ROS_MASTER_URI"] = os.environ["ROS_MASTER_URI_TEAM_" + self.team]
        os.environ["ROS_NAMESPACE"] = "/bot" + str(self.player_id)
        import rospy
        self.measurement_publisher = rospy.Publisher('bot_measurements', bot_measurements, queue_size=1)
        self.ros_node = rospy.init_node("bot" + str(self.player_id), anonymous=True)
        self.command_subscruber = rospy.Subscriber('bot_command', bot_command, self.apply_bot_command)

        self.receiver = self.robot.getDevice("receiver")
        self.receiver.enable(int(self.robot.getBasicTimeStep()))

        self.left_motor = self.robot.getDevice("left wheel motor")
        self.right_motor = self.robot.getDevice("right wheel motor")

        self.left_motor.setPosition(float('+inf'))
        self.right_motor.setPosition(float('+inf'))

        self.left_motor.setVelocity(0.0)
        self.right_motor.setVelocity(0.0)

    def apply_bot_command(self, bot_command):
        self.left_motor.setVelocity(bot_command.left_wheel_speed)
        self.right_motor.setVelocity(bot_command.right_wheel_speed)

    def parse_supervisor_msg(self, packet: str) -> dict:
        """Parse message received from supervisor

        Returns:
            dict: Location info about each robot and the ball.
            Example:
                {
                    'B1': {'x': 0.0, 'y': 0.2, 'orientation': 1},
                    'B2': {'x': 0.4, 'y': -0.2, 'orientation': 1},
                    ...
                    'ball': {'x': -0.7, 'y': 0.3}
                }
        """
        # X, Z and rotation for each robot
        # plus X and Z for ball
        struct_fmt = 'ddd' * N_ROBOTS + 'dd'

        unpacked = struct.unpack(struct_fmt, packet)

        data = {}
        for i, r in enumerate(ROBOT_NAMES):
            data[r] = {
                "x": unpacked[3 * i],
                "y": unpacked[3 * i + 1],
                "orientation": unpacked[3 * i + 2]
            }
        data["ball"] = {
            "x": unpacked[3 * N_ROBOTS],
            "y": unpacked[3 * N_ROBOTS + 1]
        }
        return data

    def get_new_data(self) -> dict:
        """Read new data from supervisor

        Returns:
            dict: See `parse_supervisor_msg` method
        """
        packet = self.receiver.getData()
        self.receiver.nextPacket()

        return self.parse_supervisor_msg(packet)

    def is_new_data(self) -> bool:
        """Check if there are new data to be received

        Returns:
            bool: Whether there is new data received from supervisor.
        """
        return self.receiver.getQueueLength() > 0

    def get_angles(self, ball_pos: dict, robot_pos: dict) -> Tuple[float, float]:
        """Get angles in degrees.

        Args:
            ball_pos (dict): Dict containing info about position of the ball
            robot_pos (dict): Dict containing info about position and rotation
                of the robot

        Returns:
            :rtype: (float, float):
                Angle between the robot and the ball
                Angle between the robot and the north
        """
        robot_angle: float = robot_pos['orientation']

        # Get the angle between the robot and the ball
        angle = math.atan2(
            ball_pos['y'] - robot_pos['y'],
            ball_pos['x'] - robot_pos['x'],
        )

        if angle < 0:
            angle = 2 * math.pi + angle

        if robot_angle < 0:
            robot_angle = 2 * math.pi + robot_angle

        robot_ball_angle = math.degrees(angle + robot_angle)

        # Axis Z is forward
        # TODO: change the robot's orientation so that X axis means forward
        robot_ball_angle -= 90
        if robot_ball_angle > 360:
            robot_ball_angle -= 360

        return robot_ball_angle, robot_angle

    def run(self):
        while self.robot.step(int(self.robot.getBasicTimeStep())) != -1:
            if self.is_new_data():
                data = self.get_new_data()

                # Get the position of our robot
                robot_pos = data[self.name]
                # Get the position of the ball
                ball_pos = data['ball']

                # Publish robot data
                measurement_msg = bot_measurements(pos_x=robot_pos['x'], pos_y=robot_pos['y'], theta=robot_pos['orientation'])
                self.measurement_publisher.publish(measurement_msg)

this_bot = RCJSoccerRobot()
this_bot.run()
