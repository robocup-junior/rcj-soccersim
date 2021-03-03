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
directory. Each controller is prefixed with `rcj_soccer_player_`. They are all programmed in the same way,
meaning they rotate to face the ball and then goes towards it.

We decided to make the code reusable and put some common methods into
the `RCJSoccerRobot` class inside `rcj_soccer_robot.py` file.

Let's put together a simple program to showcase how you can go about programming a robot.

```python
from controller import Robot
import struct

TIME_STEP = 64
ROBOT_NAMES = ["B1", "B2", "B3", "Y1", "Y2", "Y3"]
N_ROBOTS = len(ROBOT_NAMES)


class MyRobot:
    def __init__(self):
        self.robot = Robot()
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


my_robot = MyRobot()
my_robot.run()
```

Let's explain the code in detail:

```python
from controller import Robot
```

The Robot class is required to be imported because this is the only way we are able
to controll the robot. The Robot class is shipped together with Webots.

```python
import struct
```

This library is a [built-in Python library](https://docs.python.org/3/library/struct.html), which is required to unpack the data sent by
the supervisor.

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
([Object Oriented Programming](https://realpython.com/python3-object-oriented-programming/)) is that you can later reuse the same common class
throughout your controllers and therefore make the code easier to read. We are
going to continue with our OOP approach.

```python
def __init__(self):
    self.robot = Robot()
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

This is the method which contains the logic for controlling the robot.

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

```python
my_robot = MyRobot()
my_robot.run()
```

In the very end of our program, we initialize the robot and call the method `run`
in order to execute the code.


## Importing shared code

Each team consists of three robots. These robots might share some of the code
and it is  actually [a good practice](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) not to duplicate code all over the place.

Imagine you have the folder structure which looks like this

```
controllers/
├── robot1/
│   └── robot1.py
|   └── utils.py
├── robot2/
│   └── robot2.py
├── robot3/
│   └── robot3.py
```

and within `robot2.py` you want to import some useful code from `utils.py`
located in the `robot1` folder. This is possible, but you need to put the following code snippet right at the 
top of your `robot2.py` file.

```python
import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
from robot1 import utils
```

This will ensure that the code from `robot1` is importable (it adds the parent folder
to the Python PATH -- the list of folders where Python looks when importing modules).

If you want to import `utils` within `robot1`, you do no have to add these
magic lines to `robot1.py`, but instead just call

```python
import utils
```

because the PATH actually contains the folder of the script which is being run.
