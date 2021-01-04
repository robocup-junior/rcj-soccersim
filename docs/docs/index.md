# Welcome to RCJ Soccer Sim!

The RoboCupJunior Soccer Simulator is an attempt at playing RoboCupJunior
Soccer in a virtualized environment. It is an experimental project organized by
the RoboCupJunior Soccer Technical Committe.

![Screenshot of RCJ Soccer Sim](images/soccer_sim.png)

The simulator is based on [Webots](https://github.com/cyberbotics/webots). The
associated repository provides both the "automatic referee" (which implements
the [Soccer Simulated Rules](https://github.com/RoboCupJuniorTC/soccer-rules-simulation))
as well as a sample team of robots with some basic simulated strategy.

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

