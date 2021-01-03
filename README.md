# RCJ Soccer Simulator

This is the official repository of the RoboCupJunior Soccer Simulator. The
simulator is based on [Webots](https://github.com/cyberbotics/webots) and this
repository provides both the "automatic referee" (which implements the [Soccer
Simulated Rules](https://github.com/RoboCupJuniorTC/soccer-rules-simulation))
as well as a sample simulated team of robots with some basic strategy.

![Soccer Sim](./docs/docs/images/soccer_sim.png)

*Learn more in the [documentation](https://robocupjuniortc.github.io/rcj-soccer-sim/).*

## How do I try this out?

1. Download [Webots](https://www.cyberbotics.com/#download)

2. Clone this repository to your computer by downloading the ZIP file from [here](https://github.com/RoboCupJuniorTC/rcj-soccer-sim/archive/master.zip) or running

        git clone https://github.com/RoboCupJuniorTC/rcj-soccer-sim.git

3. Soccer Sim needs Python version 3.7 (or higher). You can download it from [here](https://www.python.org/downloads/).

4. In Webots, go to `Tools > Preferences > Python command` and set it to `python` or `python3` to point Webots to Python 3. Depending on your system, the reference to Python 3 can be via the command `python` or `python3`. More information on how to configure Webots to work with Python can be found [here](https://cyberbotics.com/doc/guide/using-python).

5. Use Webots to open the downloaded `soccer.wbt` world located in the `worlds`
   directory (via `File > Open World`)

6. Run the simulation. Note that the controllers that are responsible for the
   various robots on the field can be found in the `controllers/` directory.

## Notes

A specific `webots` world can be executed directly from the command line as
follows:

        webots --mode=run worlds/soccer.wbt

Which allows for at least some automation. Further info can be found in the
[docs](https://cyberbotics.com/doc/guide/starting-webots).

The sample players as well as the "automatic referee" are implemented in
Python, which should allow for easily updating the code to match the rules and
avoid any compilation issues.
