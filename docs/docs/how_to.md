# How to program your robot

## Controllers

Each object in the simulation world can be controlled by a program.
This program is called **Controller**. Each robot should have exactly
one controller, implemented as a **Python3** program. There is an invisible referee object in the simulation,
which takes care of controlling the game and checking the rules.

The controllers are located in the `controllers` directory. The name of the controller
must be located in a subfolder with the same name (i.e. `my_controller/my_controller.py`)
and this name ought to be specified in `soccer.wbt` file.

## Hello world, robot!

We have prepared a few sample robot controllers. They can be found in the `controllers`
directory. The controllers for the robots of blue team are located in
`rcj_soccer_team_blue` folder and for the robots of yellow team in
`rcj_soccer_team_yellow` folder, respectively.

Team folders contain a file called `rcj_soccer_team_blue.py` (blue team)
or `rcj_soccer_team_yellow.py` (yellow team). Each of the robots initially runs
this file. Based on the unique identifier of the robot (which can be `1`, `2` or `3`)
we initialize the code for the particular robot.

### Script for determining and initializing the robot controller

A sample initial file might look as follows:

```python
from controller import Robot

from robot1 import MyRobot1
from robot2 import MyRobot2
from robot3 import MyRobot3


robot = Robot()
name = robot.getName()
robot_number = int(name[1])

if robot_number == 1:
    robot_controller = MyRobot1(robot)
elif robot_number == 2:
    robot_controller = MyRobot2(robot)
else:
    robot_controller = MyRobot3(robot)

robot_controller.run()
```

Let's describe a file for determining robot's name and running specific controller.

```python
from controller import Robot
```

The Robot class is required to be imported because this is the only way we are able
to controll the robot. The Robot class is shipped together with Webots.

```python
from robot1 import MyRobot1
from robot2 import MyRobot2
from robot3 import MyRobot3
```

Since all of robot controllers are located in the same directory, we can easily import them.

```python
robot = Robot()
name = robot.getName()
```

Initialize robot instance and get the name of the robot. The name is one of
the following `{"B1", "B2", "B3", "Y1", "Y2", "Y3"}`.

```python
robot_number = int(name[1])
if robot_number == 1:
    robot_controller = MyRobot1(robot)
elif robot_number == 2:
    robot_controller = MyRobot2(robot)
else:
    robot_controller = MyRobot3(robot)
```

By checking the second character in the name, we can easily get the number identifier
of the robot and initialize its controller appropriately.

```python
robot_controller.run()
```

We just call the method `run` in order to execute the code for the specific
robot we initialized previously.


### Robot controller

Let's put together a simple program to showcase how you can go about programming a robot.

```python
import struct

TIME_STEP = 64
ROBOT_NAMES = ["B1", "B2", "B3", "Y1", "Y2", "Y3"]
N_ROBOTS = len(ROBOT_NAMES)


class MyRobot:
    def __init__(self, robot):
        self.robot = robot
        self.name = self.robot.getName()

        self.receiver = self.robot.getDevice("receiver")
        self.receiver.enable(TIME_STEP)

        self.left_motor = self.robot.getDevice("left wheel motor")
        self.right_motor = self.robot.getDevice("right wheel motor")

        self.left_motor.setPosition(float('+inf'))
        self.right_motor.setPosition(float('+inf'))

        self.left_motor.setVelocity(0.0)
        self.right_motor.setVelocity(0.0)

    def get_new_data(self):
        packet = self.receiver.getData()
        self.receiver.nextPacket()

        struct_fmt = 'ddd' * 6 + 'dd' + '?'

        unpacked = struct.unpack(struct_fmt, packet)

        data = {}
        for i, r in enumerate(ROBOT_NAMES):
            data[r] = {
                "x": unpacked[3 * i],
                "y": unpacked[3 * i + 1],
                "orientation": unpacked[3 * i + 2]
            }
        ball_data_index = 3 * N_ROBOTS
        data["ball"] = {
            "x": unpacked[ball_data_index],
            "y": unpacked[ball_data_index + 1]
        }

        waiting_for_kickoff_data_index = ball_data_index + 2
        data["waiting_for_kickoff"] = unpacked[waiting_for_kickoff_data_index]
        return data

    def run(self):
        while self.robot.step(TIME_STEP) != -1:
            if self.receiver.getQueueLength() > 0:
                data = self.get_new_data()

                # Get the position of our robot
                robot_pos = data[self.name]
                # Get the position of the ball
                ball_pos = data['ball']

                self.left_motor.setVelocity(1)
                self.right_motor.setVelocity(-1)
```

Let's explain the code in detail:

```python
import struct
```

This library is a [built-in Python library](https://docs.python.org/3/library/struct.html),
which is required to unpack the data sent by the supervisor.

```python
TIME_STEP = 64
ROBOT_NAMES = ["B1", "B2", "B3", "Y1", "Y2", "Y3"]
N_ROBOTS = len(ROBOT_NAMES)
```

We also define some useful constants, whose values will be used later.

```python
class MyRobot:
```

You can wrap the program into the class as we did. The benefit of OOP
([Object Oriented Programming](https://realpython.com/python3-object-oriented-programming/))
is that you can later reuse the same common class throughout your controllers and
therefore make the code easier to read. We are going to continue with our OOP approach.

```python
def __init__(self, robot):
    self.robot = Robot
    self.name = self.robot.getName()
    ...
```

The `__init__` function is something like a constructor of the class and is called when an instance of the `MyRobot` object
is created. We use this function to initialize some important variables. The most important one
is the `Robot` instance, which allows us to get access to the so called Webots devices
like motor (for controlling the speed) or receiver (for reading data from Supervisor).
**The name and the team of your robot** can be determined by calling `self.robot.getName()`.
It will give you one of `{"B1", "B2", "B3", "Y1", "Y2", "Y3"}`. The first letter determines
the team ("Blue", "Yellow"), while the second one is the robot's identifier.

```python
def get_new_data(self):
    ...
```

We are not going to explain this deeply. This function is to parse the incoming
data from supervisor. Feel free to copy and use it. The resulting dictionary
contains positions of all of the robots as well as the position of the ball. Moreover,
it contains information whether the goal gets scored and we are waiting for new kickoff.
In case the goal gets scored, the value is `True` and is reset to `False` when the 
referee fires new kickoff.

```python
def run(self):
```

This is the method which contains the logic for controlling the robot. As mentioned
previously, it is called by our initialization script.

```python
while self.robot.step(TIME_STEP) != -1:
```

**The `step` function is crucial and must be used in every controller.
This function synchronizes the sensor and actuator data between Webots and the controllers.**


```python
if self.receiver.getQueueLength() > 0:
```

Before reading data, it is important to check if there is actually something
in the queue that we can read.

```python
data = self.get_new_data()

robot_pos = data[self.name]
ball_pos = data['ball']

self.left_motor.setVelocity(1)
self.right_motor.setVelocity(-1)
```

And finally, after reading the new data received from supervisor, we do some calculations
and set the speed of the motors.


## Importing shared code

Each team consists of three robots. These robots might share some of the code
and it is  actually [a good practice](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself)
not to duplicate code all over the place.

Imagine you have the folder structure which looks like this

```
controllers/
├── team_name/
│   └── team_name.py
│   └── robot1.py
│   └── robot2.py
│   └── robot3.py
|   └── utils.py
```

and within `robot1.py`, `robot2.py` and `robot3.py` you want to import
some useful code from `utils.py`. You can easily import it by calling

```python
import utils
```

and use the shared code rather than copying it into each of the controllers.
Do not import anything from `team_name.py` file, otherwise you might get
cyclic import problem.
