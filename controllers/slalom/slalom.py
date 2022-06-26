from controller import Robot
from robot1 import MyRobot1

robot = Robot()
name = robot.getName()

robot_controller = MyRobot1(robot)
robot_controller.run()
