# How to program your robot

## Controllers

Each object in the simulation world can be controlled by a program.
This program is called **Controller**. Each robot should have exactly
one controller, implemented as a **Python3** program. There is an invisible referee object in the simulation,
which takes care of controlling the game and checking the rules.

The controllers are located in the `controllers` directory. The name of the controller
must be located in a subfolder with the same name (i.e. `robot/robot.py`)
and this name ought to be specified in `soccer.wbt` file.

## Hello world, robot!

We have prepared a few sample robot controllers. They can be found in the `controllers`
directory. The controllers for the robots of blue team are located in
`rcj_soccer_team_blue` folder and for the robots of yellow team in
`rcj_soccer_team_yellow` folder, respectively.

Team folders contain a file called `rcj_soccer_team_blue.py` (blue team)
or `rcj_soccer_team_yellow.py` (yellow team). Each of the robots initially runs
this file (for the competition, it should be `robot.py`). Based on the unique identifier of the robot (which can be `1`, `2` or `3`)
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
import json

TIME_STEP = 32
ROBOT_NAMES = ["B1", "B2", "B3", "Y1", "Y2", "Y3"]
N_ROBOTS = len(ROBOT_NAMES)


class MyRobot:
    def __init__(self, robot):
        self.robot = robot
        self.name = self.robot.getName()

        self.receiver = self.robot.getDevice("supervisor receiver")
        self.receiver.enable(TIME_STEP)

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

        self.left_motor.setPosition(float('+inf'))
        self.right_motor.setPosition(float('+inf'))

        self.left_motor.setVelocity(0.0)
        self.right_motor.setVelocity(0.0)

    def get_new_data(self):
        packet = self.receiver.getString()
        self.receiver.nextPacket()
        return json.loads(packet)

    def run(self):
        while self.robot.step(TIME_STEP) != -1:
            if self.receiver.getQueueLength() > 0:
                data = self.get_new_data()

                # Get data from compass
                heading = self.get_compass_heading()

                # Get GPS coordinates of the robot
                robot_pos = self.get_gps_coordinates()

                # Get data from sonars
                sonar_values = self.get_sonar_values()

                # Get direction and strength of the IR signal
                if self.is_new_ball_data():
                    ball_data = self.get_new_ball_data()

                self.left_motor.setVelocity(1)
                self.right_motor.setVelocity(-1)
```

Let's explain the code in detail:

```python
import json
```

This library is a [built-in Python library](https://docs.python.org/3/library/json.html),
which is required to decode the data sent by the supervisor.

```python
TIME_STEP = 32
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
    self.robot = robot
    self.name = self.robot.getName()
    ...
```

The `__init__` function is something like a constructor of the class and is called when an instance of the `MyRobot` object
is created. We use this function to initialize some important variables. The most important one
is the `Robot` instance, which allows us to get access to the so called Webots devices
like motor (for controlling the speed), receiver (for reading data from Supervisor),
and sensors like GPS, Compass, Sonars or IR Ball receiver.
**The name and the team of your robot** can be determined by calling `self.robot.getName()`.
It will give you one of `{"B1", "B2", "B3", "Y1", "Y2", "Y3"}`. The first letter determines
the team ("Blue", "Yellow"), while the second one is the robot's identifier.
If you want to know the side of your team (either "Blue" or "Yellow"), you can find out
by checking `self.name[0]`, which essentially gives you `"B"` for Blue or `"Y"` for Yellow side.

```python
def get_new_data(self):
    ...
```

We are not going to explain this deeply. This function simply decodes the incoming
data from supervisor. Feel free to copy and use it. The resulting dictionary
just contains a single bit of information: whether a goal was scored and we are waiting for a new kickoff.
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

heading = self.get_compass_heading()
robot_pos = self.get_gps_coordinates()
sonar_values = self.get_sonar_values()
if self.is_new_ball_data():
    ball_data = self.get_new_ball_data()

self.left_motor.setVelocity(1)
self.right_motor.setVelocity(-1)
```

And finally, after reading the new data received from supervisor as well as data
from sensors we do some calculations and set the speed of the motors.


### Available sensors

#### GPS

This sensor gives you the exact position of the robot.
For more information check [official GPS documentation](https://cyberbotics.com/doc/reference/gps).
In `rcj_soccer_robot.py` you can find `get_gps_coordinates()`, which demonstrates
how to work with GPS sensor.

#### Compass 

Useful sensor to determine the angle (rotation) of the robot from the north.
For more information check [official compass documentation](https://cyberbotics.com/doc/reference/compass).
In `rcj_soccer_robot.py` you can find `get_compass_heading()`, which demonstrates
how to work with compass sensor.

#### Sonars

There are four **sonars** mounted on the robot (each side having one). Since the
exact position of the robot may be retrieved from GPS, these sensors are useful
for detecting the opponent's robots. For more information check
[official distance sensor documentation](https://cyberbotics.com/doc/reference/distancesensor).

Note that you may encounter some error in measurements. When the robot is next to an
obstacle, the value returned is 0 with error of 0%. On the other hand, when the
sesnsor does not see anything, the value returned is 1000 with error of 5%.
The values and errors in between are linearly interpolated.

In `rcj_soccer_robot.py` you can find `get_sonar_values()`, which demonstrates
how to work with sonar sensors.
For debugging purposes, you may find it useful to turn on rendering rays of
distance sensors. This option is available in Webots GUI under
`View -> Optional Rendering -> Show DistanceSensor Rays`.

#### Ball IR Sensor

There is an infra-red emitter mounted onto the ball.
The emitter just emits a signal and each robot receives this signal if it is
located within a pre-defined range. The receiver is able to determine the
direction as well as strength of the signal, which can be used for navigating
robots towards the ball.

For more information check the [official receiver documentation](https://cyberbotics.com/doc/reference/receiver)
or our `get_new_ball_data()` method in `rcj_soccer_robot.py`.

## Importing shared code

Each team consists of three robots. These robots might share some of the code
and it is  actually [a good practice](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself)
not to duplicate code all over the place.

Imagine you have the folder structure which looks like this

```
controllers/
├── robot/
│   └── robot.py
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
Do not import anything from `robot.py` file, otherwise you might get
cyclic import problem.

## Supported external libraries

In general, the whole Python's
[standard library](https://docs.python.org/3/library/index.html) can be used in the
robot's programs.

Furthermore, to make the computations easier, the Soccer Sim environment
supports the following two Python libraries that are normally used for what's
called "scientific computing":

- [`numpy`](https://numpy.org/doc/stable/) *(version 1.20.2)*
- [`scipy`](https://docs.scipy.org/doc/scipy/reference/) *(version 1.6.3)*
