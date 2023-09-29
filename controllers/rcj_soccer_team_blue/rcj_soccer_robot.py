import json
import math

TIME_STEP = 32
ROBOT_NAMES = ["B1", "B2", "B3", "Y1", "Y2", "Y3"]
N_ROBOTS = len(ROBOT_NAMES)


class RCJSoccerRobot:
    def __init__(self, robot):
        self.robot = robot
        self.name = self.robot.getName()
        self.team = self.name[0]
        self.player_id = int(self.name[1])

        self.receiver = self.robot.getDevice("supervisor receiver")
        self.receiver.enable(TIME_STEP)

        self.team_emitter = self.robot.getDevice("team emitter")
        self.team_receiver = self.robot.getDevice("team receiver")
        self.team_receiver.enable(TIME_STEP)

        self.ball_receiver = self.robot.getDevice("ball receiver")
        self.ball_receiver.enable(TIME_STEP)

        self.gps = self.robot.getDevice("gps")
        self.gps.enable(TIME_STEP)

        self.compass = self.robot.getDevice("compass")
        self.compass.enable(TIME_STEP)

        self.sonar_left = self.robot.getDevice("distancesensor left")
        self.sonar_left.enable(TIME_STEP)
        self.sonar_right = self.robot.getDevice("distancesensor right")
        self.sonar_right.enable(TIME_STEP)
        self.sonar_front = self.robot.getDevice("distancesensor front")
        self.sonar_front.enable(TIME_STEP)
        self.sonar_back = self.robot.getDevice("distancesensor back")
        self.sonar_back.enable(TIME_STEP)

        self.left_motor = self.robot.getDevice("left wheel motor")
        self.right_motor = self.robot.getDevice("right wheel motor")

        self.left_motor.setPosition(float("+inf"))
        self.right_motor.setPosition(float("+inf"))

        self.left_motor.setVelocity(0.0)
        self.right_motor.setVelocity(0.0)

    def parse_supervisor_msg(self, data: str) -> dict:
        """Parse message received from supervisor

        Args:
            data: json data encoded into string

        Returns:
            dict: data decoded into dictionary
            Example:
                {
                    'waiting_for_kickoff': False,
                }
        """
        return json.loads(data)

    def get_new_data(self) -> dict:
        """Read new data from supervisor

        Returns:
            dict: See `parse_supervisor_msg` method
        """
        data = self.receiver.getString()
        self.receiver.nextPacket()
        return self.parse_supervisor_msg(data)

    def is_new_data(self) -> bool:
        """Check if there is new data from supervisor to be received

        Returns:
            bool: Whether there is new data received from supervisor.
        """
        return self.receiver.getQueueLength() > 0

    def parse_team_msg(self, data: str) -> dict:
        """Parse message received from team robot

        Args:
            dict: json data encoded into string

        Returns:
            dict: data decoded into dictionary
        """
        return json.loads(data)

    def get_new_team_data(self) -> dict:
        """Read new data from team robot

        Returns:
            dict: See `parse_team_msg` method
        """
        data = self.team_receiver.getString()
        self.team_receiver.nextPacket()
        return self.parse_team_msg(data)

    def is_new_team_data(self) -> bool:
        """Check if there is new data from team robots to be received

        Returns:
            bool: Whether there is new data received from team robots.
        """
        return self.team_receiver.getQueueLength() > 0

    def send_data_to_team(self, robot_id: int) -> None:
        """Send data to the team

        Args:
             robot_id (int): ID of the robot
        """
        data = {"robot_id": robot_id}
        self.team_emitter.send(json.dumps(data))

    def get_new_ball_data(self) -> dict:
        """Read new data from IR sensor

        Returns:
            dict: Direction and strength of the ball signal
            Direction is normalized vector indicating the direction of the
            emitter with respect to the receiver's coordinate system.
            Example:
                {
                    'direction': [0.23, -0.10, 0.96],
                    'strength': 0.1
                }
        """
        _ = self.ball_receiver.getString()
        data = {
            # TODO: Remove [:3] once
            #   https://github.com/cyberbotics/webots/pull/6394
            #   is released and Webots updated
            "direction": self.ball_receiver.getEmitterDirection()[:3],
            "strength": self.ball_receiver.getSignalStrength(),
        }
        self.ball_receiver.nextPacket()
        return data

    def is_new_ball_data(self) -> bool:
        """Check if there is new data from ball to be received

        Returns:
            bool: Whether there is new data received from ball.
        """
        return self.ball_receiver.getQueueLength() > 0

    def get_gps_coordinates(self) -> list:
        """Get new GPS coordinates

        Returns:
            List containing x and y values
        """
        gps_values = self.gps.getValues()
        return [gps_values[0], gps_values[1]]

    def get_compass_heading(self) -> float:
        """Get compass heading in radians

        Returns:
            float: Compass value in radians
        """
        compass_values = self.compass.getValues()

        # Add math.pi/2 (90) so that the heading 0 is facing opponent's goal
        rad = math.atan2(compass_values[0], compass_values[1]) + (math.pi / 2)
        if rad < -math.pi:
            rad = rad + (2 * math.pi)

        return rad

    def get_sonar_values(self) -> dict:
        """Get new values from sonars.

        Returns:
            dict: Value for each sonar.
        """
        return {
            "left": self.sonar_left.getValue(),
            "right": self.sonar_right.getValue(),
            "front": self.sonar_front.getValue(),
            "back": self.sonar_back.getValue(),
        }

    def run(self):
        raise NotImplementedError
