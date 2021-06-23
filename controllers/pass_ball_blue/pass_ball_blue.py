from controller import Robot

from robot1 import MyBallPassingRobot1
from robot2 import MyBallPassingRobot2


robot = Robot()
name = robot.getName()
robot_number = int(name[1])

if robot_number == 1:
    robot_controller = MyBallPassingRobot1(robot)
else:
    robot_controller = MyBallPassingRobot2(robot)

robot_controller.run()
