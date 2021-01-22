# How to program your robot

## Controllers

Each object in the simulation world is able to be controlled by a program.
This program is called **Controller**. Each of the robots should have exactly
one controller **Python3** program. There is an invisible referee object in the simulation,
which takes care of controlling the game and checking the rules.

The controllers are located in `controllers` directory. The name of the controller
must be located in a subfolder with the same name and this name ought to be specified
in `soccer.wbt` file.

## Hello world, robot!

We have prepared an example robot controllers, which can be found in `controllers`
directory prefixed with `rcj_soccer_player`. Each robot is programmed the same way,
meaning it rotates to face the ball and goes towards it afterwards.

We decided to make the code reusable and put some common methods into
`RCJSoccerRobot` class inside `rcj_soccer_robot.py` file.

Let's put together a simple program on how to program the robot.

```python
from controller import Robot
import struct

TIME_STEP = 64
ROBOT_NAMES = ["B1", "B2", "B3", "Y1", "Y2", "Y3"]
N_ROBOTS = len(ROBOT_NAMES)


class MyRobot:
    def __init__(self):
        self.robot = Robot()
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
to controll the robot. The Robot class is shipped together with webots.

```python
import struct
```

This library is a built-in python library, which is required to unpack the data sent by
the supervisor.

```python
TIME_STEP = 64
ROBOT_NAMES = ["B1", "B2", "B3", "Y1", "Y2", "Y3"]
N_ROBOTS = len(ROBOT_NAMES)
```

We define some constants here, whose values we will be used later.

```python
class MyRobot:
```

You can wrap the program into the class as we did. The benefit of OOP
(object oriented programmin) is that you can later inherit from common class used
throughout your controllers and therefore make the code easier to read. We are
going to continue with our OOP approach.

```python
def __init__(self):
    self.robot = Robot()
    ...
```

The `__init__` something like constructor of the class and is called when the object
is created. We initialize some important variables there. The most important one
is the `Robot` instance, which allows us to get access to the so called devices
like motor (for controlling the speed) or receiver (for reading data from supervisor).

```python
def get_new_data(self):
    ...
``` 

We are not going to explain this deeply. This function is to parse the incoming
data from supervisor. Feel free to copy and use it. The resulting dictionary
contains positions of all of the robots as well as the position of the ball.

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

Before reading data, its important to check if there is actually something
in the queue.

```python
data = self.get_new_data()

robot_pos = data[self.name]
ball_pos = data['ball']

self.left_motor.setVelocity(1)
self.right_motor.setVelocity(-1)
```

And finally, read the new data received from supervisor, do some calculations
and set the speed of the motors.

```python
my_robot = MyRobot()
my_robot.run()
```

In the very end of our program, we initialize the robot and call the method `run`
in order to run the code.


## Importing shared code

Each team consists out of three robots. These robots might share some of the code
and its actually a good practice not to duplicate code all over the place.

Imagine you have the folder structure which looks like this

```
controllers
controllers/
├── robot1/
│   └── robot1.py
|   └── utils.py
├── robot2/
│   └── robot2.py
├── robot3/
│   └── robot3.py
```

and within `robot2.py` you want to import some useful code from the `utils.py`
located in `robot1` folder. This is possible, but you need to put the code below
on top of your `robot2.py` file.

```python
import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))
from robot1 import utils
``` 

This will ensure that the code from `robot1` is importable (adds the parent folder
to the PATH)

If you want to import `utils` within the `robot1`, you do no have to add these
magic lines to `robot1.py`, but instead just call

```python
import utils
```
