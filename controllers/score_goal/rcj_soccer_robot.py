import math
import struct
from typing import Tuple

TIME_STEP = 64
ROBOT_NAMES = ["Y3"]
N_ROBOTS = len(ROBOT_NAMES)


class RCJSoccerRobot:
    def __init__(self, robot):
        self.robot = robot
        self.name = self.robot.getName()
        self.team = self.name[0]
        self.player_id = int(self.name[1])

        self.receiver = self.robot.getDevice("receiver")
        self.receiver.enable(TIME_STEP)

        self.left_motor = self.robot.getDevice("left wheel motor")
        self.right_motor = self.robot.getDevice("right wheel motor")

        self.left_motor.setPosition(float('+inf'))
        self.right_motor.setPosition(float('+inf'))

        self.left_motor.setVelocity(0.0)
        self.right_motor.setVelocity(0.0)

        # for the sensors GPS & Compass & LIDAR the WBT file has to include them for the robot controlled
        self.gps = self.robot.getDevice("gps")
        self.gps.enable(TIME_STEP)
        self.compass = self.robot.getDevice("compass")
        self.compass.enable(TIME_STEP)
        self.lidar = self.robot.getDevice("lidar")
        self.lidar.enable(TIME_STEP)
        self.lidar.enablePointCloud()

    # support functions for sensors GPS & Compass
    def get_coordinates(self):
        gps_sensors = self.gps.getValues()
        return [gps_sensors[0], gps_sensors[2]]

    def get_compass_heading_in_grad(self):
        compass_values = self.compass.getValues()
        # subtract math.pi/2 (90) so that the heading is 0 facing 'north' (given x going from left to right) 
        rad = math.atan2(compass_values[0], compass_values[2]) - (math.pi / 2)
        if (rad < -math.pi):
            rad = rad + (2 * math.pi)
        rad *= -1   # originally for EUN rad would be returned, but this wolrd is in NUE, not so -1* has to be applied  
        return rad  # for degrees: rad / math.pi * 180.0

    def get_posfrom_devices(self):
        gps_pos = self.gps.getValues()
        compass_val = self.get_compass_heading_in_grad()
        return {'x': gps_pos[0], 'y': gps_pos[2], 'orientation': compass_val}

    def get_lidar_range_in_dir(self, dir):
        ranges = self.lidar.getRangeImage()
        return ranges[dir]

    def parse_supervisor_msg(self, packet: str) -> dict:
        """Parse message received from supervisor

        Returns:
            dict: Location info ONLY ABOUT the ball.
            Example:
                {
                    'B1': {'x': 0.0, 'y': 0.2, 'orientation': 1},
                    'B2': {'x': 0.4, 'y': -0.2, 'orientation': 1},
                    ...
                    'ball': {'x': -0.7, 'y': 0.3},
                    'waiting_for_kickoff': False,
                }
        """
        # X, Z and rotation for each robot
        # plus X and Z for ball
        # plus True/False telling whether the goal was scored
        struct_fmt = 'dd' + '?'

        unpacked = struct.unpack(struct_fmt, packet)

        data = {}
        #for i, r in enumerate(ROBOT_NAMES):
        #    data[r] = {
        #        "x": unpacked[3 * i],
        #        "y": unpacked[3 * i + 1],
        #        "orientation": unpacked[3 * i + 2]
        #    }
        #ball_data_index = 3 * N_ROBOTS
        data["ball"] = {
            "x": unpacked[0],
            "y": unpacked[1]
        }

        waiting_for_kickoff_data_index = 2
        data["waiting_for_kickoff"] = unpacked[waiting_for_kickoff_data_index]
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
        raise NotImplementedError
