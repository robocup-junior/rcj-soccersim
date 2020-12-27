# rcj_soccer_player controller - ROBOT B3
from controller import Robot
import struct
import math

TIME_STEP = 64
MY_ROBOT_NAME = "B3"
ROBOT_NAMES = ["B1", "B2", "B3", "Y1", "Y2", "Y3"]
N_ROBOTS = len(ROBOT_NAMES)


def parse_supervisor_msg(packet: str) -> dict:
    # X, Z and rotation for each robot
    # plus X and Z for ball
    struct_fmt = 'ddd' * 6 + 'dd'

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

# create the Robot instance.
robot = Robot()

name = robot.getName()
team = name[0]
player_id = int(name[1])


receiver = robot.getReceiver("receiver")
receiver.enable(TIME_STEP)

left_motor = robot.getMotor("left wheel motor")
right_motor = robot.getMotor("right wheel motor")

left_motor.setPosition(float('+inf'))
right_motor.setPosition(float('+inf'))

left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

while robot.step(TIME_STEP) != -1:
    if receiver.getQueueLength() > 0:
        packet = receiver.getData()
        receiver.nextPacket()

        data = parse_supervisor_msg(packet)

        # Get the position of our robot
        robot_pos = data[name.upper()]
        # Get the position of the ball
        ball_pos = data['ball']

        robot_angle = robot_pos['orientation']

        # Get the angle between the robot and the ball
        angle = math.atan2(ball_pos['y'] - robot_pos['y'],
                           ball_pos['x'] - robot_pos['x'])

        if angle < 0:
            angle = 2 * math.pi + angle

        if robot_angle < 0:
            robot_angle = 2 * math.pi + robot_angle

        degrees = math.degrees(angle + robot_angle)

        # Axis Z is forward
        # TODO: change the robot's orientation so that X axis means forward
        degrees -= 90
        if degrees > 360:
            degrees -= 360

        left_speed = 1
        right_speed = -1

        # If the robot has the ball right in front of it, go forward, otherwise
        # rotate
        if degrees >= 345 or degrees <= 15:
            left_speed = -5
            right_speed = -5
        else:
            multiplier = -1 if degrees < 180 else 1
            left_speed = multiplier * 4
            right_speed = multiplier * -4

        left_motor.setVelocity(left_speed)
        right_motor.setVelocity(right_speed)
